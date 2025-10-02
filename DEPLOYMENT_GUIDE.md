# FabLab Equipment Booking - Streamlit Cloud Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Your code pushed to a GitHub repository

### 2. Repository Setup

**Option A: Create a New Repository**
```bash
cd components/nexus/fablab_booking
git init
git add .
git commit -m "Initial commit: FabLab booking system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fablab-booking.git
git push -u origin main
```

**Option B: Use Existing Repository**
- Ensure `components/nexus/fablab_booking/` is in your repo
- Push the latest changes

### 3. Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Configure**:
   - **Repository**: Your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `components/nexus/fablab_booking/app.py`
   - **Python version**: 3.11

5. **Advanced settings** (click to expand):
   - Add environment variables (see below)

6. **Click** "Deploy!"

### 4. Environment Variables (Required)

In Streamlit Cloud's "Advanced settings", add these secrets:

```toml
# API Configuration
API_BASE_URL = "YOUR_NEXUS_API_URL"  # e.g., "https://your-api.com"

# Microsoft Graph API (for emails)
MS_GRAPH_CLIENT_ID = "your_client_id"
MS_GRAPH_CLIENT_SECRET = "your_client_secret"
MS_GRAPH_TENANT_ID = "your_tenant_id"
MS_GRAPH_ACCESS_TOKEN = "your_access_token"
MS_GRAPH_REFRESH_TOKEN = "your_refresh_token"
```

**Note**: If you don't configure email settings, the system will still work but won't send confirmation emails.

### 5. API Backend Deployment

The booking system requires the Nexus API to be running. Deploy options:

**Option A: Deploy API Separately**
- Deploy `components/nexus/api/` to a cloud platform:
  - Heroku
  - Railway
  - Render
  - AWS/Azure/GCP
- Update `API_BASE_URL` in Streamlit Cloud secrets

**Option B: Run API Locally (for testing)**
```bash
cd components/nexus
python start_nexus.py
```
- Use ngrok or similar to expose local API
- Update `API_BASE_URL` to ngrok URL

### 6. Custom Domain (Optional)

Streamlit Cloud provides:
- Free subdomain: `https://your-app.streamlit.app`
- Custom domain support (paid plan)

---

## 📁 Required Files Checklist

Ensure these files exist in your deployment folder:

```
fablab_booking/
├── app.py                    ✅ Main application
├── booking_manager.py        ✅ Booking logic
├── equipment_config.py       ✅ Equipment setup
├── requirements.txt          ✅ Python dependencies
├── .streamlit/
│   └── config.toml          ✅ Streamlit config
└── bookings/                 📁 Created automatically
    └── bookings.json
```

---

## 🔧 Configuration Updates

### Update API URL in Code

If your API URL changes, update in `app.py`:

```python
# Around line 40-50
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8300")
```

### Email Configuration

The system will gracefully degrade if email isn't configured:
- Bookings still work
- Data is saved to JSON
- Email confirmation just won't be sent

---

## 🐛 Troubleshooting

### App Won't Start
- **Check**: Python version is 3.11
- **Check**: All files are in the correct path
- **Check**: `requirements.txt` is present

### API Connection Errors
- **Check**: `API_BASE_URL` is correctly set in secrets
- **Check**: API is accessible from internet
- **Check**: CORS is enabled on API for Streamlit Cloud domain

### Email Not Working
- **Check**: All MS Graph variables are set in secrets
- **Check**: Tokens haven't expired
- **Re-run**: `python components/nexus/auth_outlook_azure.py` to refresh tokens

### Bookings Not Persisting
- **Note**: Streamlit Cloud has ephemeral storage
- **Solution**: Consider database integration:
  - SQLite (simple)
  - PostgreSQL (Streamlit Cloud supports)
  - MongoDB Atlas (free tier)

---

## 🔐 Security Best Practices

1. **Never commit secrets** to GitHub
2. **Use Streamlit Secrets** for all sensitive data
3. **Rotate tokens** regularly
4. **Enable CORS** properly on API
5. **Use HTTPS** for production API

---

## 📊 Monitoring

Streamlit Cloud provides:
- **Analytics**: View usage stats
- **Logs**: Debug issues in real-time
- **Resource usage**: Monitor performance

Access via your app's settings page.

---

## 🚀 Going Live

### Pre-Launch Checklist:
- [ ] All features tested
- [ ] Email integration working
- [ ] API deployed and accessible
- [ ] Secrets configured
- [ ] Custom domain set up (optional)
- [ ] Users can login
- [ ] Bookings save correctly
- [ ] Email confirmations sent

### Launch!
1. Share your app URL: `https://your-app.streamlit.app`
2. Monitor logs for issues
3. Gather user feedback
4. Iterate and improve

---

## 🆘 Need Help?

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Status**: [status.streamlit.io](https://status.streamlit.io)

---

## 📈 Future Enhancements

Consider adding:
- Database integration (PostgreSQL)
- User authentication (OAuth)
- Admin dashboard
- Analytics tracking
- Mobile responsiveness improvements
- Calendar sync (Google Calendar, Outlook)
- SMS notifications
- Payment integration

