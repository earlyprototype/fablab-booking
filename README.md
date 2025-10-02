# 🏭 FabLab Equipment Booking System

**A modern, user-friendly equipment booking system built with Streamlit**

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## ✨ Features

- 📅 **Visual Calendar** - 2-week rolling view with color-coded availability
- 🔐 **Simple Login** - Email-based authentication
- 📧 **Email Notifications** - Automatic confirmations to managers and users
- 📱 **Mobile Responsive** - Works on any device
- 🎨 **Modern UI** - Clean, professional design
- ⚡ **Real-time Updates** - Instant booking confirmations
- 🏷️ **Equipment Icons** - Visual identification for each machine

---

## 🚀 Quick Deploy

**Deploy to Streamlit Cloud in 5 minutes:**

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your repo
4. Main file: `app.py`
5. Deploy!

**See**: `QUICK_START.md` for detailed steps

---

## 🏭 Equipment Supported

- 🏺 Ceramic 3D Printer
- ⚡ Laser Cutter
- 🔩 CNC Router
- 💧 Resin 3D Printer
- ✂️ Vinyl Cutter
- 🧵 Embroidery Machine

---

## 📋 Documentation

- **[QUICK_START.md](QUICK_START.md)** - 5-minute deployment
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Comprehensive guide
- **[STREAMLIT_CLOUD_READY.md](STREAMLIT_CLOUD_READY.md)** - Deployment checklist
- **[CALENDAR_BEHAVIOR.md](CALENDAR_BEHAVIOR.md)** - How the calendar works

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend API**: FastAPI (optional, for emails)
- **Storage**: JSON (local) or PostgreSQL (cloud)
- **Email**: Microsoft Graph API
- **Hosting**: Streamlit Cloud

---

## 🎯 Use Cases

Perfect for:
- FabLabs & Makerspaces
- University workshops
- Co-working spaces
- Studio equipment
- Shared resources

---

## 📸 Screenshots

### Login Screen
Clean, centered authentication

### Calendar View
2-week view with color-coded slots:
- ⬜ White = Available
- 🔴 Red = Booked by others
- 🔵 Blue = Your bookings
- ⬜ Grey = Weekends

### Booking Form
Quick, simple booking with duration selection

---

## ⚙️ Configuration

### Environment Variables:
```toml
API_BASE_URL = "https://your-api.com"  # Optional
MS_GRAPH_CLIENT_ID = "..."  # For emails
MS_GRAPH_CLIENT_SECRET = "..."
MS_GRAPH_TENANT_ID = "..."
```

### Equipment Configuration:
Edit `equipment_config.py` to:
- Add/remove equipment
- Change operating hours
- Adjust booking rules
- Update contact emails

---

## 📧 Contact Information

- **Booking Manager**: carl@creativespark.ie
- **General Enquiries**: hello@creativespark.ie
- **Website**: www.factoryxchange.ie

---

## 🔐 Security

- Email-based authentication
- Session management
- HTTPS recommended for production
- Environment-based secrets
- No passwords stored

---

## 📈 Roadmap

- [ ] Database integration (PostgreSQL)
- [ ] Admin dashboard
- [ ] Calendar sync (Google/Outlook)
- [ ] SMS notifications
- [ ] Multi-location support
- [ ] Analytics & reporting
- [ ] Payment integration
- [ ] Resource management

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - Feel free to use and modify

---

## 🆘 Support

- **Issues**: GitHub Issues
- **Community**: Streamlit Community Forum
- **Docs**: See documentation files above

---

## 🎉 Ready to Deploy!

```bash
# See the Quick Start guide
cat QUICK_START.md
```

Made with ❤️ by Creative Spark FabLab

A Streamlit-based equipment booking system for FabLab users to book equipment with automatic email notifications.

## Features

- 📅 **Visual Calendar View** - See all bookings at a glance
- 🎯 **Easy Booking** - Select equipment, date, time, and duration
- 🚫 **Conflict Detection** - Prevents double-booking
- 📧 **Email Notifications** - Automatically notifies Carl of new bookings
- 👤 **My Bookings** - View and manage your bookings
- ⏰ **Operating Hours** - Enforces Mon-Fri, 9am-5pm schedule

## Equipment Available

1. **Ceramic 3D Printer** - Large format ceramic 3D printing (max 4 hours)
2. **Laser Cutter** - CO2 laser cutter (max 3 hours)
3. **CNC Router** - 3-axis CNC router (max 4 hours)
4. **Resin 3D Printer** - High-resolution resin printing (max 8 hours)
5. **Vinyl Cutter** - Large format vinyl cutting (max 2 hours)
6. **Embroidery Machine** - Digital embroidery (max 3 hours)

## How to Run

### Prerequisites
- Nexus API running on port 8300
- Microsoft Graph API configured (for email notifications)

### Start the Booking System

```powershell
cd components/nexus/fablab_booking
streamlit run app.py --server.port 8503
```

The app will be available at: http://localhost:8503

## Usage

### 1. Make a Booking
1. Go to "Make Booking" tab
2. Enter your name and email
3. Select equipment
4. Choose date and time
5. Select duration
6. Add notes (optional)
7. Click "Confirm Booking"

### 2. View Calendar
- Navigate weeks using Previous/Next buttons
- See all bookings color-coded by availability
- Green = Available
- Red = Booked

### 3. Manage Your Bookings
- Go to "My Bookings" tab
- View all your active bookings
- Cancel bookings if needed

## Configuration

Edit `equipment_config.py` to:
- Add/remove equipment
- Change operating hours
- Modify booking duration limits
- Update email recipients

## File Structure

```
fablab_booking/
├── app.py                  # Main Streamlit application
├── booking_manager.py      # Booking logic and storage
├── equipment_config.py     # Equipment and settings
├── bookings.json          # Booking data storage (auto-created)
└── README.md              # This file
```

## Email Integration

Emails are sent via the Nexus API email endpoint which uses Microsoft Graph API.

**Email Recipient:** Carl McAteer (Facilities Manager)
**Current Test Email:** thom@creativespark.ie

## Booking Rules

- Minimum booking: 1 hour
- Maximum booking: 4 hours (or equipment-specific limit)
- Operating hours: 9am - 5pm
- Operating days: Monday - Friday
- Bookings can be made up to 60 days in advance

## Support

For issues or questions, contact the FabLab team at info@factoryxchange.ie

