# 🚂 Railway Deployment Instructions

**Important:** This is a monorepo. You need to deploy Backend and Frontend as **separate services**.

## ⚠️ Common Issue: "Script start.sh not found"

This error happens when Railway tries to deploy the entire repository as one service.

**Solution:** Deploy Backend and Frontend separately with correct Root Directory settings.

---

## 📋 Step-by-Step Deployment

### Step 1: Create Railway Project

1. Go to **https://railway.app/new**
2. Click **"Empty Project"** (NOT "Deploy from GitHub repo")
3. Name it: `Workout Tracker`

### Step 2: Deploy Backend

1. In your project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose your repository: `Exercise-tracking`
4. **Configure the service:**

   **Settings → Service:**
   - Name: `backend`

   **Settings → Source:**
   - Branch: `dev`
   - **Root Directory: `/backend`** ⚠️ **CRITICAL**

   **Variables:**
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   CLAUDE_MODEL=claude-sonnet-4-20250514
   DATA_DIR=/app/data
   ```

5. **Add Volume for Data Storage:**
   - Settings → Volumes
   - Click "New Volume"
   - Mount Path: `/app/data`
   - Size: 1GB

6. **Generate Domain:**
   - Settings → Networking
   - Click "Generate Domain"
   - Copy the URL (e.g., `https://backend-production-xxxx.up.railway.app`)

### Step 3: Deploy Frontend

1. In same project, click **"+ New"** again
2. Select **"GitHub Repo"**
3. Choose same repository: `Exercise-tracking`
4. **Configure the service:**

   **Settings → Service:**
   - Name: `frontend`

   **Settings → Source:**
   - Branch: `dev`
   - **Root Directory: `/frontend`** ⚠️ **CRITICAL**

   **Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.up.railway.app
   ```
   *(Use the backend URL from Step 2.6)*

5. **Generate Domain:**
   - Settings → Networking
   - Click "Generate Domain"
   - Copy the URL (e.g., `https://frontend-production-xxxx.up.railway.app`)

### Step 4: Update Backend CORS (if needed)

If you get CORS errors, add the frontend URL to backend environment:

**Backend Variables:**
```
FRONTEND_URL=https://your-frontend-url.up.railway.app
```

Then redeploy backend (it will auto-update CORS).

---

## ✅ Verify Deployment

### Test Backend
```bash
curl https://your-backend.up.railway.app/
# Should return: {"status":"healthy",...}
```

**API Docs:**
```
https://your-backend.up.railway.app/docs
```

### Test Frontend
Open in browser:
```
https://your-frontend.up.railway.app/
```

---

## 🔧 Configuration Files Explained

### Root: `railway.toml`
- Tells Railway this is a monorepo
- Not used for actual deployment

### Backend: `backend/nixpacks.toml`
- Specifies Python 3.11
- Install command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend: `frontend/nixpacks.toml`
- Specifies Node.js 20
- Install: `npm install`
- Build: `npm run build`
- Start: `npm start`

---

## 🔄 Auto-Deploy

Once set up, every push to `dev` branch will automatically trigger:
- ✅ Backend rebuild and redeploy
- ✅ Frontend rebuild and redeploy

```bash
git checkout dev
git add .
git commit -m "Update features"
git push origin dev
# 🚀 Railway auto-deploys both services!
```

---

## 📊 Project Structure in Railway

```
Workout Tracker Project
├── backend (Service)
│   ├── Root: /backend
│   ├── Branch: dev
│   ├── Build: nixpacks.toml
│   ├── Volume: /app/data
│   └── Domain: backend-xxx.up.railway.app
│
└── frontend (Service)
    ├── Root: /frontend
    ├── Branch: dev
    ├── Build: nixpacks.toml
    └── Domain: frontend-xxx.up.railway.app
```

---

## ❓ Troubleshooting

### "Script start.sh not found"
**Problem:** Railway is trying to build from root directory

**Solution:**
1. Delete the failed service
2. Create new service with **Root Directory** set correctly:
   - Backend: `/backend`
   - Frontend: `/frontend`

### Build fails with "No package.json found" (Frontend)
**Problem:** Root directory not set

**Solution:** Settings → Source → Root Directory: `/frontend`

### Build fails with "No requirements.txt found" (Backend)
**Problem:** Root directory not set

**Solution:** Settings → Source → Root Directory: `/backend`

### Frontend can't connect to Backend
**Problem:** API URL not set or incorrect

**Solution:**
1. Check backend domain is generated
2. Update frontend env: `NEXT_PUBLIC_API_URL=https://backend-xxx.up.railway.app`
3. Redeploy frontend

### CORS errors
**Problem:** Backend doesn't allow frontend domain

**Solution:** Already handled! Backend auto-detects Railway domains. If still failing:
1. Add to backend env: `FRONTEND_URL=https://frontend-xxx.up.railway.app`
2. Redeploy backend

### Data not persisting
**Problem:** Volume not mounted

**Solution:**
1. Backend → Settings → Volumes
2. Create volume with mount path: `/app/data`
3. Redeploy

---

## 💰 Cost

**Free Tier:**
- $5 credit per month
- Enough for this MVP (~500 hours)
- Both services combined: ~$5/month

**What's included:**
- ✅ Auto-deploy
- ✅ Persistent storage (1GB)
- ✅ Custom domains
- ✅ HTTPS
- ✅ Monitoring

---

## 🎯 Summary Checklist

- [ ] Create empty Railway project
- [ ] Deploy backend with Root Directory: `/backend`
- [ ] Add backend environment variables
- [ ] Create volume for `/app/data`
- [ ] Generate backend domain
- [ ] Deploy frontend with Root Directory: `/frontend`
- [ ] Add frontend environment variable (backend URL)
- [ ] Generate frontend domain
- [ ] Test both services
- [ ] Verify auto-deploy works

---

**Need help?** Check `DEPLOYMENT.md` for full details.

**Ready to deploy?** Start with Step 1! 🚀
