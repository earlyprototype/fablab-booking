# 🚀 Quick Start - 5 Minutes to Deploy

## Step 1: Push to GitHub (2 minutes)

```bash
cd components/nexus/fablab_booking
git init
git add .
git commit -m "FabLab booking system"
gh repo create fablab-booking --public --source=. --remote=origin --push
```

Or manually:
1. Create new repo on GitHub: `fablab-booking`
2. Push this folder to it

## Step 2: Deploy to Streamlit Cloud (2 minutes)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repo: `fablab-booking`
4. Main file: `app.py`
5. Click "Deploy"

## Step 3: Done! (1 minute)

Your app is live at: `https://your-app.streamlit.app`

---

## Optional: Enable Email Notifications

If you want booking confirmations sent via email:

1. In Streamlit Cloud, click your app
2. Go to "Settings" → "Secrets"
3. Add:
```toml
MS_GRAPH_CLIENT_ID = "your_id"
MS_GRAPH_CLIENT_SECRET = "your_secret"
MS_GRAPH_TENANT_ID = "your_tenant"
MS_GRAPH_ACCESS_TOKEN = "your_token"
MS_GRAPH_REFRESH_TOKEN = "your_refresh"
```

(Get these by running `python components/nexus/auth_outlook_azure.py`)

---

## That's It!

Your FabLab booking system is now live and accessible to anyone!

**Test it**: Make a booking and see it appear in the calendar.

**Share it**: Send the URL to your users.

**Monitor it**: Check Streamlit Cloud for usage stats.

---

## Need the API?

The app works standalone for testing, but for production with email:

**Option 1: Deploy API to Railway (free)**
```bash
cd components/nexus
railway init
railway up
```

**Option 2: Use existing deployment**
Add to Streamlit secrets:
```toml
API_BASE_URL = "https://your-api.com"
```

Full guide: See `DEPLOYMENT_GUIDE.md`

