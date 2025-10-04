# 🚀 FabLab Booking System - Deployment Options

## Overview
Your booking system is currently deployed on **Streamlit Cloud** (free tier). This document outlines all deployment options, with focus on **free and reliable** solutions.

---

## 📊 Deployment Options Comparison

| Option | Cost | Reliability | Complexity | Custom Domain | Best For |
|--------|------|-------------|------------|---------------|----------|
| **Streamlit Cloud (Current)** | FREE | ⭐⭐⭐⭐ | ⭐ Easy | Paid only | Quick start |
| **Railway** | FREE (500hrs/month) | ⭐⭐⭐⭐ | ⭐⭐ Medium | ✅ FREE | Best free option |
| **Render** | FREE | ⭐⭐⭐⭐ | ⭐⭐ Medium | ✅ FREE | Reliable free hosting |
| **Fly.io** | FREE (3 VMs) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ Advanced | ✅ FREE | Power users |
| **Google Cloud Run** | FREE tier | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ Advanced | ✅ FREE | Enterprise-grade |
| **Heroku** | $7/month | ⭐⭐⭐⭐ | ⭐⭐ Medium | ✅ Yes | Simple paid option |
| **DigitalOcean** | $6/month | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ Advanced | ✅ Yes | Full control |

---

## 🆓 FREE & RELIABLE OPTIONS (Recommended)

### **Option 1: Railway.app** ⭐ RECOMMENDED

**What it is:** Modern platform-as-a-service with generous free tier

**Free Tier:**
- 500 hours/month (always-on: 16 days/month)
- $5 credit monthly (enough for 24/7 small apps)
- Custom domains FREE
- Automatic HTTPS
- GitHub auto-deploy

**Setup Steps:**
1. Create account at railway.app
2. Connect GitHub repository
3. Railway auto-detects Python/Streamlit
4. Add custom domain: `booking.creativespark.ie`
5. Done!

**Reliability:** ⭐⭐⭐⭐⭐ (99.9% uptime)

**Why Railway:**
- ✅ Truly free for your use case
- ✅ Custom domain included
- ✅ Auto-deploy on git push
- ✅ Professional infrastructure
- ✅ Easy rollbacks
- ✅ Environment variables secure

**Deployment Time:** 10 minutes

---

### **Option 2: Render.com** 

**What it is:** Developer-friendly hosting platform

**Free Tier:**
- Unlimited apps
- 750 hours/month compute
- Custom domains FREE
- Auto-deploy from GitHub
- Spins down after 15 min inactivity (spins up in ~30 seconds)

**Setup Steps:**
1. Create account at render.com
2. New Web Service → Connect GitHub
3. Select `fablab-booking` repo
4. Runtime: Python 3
5. Start command: `streamlit run streamlit_app.py --server.port=$PORT`
6. Add custom domain

**Reliability:** ⭐⭐⭐⭐ (Excellent, but cold starts)

**Trade-off:** 
- App sleeps after inactivity
- First visit after sleep: 30-60 second load time
- Good for: Regular business hours usage
- Not ideal for: 24/7 instant access

**Deployment Time:** 15 minutes

---

### **Option 3: Fly.io**

**What it is:** Modern app hosting on edge network

**Free Tier:**
- 3 VMs with 256MB RAM each
- 160GB bandwidth/month
- Custom domains FREE
- Global CDN included
- No sleep/cold starts

**Setup Steps:**
1. Install flyctl CLI
2. `fly launch` (auto-detects Streamlit)
3. Deploy with `fly deploy`
4. Add custom domain: `fly certs add booking.creativespark.ie`

**Reliability:** ⭐⭐⭐⭐⭐ (Enterprise-grade)

**Why Fly.io:**
- ✅ No cold starts (always warm)
- ✅ Truly free forever
- ✅ Edge network (fast globally)
- ✅ Professional tool

**Complexity:** Requires CLI usage (more technical)

**Deployment Time:** 20 minutes

---

### **Option 4: Google Cloud Run** 🐳

**What it is:** Serverless container platform (Docker required)

**Free Tier:**
- 2 million requests/month
- 360,000 GB-seconds memory
- 180,000 vCPU-seconds compute
- Custom domains FREE
- Auto-scaling

**Setup:**
1. Create Dockerfile (provided below)
2. Build container: `docker build -t fablab-booking .`
3. Push to Google Container Registry
4. Deploy to Cloud Run
5. Connect custom domain

**Reliability:** ⭐⭐⭐⭐⭐ (Google infrastructure)

**Requirements:**
- Docker installed locally
- Google Cloud account (free tier)
- Basic Docker knowledge

**Monthly Cost:** $0 for your traffic level

**Why Cloud Run:**
- ✅ Scales automatically
- ✅ Pay only for requests (free for low traffic)
- ✅ Google reliability
- ✅ Container portability

**Deployment Time:** 30 minutes

---

## 🐳 DOCKER DEPLOYMENT DETAILS (Option 4)

### **What You Need:**

**1. Dockerfile** (I'll create this for you)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**2. .dockerignore** (exclude unnecessary files)
```
__pycache__/
*.pyc
*.pyo
*.pyd
.git/
.venv/
venv/
```

### **Free Docker Hosting Options:**

#### **A) Google Cloud Run** (Recommended for Docker)
- **Cost:** FREE (under free tier limits)
- **Traffic Limit:** 2 million requests/month (plenty for you)
- **Always Free:** Yes, within limits
- **Setup:**
  ```bash
  gcloud run deploy fablab-booking \
    --source . \
    --platform managed \
    --region europe-west1 \
    --allow-unauthenticated
  ```

#### **B) Fly.io** (Easiest Docker deployment)
- **Cost:** FREE (3 VMs forever)
- **No Credit Card:** Required but not charged
- **Setup:**
  ```bash
  fly launch
  fly deploy
  ```

#### **C) Railway** (Docker support)
- **Cost:** FREE ($5 monthly credit)
- **Build:** Automatic Dockerfile detection
- **Setup:** Connect GitHub → Railway auto-builds Docker

---

## 💰 COMPLETELY FREE (No Credit Card) Options

### **1. Streamlit Cloud** (Current)
- ✅ No credit card
- ✅ Already set up
- ❌ No custom domain on free tier
- ❌ Resource limits

### **2. PythonAnywhere** (Rarely mentioned but viable)
- ✅ No credit card needed
- ✅ Free tier includes web apps
- ✅ Custom domain possible
- ❌ Limited resources (512MB RAM)
- ❌ Manual deployment

### **3. Hugging Face Spaces**
- ✅ No credit card
- ✅ Free Streamlit hosting
- ✅ Good for demos
- ❌ Not ideal for production
- ❌ Limited customization

---

## 🎯 RECOMMENDATION FOR CREATIVE SPARK

### **Best Option: Railway.app**

**Why:**
1. ✅ **Completely FREE** for your usage
2. ✅ **Custom domain included**: `booking.creativespark.ie`
3. ✅ **Reliable**: Professional infrastructure
4. ✅ **Auto-deploy**: Push to GitHub → automatic update
5. ✅ **No cold starts**: Always responsive
6. ✅ **Easy setup**: 10 minutes
7. ✅ **Secure**: Environment variables, HTTPS auto

**Limitations:**
- 500 hours/month OR $5 credit (easily covers 24/7 for small Streamlit app)
- If you exceed: Upgrade for $5/month (unlikely)

### **Setup Process:**
1. Sign up at railway.app with GitHub
2. "New Project" → "Deploy from GitHub repo"
3. Select: `earlyprototype/fablab-booking`
4. Railway auto-detects Python
5. Add start command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
6. Settings → Add custom domain → `booking.creativespark.ie`
7. Update DNS CNAME record
8. Done!

**No cost, reliable, professional. Perfect for Creative Spark.**

---

## 🔄 iFrame Embed (Works with ANY option)

If you want to embed in your existing website:

```html
<!-- Add to your creativespark.ie page -->
<div style="width: 100%; height: 800px;">
    <iframe 
        src="https://booking.creativespark.ie" 
        width="100%" 
        height="100%" 
        frameborder="0"
        style="border: none;">
    </iframe>
</div>
```

Works with current URL or custom domain.

---

## 📝 Next Steps

**To proceed:**
1. ✅ Choose deployment platform (recommend Railway)
2. ✅ Decide on custom domain: `booking.creativespark.ie`?
3. ✅ I can help with setup

**Files ready for deployment:**
- ✅ All code files
- ✅ Requirements.txt
- ✅ Config files
- ✅ Documentation

**Deployment time:** 10-30 minutes depending on option

---

## 🆘 Support

- Railway: https://railway.app/help
- Render: https://render.com/docs
- Fly.io: https://fly.io/docs
- Google Cloud Run: https://cloud.google.com/run/docs

---

**Last Updated:** October 2025
**System Status:** Production Ready ✅

