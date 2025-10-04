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
    page_icon="image.png",
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
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "show_admin_dashboard" not in st.session_state:
    st.session_state.show_admin_dashboard = False


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
    
    # Create calendar grid with equipment info side by side
    header_col1, header_col2, header_col3 = st.columns([3, 2.5, 2.5])
    
    with header_col1:
        st.markdown(f"### {equipment['name']}")
        st.markdown(f"*{equipment['description']}*")
    
    with header_col2:
        st.markdown("<div style='text-align: center;'><strong>🕐 Operating Hours</strong></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>Monday - Friday</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>9:00 AM - 5:00 PM</div>", unsafe_allow_html=True)
    
    with header_col3:
        st.markdown("<div style='text-align: center;'><strong>⏱️ Booking Info</strong></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>30-minute slots</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>Max 8 hours per booking</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create columns for dates (scrollable)
    with st.container():
        # Date headers - aligned with time slots below
        header_cols = st.columns([0.7] + [1] * len(dates))
        
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
                    st.markdown(f"<div style='text-align: center; background-color: #9CA3AF; padding: 8px; border-radius: 5px;'>"
                              f"<small>{day_name}</small><br><b>{day_num}</b><br><small>{month}</small></div>",
                              unsafe_allow_html=True)
                elif is_today:
                    st.markdown(f"<div style='text-align: center; background: #D4DDD7; color: #4A6759; padding: 8px; border-radius: 8px;'>"
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
                st.markdown("""<div style='background: linear-gradient(90deg, transparent, #D4DDD7 20%, #D4DDD7 80%, transparent); 
                            height: 2px; margin: 12px 0;'></div>
                            <div style='text-align: center; color: #4A6759; font-weight: 600; font-size: 0.9rem; 
                            margin: 8px 0; letter-spacing: 1px;'>☀️ MORNING (9:00 AM - 12:00 PM)</div>
                            <div style='background: linear-gradient(90deg, transparent, #D4DDD7 20%, #D4DDD7 80%, transparent); 
                            height: 2px; margin: 12px 0 16px 0;'></div>""", unsafe_allow_html=True)
            elif time_slot == "12:00":
                st.markdown("""<div style='background: linear-gradient(90deg, transparent, #B5C4BA 20%, #B5C4BA 80%, transparent); 
                            height: 2px; margin: 12px 0;'></div>
                            <div style='text-align: center; color: #4A6759; font-weight: 600; font-size: 0.9rem; 
                            margin: 8px 0; letter-spacing: 1px;'>☀️ AFTERNOON (12:00 PM - 5:00 PM)</div>
                            <div style='background: linear-gradient(90deg, transparent, #B5C4BA 20%, #B5C4BA 80%, transparent); 
                            height: 2px; margin: 12px 0 16px 0;'></div>""", unsafe_allow_html=True)
            
            cols = st.columns([0.7] + [1] * len(dates))
            
            # Time label (on one line)
            with cols[0]:
                st.markdown(f"<div style='text-align: right; padding-right: 20px; font-weight: 600; color: #4A6759; white-space: nowrap;'>{time_slot}</div>",
                          unsafe_allow_html=True)
            
            # Date cells
            for idx, date in enumerate(dates):
                with cols[idx + 1]:
                    date_str = date.strftime("%Y-%m-%d")
                    is_weekend = date.strftime("%A") not in OPERATING_DAYS
                    
                    if is_weekend:
                        # Grey out weekends
                        st.markdown("<div style='background-color: #9CA3AF; height: 35px; border-radius: 3px; border: 1.5px solid #6B7280;'></div>",
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
                            # Soft Coral Pink for user's bookings
                            st.markdown("<div style='background-color: #F3C5C5; height: 35px; border-radius: 3px; cursor: not-allowed; border: 1.5px solid #E8AFA8;'></div>",
                                      unsafe_allow_html=True)
                        elif booked_by_other:
                            # Dusty Rose for other bookings
                            st.markdown("<div style='background-color: #D4918D; height: 35px; border-radius: 3px; cursor: not-allowed; border: 1.5px solid #C17F7A;'></div>",
                                      unsafe_allow_html=True)
                        else:
                            # White with thin black border for available (clickable)
                            button_html = f"""
                            <button onclick="window.location.href='?book={equipment['id']}_{date_str}_{time_slot}'" 
                                    style='width: 100%; height: 30px; background-color: white; 
                                           border: 1.5px solid #6B8E7F; border-radius: 3px; 
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
                    # Check if admin (Carl's email)
                    st.session_state.is_admin = (email.lower() == "carl@creativespark.ie")
                    if st.session_state.is_admin:
                        st.success(f"Welcome, {name}! (Admin Access)")
                    else:
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
                st.session_state.is_admin = False
                st.session_state.show_admin_dashboard = False
                st.rerun()
            
            # Admin dashboard button
            if st.session_state.is_admin:
                if st.session_state.show_admin_dashboard:
                    if st.button("📅 Back to Booking Calendar", use_container_width=True, type="primary"):
                        st.session_state.show_admin_dashboard = False
                        st.rerun()
                else:
                    if st.button("👨‍💼 Admin Dashboard", use_container_width=True, type="primary"):
                        st.session_state.show_admin_dashboard = True
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


def show_admin_dashboard():
    """Admin dashboard for Carl to view all bookings and analytics"""
    st.title("👨‍💼 Admin Dashboard")
    st.markdown("**Manager:** Carl McAteer | **Email:** carl@creativespark.ie")
    st.markdown("---")
    
    # Get all bookings
    all_bookings = st.session_state.booking_manager.load_bookings()
    active_bookings = [b for b in all_bookings if b["status"] != "cancelled"]
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 All Bookings", "👥 User Analytics", "🛠️ Equipment Analytics", "📅 Weekly Overview", "📊 Export Data"])
    
    with tab1:
        st.subheader("All Bookings")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status_filter = st.selectbox("Status", ["All", "Active", "Cancelled"])
        with col2:
            equipment_filter = st.selectbox("Equipment", ["All"] + [e["name"] for e in EQUIPMENT_LIST])
        with col3:
            user_filter = st.selectbox("User", ["All"] + sorted(list(set([b["user_email"] for b in all_bookings]))))
        with col4:
            date_from = st.date_input("From Date", value=datetime.now().date() - timedelta(days=30))
        
        # Filter bookings
        filtered_bookings = all_bookings.copy()
        if status_filter == "Active":
            filtered_bookings = [b for b in filtered_bookings if b["status"] != "cancelled"]
        elif status_filter == "Cancelled":
            filtered_bookings = [b for b in filtered_bookings if b["status"] == "cancelled"]
        
        if equipment_filter != "All":
            filtered_bookings = [b for b in filtered_bookings if b["equipment_name"] == equipment_filter]
        
        if user_filter != "All":
            filtered_bookings = [b for b in filtered_bookings if b["user_email"] == user_filter]
        
        filtered_bookings = [b for b in filtered_bookings if datetime.strptime(b["date"], "%Y-%m-%d").date() >= date_from]
        
        # Display as table
        if filtered_bookings:
            df = pd.DataFrame(filtered_bookings)
            df = df[["date", "start_time", "end_time", "equipment_name", "user_name", "user_email", "status"]]
            df.columns = ["Date", "Start", "End", "Equipment", "User", "Email", "Status"]
            df = df.sort_values("Date", ascending=False)
            st.dataframe(df, use_container_width=True, height=400)
            st.info(f"**Total:** {len(filtered_bookings)} bookings")
        else:
            st.info("No bookings match the selected filters")
    
    with tab2:
        st.subheader("User Analytics")
        
        # Get unique users
        users = list(set([b["user_email"] for b in active_bookings]))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Monthly Bookings (Last 30 Days)")
            now = datetime.now().date()
            thirty_days_ago = now - timedelta(days=30)
            
            user_monthly_stats = {}
            for user in users:
                count = len([b for b in active_bookings 
                           if b["user_email"] == user 
                           and datetime.strptime(b["date"], "%Y-%m-%d").date() >= thirty_days_ago])
                if count > 0:
                    user_monthly_stats[user] = count
            
            if user_monthly_stats:
                monthly_df = pd.DataFrame(list(user_monthly_stats.items()), columns=["User", "Bookings"])
                monthly_df = monthly_df.sort_values("Bookings", ascending=False)
                st.dataframe(monthly_df, use_container_width=True, hide_index=True)
            else:
                st.info("No bookings in the last 30 days")
        
        with col2:
            st.markdown("### Annual Bookings (Last 365 Days)")
            one_year_ago = now - timedelta(days=365)
            
            user_annual_stats = {}
            for user in users:
                count = len([b for b in active_bookings 
                           if b["user_email"] == user 
                           and datetime.strptime(b["date"], "%Y-%m-%d").date() >= one_year_ago])
                if count > 0:
                    user_annual_stats[user] = count
            
            if user_annual_stats:
                annual_df = pd.DataFrame(list(user_annual_stats.items()), columns=["User", "Bookings"])
                annual_df = annual_df.sort_values("Bookings", ascending=False)
                st.dataframe(annual_df, use_container_width=True, hide_index=True)
            else:
                st.info("No bookings in the last year")
    
    with tab3:
        st.subheader("Equipment Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Total Bookings by Equipment")
            equipment_stats = {}
            for equipment in EQUIPMENT_LIST:
                count = len([b for b in active_bookings if b["equipment_name"] == equipment["name"]])
                equipment_stats[equipment["name"]] = count
            
            if equipment_stats:
                eq_df = pd.DataFrame(list(equipment_stats.items()), columns=["Equipment", "Bookings"])
                eq_df = eq_df.sort_values("Bookings", ascending=False)
                st.dataframe(eq_df, use_container_width=True, hide_index=True)
                
                # Bar chart
                st.bar_chart(eq_df.set_index("Equipment"))
        
        with col2:
            st.markdown("### Utilisation Rate (Last 30 Days)")
            thirty_days_ago = datetime.now().date() - timedelta(days=30)
            
            for equipment in EQUIPMENT_LIST:
                recent_bookings = len([b for b in active_bookings 
                                      if b["equipment_name"] == equipment["name"]
                                      and datetime.strptime(b["date"], "%Y-%m-%d").date() >= thirty_days_ago])
                st.metric(equipment["name"], f"{recent_bookings} bookings")
    
    with tab4:
        st.subheader("Weekly Equipment Schedule")
        st.markdown("Visual timeline showing when each machine is booked")
        
        # Week selector
        col1, col2 = st.columns([1, 3])
        with col1:
            week_offset = st.number_input("Week offset", min_value=-4, max_value=4, value=0, help="0 = current week, -1 = last week, +1 = next week")
        
        # Calculate week dates
        today = datetime.now().date()
        days_since_monday = today.weekday()
        monday_this_week = today - timedelta(days=days_since_monday)
        target_monday = monday_this_week + timedelta(weeks=week_offset)
        week_dates = [target_monday + timedelta(days=i) for i in range(5)]
        
        with col2:
            st.info(f"**Week of:** {target_monday.strftime('%d %B %Y')} - {week_dates[-1].strftime('%d %B %Y')}")
        
        st.markdown("---")
        
        # Color palette for different users
        user_colors = {}
        color_palette = ["#F3C5C5", "#D4918D", "#B8CADB", "#95B3A8", "#E8B4A0", "#C68968"]
        
        # For each equipment, show a timeline for each day
        for equipment in EQUIPMENT_LIST:
            st.markdown(f"### {equipment['icon']} {equipment['name']}")
            
            # Create columns for each day
            day_cols = st.columns(5)
            
            for day_idx, date in enumerate(week_dates):
                with day_cols[day_idx]:
                    date_str = date.strftime("%Y-%m-%d")
                    day_name = date.strftime("%a %d")
                    
                    st.markdown(f"<div style='text-align: center; font-weight: 600; color: #2C3E36; margin-bottom: 8px;'>{day_name}</div>", unsafe_allow_html=True)
                    
                    # Get bookings for this equipment on this day
                    day_bookings = [b for b in active_bookings 
                                   if b["equipment_name"] == equipment["name"] 
                                   and b["date"] == date_str]
                    
                    if day_bookings:
                        # Sort by start time
                        day_bookings.sort(key=lambda x: x["start_time"])
                        
                        for booking in day_bookings:
                            # Assign consistent color to user
                            user_email = booking["user_email"]
                            if user_email not in user_colors:
                                user_colors[user_email] = color_palette[len(user_colors) % len(color_palette)]
                            
                            bg_color = user_colors[user_email]
                            
                            # Create booking block
                            with st.expander(f"{booking['start_time']}-{booking['end_time']}", expanded=False):
                                st.markdown(f"**👤 {booking['user_name']}**")
                                st.markdown(f"📧 {booking['user_email']}")
                                st.markdown(f"⏰ {booking['start_time']} - {booking['end_time']}")
                                
                            # Visual block representation
                            st.markdown(f"""
                            <div style='background-color: {bg_color}; 
                                        padding: 6px; 
                                        border-radius: 4px; 
                                        margin-bottom: 4px;
                                        border-left: 4px solid {user_colors[user_email]};
                                        font-size: 0.75rem;
                                        color: #2C3E36;'>
                                <strong>{booking['start_time'][:5]}</strong> - <strong>{booking['end_time'][:5]}</strong><br>
                                <small>{booking['user_name'][:20]}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='text-align: center; color: #9CA3AF; padding: 20px; background: #F5F7F5; border-radius: 4px; margin-top: 8px;'>Available</div>", unsafe_allow_html=True)
            
            st.markdown("---")
        
        # User color legend
        if user_colors:
            st.markdown("### 👥 User Colour Legend")
            legend_text = " | ".join([f"<span style='color: {color}; font-weight: bold;'>●</span> {email}" 
                                     for email, color in list(user_colors.items())[:6]])
            st.markdown(legend_text, unsafe_allow_html=True)
    
    with tab5:
        st.subheader("Export Data")
        
        st.markdown("Download booking data as CSV for external analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### All Active Bookings")
            if active_bookings:
                df_export = pd.DataFrame(active_bookings)
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="📥 Download Active Bookings CSV",
                    data=csv,
                    file_name=f"fablab_active_bookings_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No active bookings to export")
        
        with col2:
            st.markdown("### All Bookings (Including Cancelled)")
            if all_bookings:
                df_all = pd.DataFrame(all_bookings)
                csv_all = df_all.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Bookings CSV",
                    data=csv_all,
                    file_name=f"fablab_all_bookings_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No bookings to export")


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
    
    /* Integrated tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
        padding: 0px;
        border-radius: 0px;
        border-bottom: 2px solid #D4DDD7;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        height: 50px;
        padding: 0 24px;
        border-radius: 0px;
        border-bottom: 3px solid transparent;
        font-weight: 500;
        font-size: 16px;
        transition: all 0.2s ease;
        color: #4A6759 !important;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #F5F7F5 !important;
        color: #6B8E7F !important;
        border-bottom: 3px solid #6B8E7F !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #F5F7F5 !important;
        border-bottom: 3px solid #B5C4BA !important;
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
        background-color: #F5F7F5 !important;
        border-color: #6B8E7F !important;
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
        border-color: #6B8E7F !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #E8EDE8 !important;
        border-left: 4px solid #6B8E7F !important;
        border-radius: 8px !important;
        padding: 16px !important;
        animation: slideIn 0.3s ease;
    }
    
    /* Error message styling */
    .stError {
        background-color: #F5E8E8 !important;
        border-left: 4px solid #A67B7B !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #E8EDE8 !important;
        border-left: 4px solid #6B8E7F !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        background-color: #F5F7F5;
        border-right: 2px solid #D4DDD7;
    }
    
    /* Login form centering */
    .login-container {
        max-width: 220px;
        margin: 60px auto;
        padding: 0px;
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
    
    # Header with logo
    header_left, header_right = st.columns([4, 1])
    with header_left:
        st.title("FabLab Equipment Booking")
    with header_right:
        try:
            st.image("image.png", width=150)
        except:
            pass  # If logo not found, just skip it
    
    # Sidebar (always show)
    show_my_bookings_sidebar()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        show_login_form()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Show admin dashboard if requested
    if st.session_state.show_admin_dashboard and st.session_state.is_admin:
        show_admin_dashboard()
        return
    
    # Quick stats banner
    today = datetime.now().date()
    
    # Count user's active bookings
    user_bookings = [b for b in st.session_state.booking_manager.load_bookings() 
                     if b["status"] != "cancelled" and b["user_email"] == st.session_state.user_email]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📅 Today's Date", today.strftime("%d %B %Y"))
    with col2:
        st.metric("📊 My Active Bookings", len(user_bookings))
    
    st.markdown("---")
    
    # Main instruction with flat muted sage styling
    st.markdown("""
    <div style='background: #E8EDE8; 
                padding: 20px; 
                border-radius: 0px; 
                color: #2C3E36; 
                margin-bottom: 24px;
                border-left: 4px solid #6B8E7F;
                display: flex;
                justify-content: space-between;
                align-items: center;'>
        <div>
            <h3 style='margin: 0; color: #2C3E36; font-size: 1.3rem;'>💡 Click any start time to book equipment</h3>
            <p style='margin: 8px 0 0 0; color: #4A6759;'>
                <span style='display: inline-block; width: 18px; height: 18px; background: white; border: 1.5px solid #6B8E7F; border-radius: 2px; vertical-align: middle;'></span> Available  |  
                <span style='display: inline-block; width: 18px; height: 18px; background: #D4918D; border-radius: 2px; vertical-align: middle;'></span> Booked by Others  |  
                <span style='display: inline-block; width: 18px; height: 18px; background: #F3C5C5; border-radius: 2px; vertical-align: middle;'></span> Your Bookings  |  
                <span style='display: inline-block; width: 18px; height: 18px; background: #9CA3AF; border: 1.5px solid #6B7280; border-radius: 2px; vertical-align: middle;'></span> Weekend (Closed)
            </p>
        </div>
        <div style='text-align: right; font-size: 0.9rem; color: #4A6759; white-space: nowrap;'>
            <div style='margin-bottom: 4px;'><strong>Booking Manager:</strong> <a href='mailto:carl@creativespark.ie' style='color: #6B8E7F;'>carl@creativespark.ie</a></div>
            <div><strong>General Enquiries:</strong> <a href='mailto:hello@creativespark.ie' style='color: #6B8E7F;'>hello@creativespark.ie</a></div>
        </div>
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
    st.markdown("<div style='text-align: center; color: #4A6759; font-size: 0.9rem;'>© 2024 Creative Spark FabLab | Powered by FactoryXChange</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
