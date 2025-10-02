"""
FabLab Equipment Booking System
A Streamlit app for booking FabLab equipment with calendar view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import httpx
import os
from equipment_config import (
    EQUIPMENT_LIST, OPENING_HOUR, CLOSING_HOUR, OPERATING_DAYS,
    MIN_BOOKING_DURATION, MAX_BOOKING_DURATION,
    FACILITIES_MANAGER_EMAIL, FACILITIES_MANAGER_NAME
)
from booking_manager import BookingManager

# API Configuration - use environment variable or fallback to localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8300")

# Page configuration
st.set_page_config(
    page_title="FabLab Equipment Booking",
    page_icon="🏭",
    layout="wide"
)

# Initialize booking manager
if "booking_manager" not in st.session_state:
    st.session_state.booking_manager = BookingManager()

# Initialize session state
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def send_booking_email(booking: dict) -> bool:
    """Send separate booking emails to facilities manager and user"""
    try:
        # Send to Carl (Staff Notification)
        response1 = httpx.post(
            f"{API_BASE_URL}/v1/email/send-equipment-booking",
            json={
                "equipment_name": booking['equipment_name'],
                "booking_date": booking['date'],
                "booking_time": booking['start_time'],
                "duration": float(booking['duration_hours']),
                "recipient": FACILITIES_MANAGER_EMAIL,
                "project_name": "FabLab Staff Notification",
                "project_id": booking['id'],
                "client_name": booking['user_name'],
                "is_staff_email": True
            },
            timeout=30.0
        )
        
        # Send to User (Confirmation)
        response2 = httpx.post(
            f"{API_BASE_URL}/v1/email/send-equipment-booking",
            json={
                "equipment_name": booking['equipment_name'],
                "booking_date": booking['date'],
                "booking_time": booking['start_time'],
                "duration": float(booking['duration_hours']),
                "recipient": booking['user_email'],
                "project_name": "FabLab User Confirmation",
                "project_id": booking['id'],
                "client_name": booking['user_name'],
                "is_staff_email": False,
                "user_notes": booking.get('notes', '')
            },
            timeout=30.0
        )
        
        return response1.status_code == 200 and response2.status_code == 200
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False


def generate_time_slots():
    """Generate 30-minute time slots from opening to closing"""
    slots = []
    current_hour = OPENING_HOUR
    current_min = 0
    
    while current_hour < CLOSING_HOUR:
        slots.append(f"{current_hour:02d}:{current_min:02d}")
        current_min += 30
        if current_min >= 60:
            current_min = 0
            current_hour += 1
    
    return slots


def get_two_week_dates():
    """Get dates for the next 2 weeks from today"""
    dates = []
    start_date = datetime.now().date()
    
    for i in range(14):
        date = start_date + timedelta(days=i)
        dates.append(date)
    
    return dates


def is_slot_booked(equipment_id: str, date: str, time_slot: str, bookings: list) -> bool:
    """Check if a specific time slot is booked"""
    for booking in bookings:
        if booking["equipment_id"] != equipment_id or booking["date"] != date:
            continue
        
        # Parse times
        slot_hour = int(time_slot.split(":")[0])
        slot_min = int(time_slot.split(":")[1])
        slot_time = slot_hour + (slot_min / 60.0)
        
        booking_start_hour = int(booking["start_time"].split(":")[0])
        booking_start_min = int(booking["start_time"].split(":")[1])
        booking_start = booking_start_hour + (booking_start_min / 60.0)
        
        booking_end_hour = int(booking["end_time"].split(":")[0])
        booking_end_min = int(booking["end_time"].split(":")[1])
        booking_end = booking_end_hour + (booking_end_min / 60.0)
        
        # Check if slot is within booking time
        if booking_start <= slot_time < booking_end:
            return True
    
    return False


def show_equipment_calendar(equipment: dict):
    """Display calendar view for a specific piece of equipment"""
    dates = get_two_week_dates()
    time_slots = generate_time_slots()
    
    # Get all bookings for the equipment
    bookings = st.session_state.booking_manager.load_bookings()
    equipment_bookings = [b for b in bookings 
                         if b["equipment_id"] == equipment["id"] 
                         and b["status"] != "cancelled"]
    
    # Create calendar grid with equipment info and contact details side by side
    header_col1, header_col2, header_col3 = st.columns([2, 2, 2])
    
    with header_col1:
        st.markdown(f"### {equipment['name']}")
        st.markdown(f"*{equipment['description']}*")
        st.markdown("**📧 Booking Manager:** [carl@creativespark.ie](mailto:carl@creativespark.ie)")
    
    with header_col2:
        st.markdown("**🕐 Operating Hours**")
        st.markdown("Monday - Friday")
        st.markdown("9:00 AM - 5:00 PM")
    
    with header_col3:
        st.markdown("**⏱️ Booking Info**")
        st.markdown("30-minute slots")
        st.markdown("Max 4 hours per booking")
        
    # General Enquiries row - aligned left across all columns
    st.markdown("**💬 General Enquiries:** [hello@creativespark.ie](mailto:hello@creativespark.ie)")
    
    st.markdown("---")
    
    # Create columns for dates (scrollable)
    with st.container():
        # Date headers - aligned with time slots below
        header_cols = st.columns([0.5] + [1] * len(dates))
        
        # Empty space above time labels
        with header_cols[0]:
            st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
        
        # Date headers
        for idx, date in enumerate(dates):
            with header_cols[idx + 1]:
                day_name = date.strftime("%a")
                day_num = date.strftime("%d")
                month = date.strftime("%b")
                
                is_weekend = date.strftime("%A") not in OPERATING_DAYS
                
                # Check if this is today
                is_today = date == datetime.now().date()
                
                if is_weekend:
                    st.markdown(f"<div style='text-align: center; background-color: #E0E0E0; padding: 8px; border-radius: 5px;'>"
                              f"<small>{day_name}</small><br><b>{day_num}</b><br><small>{month}</small></div>",
                              unsafe_allow_html=True)
                elif is_today:
                    st.markdown(f"<div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>"
                              f"<small style='opacity: 0.9;'>{day_name}</small><br><b style='font-size: 1.2rem;'>{day_num}</b><br><small style='opacity: 0.9;'>TODAY</small></div>",
                              unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: center; padding: 8px;'>"
                              f"<small>{day_name}</small><br><b>{day_num}</b><br><small>{month}</small></div>",
                              unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Time slot rows with AM/PM dividers
        for idx, time_slot in enumerate(time_slots):
            # Add AM/PM divider
            if time_slot == "09:00":
                st.markdown("""<div style='background: linear-gradient(90deg, transparent, #e1e4e8 20%, #e1e4e8 80%, transparent); 
                            height: 2px; margin: 12px 0;'></div>
                            <div style='text-align: center; color: #6b7280; font-weight: 600; font-size: 0.9rem; 
                            margin: 8px 0; letter-spacing: 1px;'>☀️ MORNING (9:00 AM - 12:00 PM)</div>
                            <div style='background: linear-gradient(90deg, transparent, #e1e4e8 20%, #e1e4e8 80%, transparent); 
                            height: 2px; margin: 12px 0 16px 0;'></div>""", unsafe_allow_html=True)
            elif time_slot == "12:00":
                st.markdown("""<div style='background: linear-gradient(90deg, transparent, #fbbf24 20%, #fbbf24 80%, transparent); 
                            height: 2px; margin: 12px 0;'></div>
                            <div style='text-align: center; color: #92400e; font-weight: 600; font-size: 0.9rem; 
                            margin: 8px 0; letter-spacing: 1px;'>☀️ AFTERNOON (12:00 PM - 5:00 PM)</div>
                            <div style='background: linear-gradient(90deg, transparent, #fbbf24 20%, #fbbf24 80%, transparent); 
                            height: 2px; margin: 12px 0 16px 0;'></div>""", unsafe_allow_html=True)
            
            cols = st.columns([0.5] + [1] * len(dates))
            
            # Time label (on one line)
            with cols[0]:
                st.markdown(f"<div style='text-align: right; padding-right: 10px; font-weight: 600; color: #4b5563; white-space: nowrap;'>{time_slot}</div>",
                          unsafe_allow_html=True)
            
            # Date cells
            for idx, date in enumerate(dates):
                with cols[idx + 1]:
                    date_str = date.strftime("%Y-%m-%d")
                    is_weekend = date.strftime("%A") not in OPERATING_DAYS
                    
                    if is_weekend:
                        # Grey out weekends
                        st.markdown("<div style='background-color: #E0E0E0; height: 35px; border-radius: 3px; border: 1.5px solid #c0c0c0;'></div>",
                                  unsafe_allow_html=True)
                    else:
                        # Check if booked
                        booked_by_user = False
                        booked_by_other = False
                        
                        for booking in equipment_bookings:
                            if is_slot_booked(equipment["id"], date_str, time_slot, [booking]):
                                if booking["user_email"] == st.session_state.user_email:
                                    booked_by_user = True
                                else:
                                    booked_by_other = True
                                break
                        
                        if booked_by_user:
                            # Light blue for user's bookings
                            st.markdown("<div style='background-color: #ADD8E6; height: 35px; border-radius: 3px; cursor: not-allowed; border: 1.5px solid #7fb3d5;'></div>",
                                      unsafe_allow_html=True)
                        elif booked_by_other:
                            # Red for other bookings
                            st.markdown("<div style='background-color: #FF4444; height: 35px; border-radius: 3px; cursor: not-allowed; border: 1.5px solid #cc0000;'></div>",
                                      unsafe_allow_html=True)
                        else:
                            # White with thin black border for available (clickable)
                            button_html = f"""
                            <button onclick="window.location.href='?book={equipment['id']}_{date_str}_{time_slot}'" 
                                    style='width: 100%; height: 30px; background-color: white; 
                                           border: 1px solid #000000; border-radius: 3px; 
                                           cursor: pointer;'
                                    title='Book {equipment['name']} on {date_str} at {time_slot}'>
                            </button>
                            """
                            
                            if st.button("", key=f"{equipment['id']}_{date_str}_{time_slot}", 
                                       help=f"Book {equipment['name']} on {date_str} at {time_slot}",
                                       use_container_width=True):
                                st.session_state.selected_booking = {
                                    "equipment": equipment,
                                    "date": date_str,
                                    "time": time_slot
                                }
                                st.rerun()


def show_booking_modal():
    """Show booking form in a modal"""
    if "selected_booking" not in st.session_state:
        return
    
    booking_info = st.session_state.selected_booking
    
    st.markdown("---")
    st.markdown(f"## 📝 Book {booking_info['equipment']['name']}")
    
    with st.form("quick_booking_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Equipment:** {booking_info['equipment']['name']}")
            st.write(f"**Date:** {booking_info['date']}")
            st.write(f"**Start Time:** {booking_info['time']}")
            
            # Duration selection
            max_duration = min(
                MAX_BOOKING_DURATION,
                booking_info['equipment']['max_duration_hours']
            )
            duration_options = [MIN_BOOKING_DURATION + (i * 0.5) 
                              for i in range(int(max_duration / 0.5) + 1)]
            duration = st.selectbox(
                "Duration (hours)",
                options=duration_options,
                format_func=lambda x: f"{x:.1f} hours" if x != 0.5 else "30 minutes"
            )
        
        with col2:
            # Pre-populate with logged-in user details
            user_name = st.text_input("Your Name*", value=st.session_state.user_name, disabled=True)
            user_email = st.text_input("Your Email*", value=st.session_state.user_email, disabled=True)
            notes = st.text_area("Notes (optional)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            submit = st.form_submit_button("✅ Confirm Booking", use_container_width=True)
        with col_b:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if cancel:
            del st.session_state.selected_booking
            st.rerun()
        
        if submit:
            if not user_name or not user_email:
                st.error("Please fill in your name and email")
            else:
                # Check for conflicts
                has_conflict = st.session_state.booking_manager.check_conflict(
                    booking_info['equipment']['id'],
                    booking_info['date'],
                    booking_info['time'],
                    duration
                )
                
                if has_conflict:
                    st.error("❌ This time slot is already booked. Please choose a different time.")
                else:
                    # Create booking
                    booking = st.session_state.booking_manager.create_booking(
                        equipment_id=booking_info['equipment']['id'],
                        equipment_name=booking_info['equipment']['name'],
                        date=booking_info['date'],
                        start_time=booking_info['time'],
                        duration_hours=duration,
                        user_name=user_name,
                        user_email=user_email,
                        notes=notes
                    )
                    
                    # Save user details
                    st.session_state.user_name = user_name
                    st.session_state.user_email = user_email
                    
                    # Send email
                    email_sent = send_booking_email(booking)
                    
                    if email_sent:
                        st.success(f"✅ Booking confirmed! ID: **{booking['id']}**")
                    else:
                        st.success(f"✅ Booking confirmed! ID: **{booking['id']}**")
                        st.warning("⚠️ Email notification failed")
                    
                    del st.session_state.selected_booking
                    st.rerun()


def show_login_form():
    """Show simple login form"""
    st.markdown("## 🔐 Login to Book Equipment")
    st.markdown("Please enter your details to access the booking system")
    
    with st.form("login_form"):
        name = st.text_input("Your Name*")
        email = st.text_input("Your Email*")
        
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if name and email:
                # Simple email validation
                if "@" in email and "." in email:
                    st.session_state.user_name = name
                    st.session_state.user_email = email
                    st.session_state.logged_in = True
                    st.success(f"Welcome, {name}!")
                    st.rerun()
                else:
                    st.error("Please enter a valid email address")
            else:
                st.error("Please fill in both fields")


def show_my_bookings_sidebar():
    """Show user's bookings in sidebar"""
    with st.sidebar:
        # Show user info and logout
        if st.session_state.logged_in:
            st.markdown(f"**Logged in as:**")
            st.markdown(f"👤 {st.session_state.user_name}")
            st.markdown(f"📧 {st.session_state.user_email}")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_name = ""
                st.session_state.user_email = ""
                st.rerun()
            
            st.markdown("---")
        
        st.markdown("## 👤 My Bookings")
        
        if not st.session_state.user_email:
            st.info("Login to see your bookings")
            return
        
        bookings = st.session_state.booking_manager.get_user_bookings(st.session_state.user_email)
        
        if not bookings:
            st.info("You have no active bookings")
            return
        
        for booking in sorted(bookings, key=lambda x: (x["date"], x["start_time"])):
            with st.expander(f"{booking['equipment_name'][:15]}...", expanded=False):
                st.write(f"**Date:** {booking['date']}")
                st.write(f"**Time:** {booking['start_time']}-{booking['end_time']}")
                st.write(f"**ID:** {booking['id']}")
                
                if st.button("Cancel", key=f"cancel_{booking['id']}", use_container_width=True):
                    st.session_state.booking_manager.cancel_booking(booking['id'])
                    st.success("Cancelled")
                    st.rerun()


# Main app
def main():
    # Apply comprehensive custom styling
    st.markdown("""
    <style>
    /* Global font improvements */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header styling */
    h1 {
        font-weight: 700 !important;
        color: #1a1a1a !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-weight: 600 !important;
        color: #2c2c2c !important;
    }
    
    h3 {
        font-weight: 600 !important;
        color: #3a3a3a !important;
        font-size: 1.4rem !important;
    }
    
    /* Larger, more prominent tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #e1e4e8;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        height: 50px;
        padding: 0 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #0066cc !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #e8f2ff !important;
        transform: translateY(-2px);
    }
    
    /* Better button styling for calendar slots */
    .stButton button {
        background-color: white !important;
        border: 1.5px solid #d1d5db !important;
        color: black !important;
        transition: all 0.15s ease !important;
        border-radius: 4px !important;
    }
    
    .stButton button:hover {
        background-color: #f0f9ff !important;
        border-color: #0066cc !important;
        transform: scale(1.05) !important;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.1) !important;
    }
    
    /* Form styling improvements */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 8px !important;
        border: 1.5px solid #d1d5db !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #d1fae5 !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        animation: slideIn 0.3s ease;
    }
    
    /* Error message styling */
    .stError {
        background-color: #fee2e2 !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #dbeafe !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 2px solid #e1e4e8;
    }
    
    /* Login form centering */
    .login-container {
        max-width: 450px;
        margin: 60px auto;
        padding: 40px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Animation keyframes */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Calendar grid improvements */
    .calendar-header {
        font-weight: 600;
        color: #4b5563;
        padding: 8px;
        text-align: center;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 14px;
            padding: 0 16px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏭 FabLab Equipment Booking")
    
    # Sidebar (always show)
    show_my_bookings_sidebar()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        show_login_form()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Quick stats banner
    today = datetime.now().date()
    bookings_today = st.session_state.booking_manager.get_bookings_for_date(today.strftime("%Y-%m-%d"))
    total_slots_today = len(generate_time_slots()) * len([d for d in get_two_week_dates() if d == today]) * len(EQUIPMENT_LIST)
    available_today = total_slots_today - len(bookings_today)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Today's Date", today.strftime("%d %B %Y"))
    with col2:
        st.metric("✅ Available Slots Today", available_today)
    with col3:
        st.metric("📊 Active Bookings", len([b for b in st.session_state.booking_manager.load_bookings() if b["status"] != "cancelled"]))
    
    st.markdown("---")
    
    # Main instruction with flat pale blue styling
    st.markdown("""
    <div style='background: #e6f2ff; 
                padding: 20px; 
                border-radius: 0px; 
                color: #1a1a1a; 
                margin-bottom: 24px;
                border-left: 4px solid #0066cc;'>
        <h3 style='margin: 0; color: #1a1a1a; font-size: 1.3rem;'>💡 Click any start time to book equipment</h3>
        <p style='margin: 8px 0 0 0; color: #4b5563;'>⬜ Available  |  🔴 Booked by Others  |  🔵 Your Bookings  |  ⬜ Weekend (Closed)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show booking modal if a slot is selected
    if "selected_booking" in st.session_state:
        show_booking_modal()
    
    # Equipment tabs with specific icons
    tabs = st.tabs([f"{e.get('icon', '🔧')} {e['name']}" for e in EQUIPMENT_LIST])
    
    for idx, equipment in enumerate(EQUIPMENT_LIST):
        with tabs[idx]:
            show_equipment_calendar(equipment)
    
    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>© 2024 Creative Spark FabLab | Powered by FactoryXChange</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
