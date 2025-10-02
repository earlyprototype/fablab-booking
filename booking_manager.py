"""
Booking Manager
Handles all booking operations and storage
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

BOOKINGS_FILE = Path(__file__).parent / "bookings.json"


class BookingManager:
    """Manages equipment bookings with conflict detection"""
    
    def __init__(self):
        self.bookings_file = BOOKINGS_FILE
        self._ensure_bookings_file()
    
    def _ensure_bookings_file(self):
        """Create bookings file if it doesn't exist"""
        if not self.bookings_file.exists():
            self.bookings_file.write_text(json.dumps({"bookings": []}, indent=2))
    
    def load_bookings(self) -> List[Dict]:
        """Load all bookings from file"""
        try:
            data = json.loads(self.bookings_file.read_text())
            return data.get("bookings", [])
        except Exception as e:
            print(f"Error loading bookings: {e}")
            return []
    
    def save_bookings(self, bookings: List[Dict]):
        """Save bookings to file"""
        try:
            self.bookings_file.write_text(json.dumps({"bookings": bookings}, indent=2))
        except Exception as e:
            print(f"Error saving bookings: {e}")
    
    def create_booking(self, equipment_id: str, equipment_name: str, 
                      date: str, start_time: str, duration_hours: int,
                      user_name: str, user_email: str, notes: str = "") -> Dict:
        """Create a new booking"""
        bookings = self.load_bookings()
        
        # Generate booking ID
        booking_id = f"BK{len(bookings) + 1:04d}"
        
        # Create booking
        booking = {
            "id": booking_id,
            "equipment_id": equipment_id,
            "equipment_name": equipment_name,
            "date": date,
            "start_time": start_time,
            "duration_hours": duration_hours,
            "user_name": user_name,
            "user_email": user_email,
            "notes": notes,
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
            "end_time": self._calculate_end_time(start_time, duration_hours)
        }
        
        bookings.append(booking)
        self.save_bookings(bookings)
        
        return booking
    
    def _calculate_end_time(self, start_time: str, duration_hours: float) -> str:
        """Calculate end time from start time and duration (supports 30-min increments)"""
        start_hour = int(start_time.split(":")[0])
        start_min = int(start_time.split(":")[1])
        
        # Convert to minutes
        start_minutes = (start_hour * 60) + start_min
        duration_minutes = int(duration_hours * 60)
        end_minutes = start_minutes + duration_minutes
        
        # Convert back to hours and minutes
        end_hour = end_minutes // 60
        end_min = end_minutes % 60
        
        return f"{end_hour:02d}:{end_min:02d}"
    
    def check_conflict(self, equipment_id: str, date: str, start_time: str, 
                      duration_hours: float, exclude_booking_id: Optional[str] = None) -> bool:
        """Check if a booking conflicts with existing bookings"""
        bookings = self.load_bookings()
        
        # Parse times (support 30-min increments)
        start_hour = int(start_time.split(":")[0])
        start_min = int(start_time.split(":")[1])
        start_minutes = (start_hour * 60) + start_min
        end_minutes = start_minutes + int(duration_hours * 60)
        
        for booking in bookings:
            # Skip cancelled bookings or the booking being edited
            if booking["status"] == "cancelled":
                continue
            if exclude_booking_id and booking["id"] == exclude_booking_id:
                continue
            
            # Check if same equipment and date
            if booking["equipment_id"] == equipment_id and booking["date"] == date:
                # Check time overlap (in minutes)
                booking_start_hour = int(booking["start_time"].split(":")[0])
                booking_start_min = int(booking["start_time"].split(":")[1])
                booking_start_minutes = (booking_start_hour * 60) + booking_start_min
                
                booking_end_hour = int(booking["end_time"].split(":")[0])
                booking_end_min = int(booking["end_time"].split(":")[1])
                booking_end_minutes = (booking_end_hour * 60) + booking_end_min
                
                # Conflict if times overlap
                if not (end_minutes <= booking_start_minutes or start_minutes >= booking_end_minutes):
                    return True
        
        return False
    
    def get_bookings_for_date(self, date: str) -> List[Dict]:
        """Get all bookings for a specific date"""
        bookings = self.load_bookings()
        return [b for b in bookings if b["date"] == date and b["status"] != "cancelled"]
    
    def get_bookings_for_week(self, start_date: str) -> List[Dict]:
        """Get all bookings for a week starting from start_date"""
        bookings = self.load_bookings()
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=7)
        
        week_bookings = []
        for booking in bookings:
            if booking["status"] == "cancelled":
                continue
            booking_dt = datetime.strptime(booking["date"], "%Y-%m-%d")
            if start_dt <= booking_dt < end_dt:
                week_bookings.append(booking)
        
        return week_bookings
    
    def get_user_bookings(self, user_email: str) -> List[Dict]:
        """Get all bookings for a specific user"""
        bookings = self.load_bookings()
        return [b for b in bookings if b["user_email"] == user_email and b["status"] != "cancelled"]
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        bookings = self.load_bookings()
        
        for booking in bookings:
            if booking["id"] == booking_id:
                booking["status"] = "cancelled"
                booking["cancelled_at"] = datetime.now().isoformat()
                self.save_bookings(bookings)
                return True
        
        return False
    
    def get_booking_by_id(self, booking_id: str) -> Optional[Dict]:
        """Get a specific booking by ID"""
        bookings = self.load_bookings()
        for booking in bookings:
            if booking["id"] == booking_id:
                return booking
        return None

