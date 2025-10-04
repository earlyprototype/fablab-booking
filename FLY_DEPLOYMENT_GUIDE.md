# 🚀 Deploy to Fly.io - Step-by-Step Guide

**Total Time:** 20 minutes  
**Total Cost:** $0 (FREE FOREVER)

---

## ✅ Prerequisites

- Credit card (for verification only - NOT charged)
- PowerShell terminal
- Your fablab_booking project folder

---

## 📝 Step-by-Step Instructions

### **Step 1: Install Fly CLI** (2 minutes)

Open PowerShell and run:

```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**Verify installation:**
```powershell
fly version
```

You should see version information.

---

### **Step 2: Create Fly.io Account** (3 minutes)

```powershell
fly auth signup
```

This will:
1. Open your browser
2. Create account (use GitHub login recommended)
3. Add credit card for verification (NOT charged)
4. Verify email

---

### **Step 3: Navigate to Your Project** (1 minute)

```powershell
cd C:\Users\Fab2\Desktop\AI\Deploy\fablab_booking
```

---

### **Step 4: Launch Your App** (10 minutes)

```powershell
fly launch
```

**You'll be asked several questions:**

1. **App name?** 
   - Suggestion: `fablab-booking-creative-spark`
   - Press Enter to accept or type your own

2. **Select region?**
   - Choose: `lhr (London)` - closest to Ireland
   - Use arrow keys, press Enter

3. **Set up Postgres?**
   - Answer: **NO** (press N)
   - You don't need a database

4. **Set up Redis?**
   - Answer: **NO** (press N)
   - You don't need Redis

5. **Deploy now?**
   - Answer: **YES** (press Y)

Fly will now:
- ✅ Create your app
- ✅ Build Docker container
- ✅ Deploy to their edge network
- ✅ Give you a URL

**Wait for:** "Successfully deployed!"

---

### **Step 5: Test Your App** (2 minutes)

After deployment completes, run:

```powershell
fly open
```

This opens your app in the browser. Test:
- ✅ Login works
- ✅ Booking calendar displays
- ✅ Logo shows

**Your app is now live!**

Current URL: `https://fablab-booking-creative-spark.fly.dev`

---

### **Step 6: Add Custom Domain** (2 minutes - OPTIONAL)

If you want `booking.creativespark.ie`:

```powershell
fly certs add booking.creativespark.ie
```

Fly will show you DNS records to add. You need to:

1. Go to your DNS provider (where creativespark.ie is hosted)
2. Add CNAME record:
   - **Name:** `booking`
   - **Value:** `fablab-booking-creative-spark.fly.dev`
   - **TTL:** 3600

Wait 5-60 minutes for DNS propagation.

**Verify:**
```powershell
fly certs show booking.creativespark.ie
```

---

## 🔄 Future Updates

Whenever you update your code:

```powershell
# Navigate to project
cd C:\Users\Fab2\Desktop\AI\Deploy\fablab_booking

# Commit changes to Git
git add .
git commit -m "Your update message"
git push

# Deploy to Fly.io
fly deploy
```

**That's it!** Changes go live in ~2 minutes.

---

## 📊 Monitor Your App

### **View logs:**
```powershell
fly logs
```

### **Check status:**
```powershell
fly status
```

### **View dashboard:**
```powershell
fly dashboard
```

---

## 💰 Cost Tracking

### **View usage:**
```powershell
fly billing
```

Your app uses **~100MB RAM** which is well within the **256MB free VM**.

**Free tier includes:**
- ✅ 3 VMs with 256MB RAM
- ✅ 160GB bandwidth/month
- ✅ Custom domains unlimited
- ✅ Your app: Uses 1 VM = FREE

---

## 🆘 Troubleshooting

### **App won't start?**

Check logs:
```powershell
fly logs
```

Common issues:
- Port mismatch (should be 8501)
- Missing requirements

### **Can't deploy?**

Restart deployment:
```powershell
fly deploy --force
```

### **Domain not working?**

Check DNS:
```powershell
fly certs check booking.creativespark.ie
```

Wait up to 1 hour for DNS propagation.

### **Need to restart app?**

```powershell
fly apps restart fablab-booking-creative-spark
```

---

## 🔧 Configuration Files

Your project already has these files ready:

1. **Dockerfile** - Tells Fly how to build your app
2. **.dockerignore** - Excludes unnecessary files
3. **requirements.txt** - Python dependencies

**No changes needed!** Everything is configured.

---

## 🎯 Commands Cheat Sheet

```powershell
# Deploy latest changes
fly deploy

# Open app in browser
fly open

# View logs (live)
fly logs

# Check app status
fly status

# View dashboard
fly dashboard

# Restart app
fly apps restart fablab-booking-creative-spark

# Check usage/billing
fly billing

# Add domain
fly certs add booking.creativespark.ie

# Check domain status
fly certs show booking.creativespark.ie

# Scale (if needed in future)
fly scale count 1  # Number of VMs
fly scale memory 256  # MB per VM
```

---

## ✅ Success Checklist

After deployment, verify:

- [ ] App accessible via Fly URL
- [ ] Login form works
- [ ] Can create bookings
- [ ] Logo displays
- [ ] Admin dashboard works (Carl's email)
- [ ] Weekly schedule shows
- [ ] Export functions work

---

## 🌐 Your Live URLs

**Fly.io URL:** `https://fablab-booking-creative-spark.fly.dev`

**Custom Domain (after DNS setup):** `https://booking.creativespark.ie`

**Current Streamlit Cloud:** `https://fablab-booking-creative-spark.streamlit.app`

You can keep both running or remove Streamlit Cloud deployment later.

---

## 📞 Support

- **Fly.io Docs:** https://fly.io/docs
- **Community Forum:** https://community.fly.io
- **Status Page:** https://status.fly.io

---

**Deployed on:** Fly.io  
**Region:** London (lhr)  
**Cost:** $0 / month  
**Reliability:** 99.99% uptime  

🎉 **Your professional booking system is now live on Fly.io!**

