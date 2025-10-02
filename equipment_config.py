"""
FabLab Equipment Configuration
Defines all available equipment and their specifications
"""

EQUIPMENT_LIST = [
    {
        "id": "ceramic_printer",
        "name": "Ceramic 3D Printer",
        "description": "Large format ceramic 3D printing",
        "color": "#FF6B6B",
        "max_duration_hours": 4,
        "icon": "🏺"
    },
    {
        "id": "laser_cutter",
        "name": "Laser Cutter",
        "description": "CO2 laser cutter for wood, acrylic, etc.",
        "color": "#4ECDC4",
        "max_duration_hours": 3,
        "icon": "⚡"
    },
    {
        "id": "cnc_router",
        "name": "CNC Router",
        "description": "3-axis CNC router for wood and soft metals",
        "color": "#95E1D3",
        "max_duration_hours": 4,
        "icon": "🔩"
    },
    {
        "id": "resin_printer",
        "name": "Resin 3D Printer",
        "description": "High-resolution resin printing",
        "color": "#F38181",
        "max_duration_hours": 8,
        "icon": "💧"
    },
    {
        "id": "vinyl_cutter",
        "name": "Vinyl Cutter",
        "description": "Large format vinyl cutting",
        "color": "#AA96DA",
        "max_duration_hours": 2,
        "icon": "✂️"
    },
    {
        "id": "embroidery",
        "name": "Embroidery Machine",
        "description": "Digital embroidery and textile work",
        "color": "#FCBAD3",
        "max_duration_hours": 3,
        "icon": "🧵"
    }
]

# Operating hours
OPENING_HOUR = 9  # 9am
CLOSING_HOUR = 17  # 5pm
OPERATING_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Booking rules
MIN_BOOKING_DURATION = 0.5  # hours (30 minutes)
MAX_BOOKING_DURATION = 4  # hours
BOOKING_SLOT_INCREMENT = 0.5  # 30-minute increments

# Email configuration
FACILITIES_MANAGER_EMAIL = "carl@creativespark.ie"  # Carl's email
FACILITIES_MANAGER_NAME = "Carl McAteer"
GENERAL_ENQUIRIES_EMAIL = "hello@creativespark.ie"

