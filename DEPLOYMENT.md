# Deployment Guide - Railway.app

This guide explains how to deploy the Workout Tracker to Railway using the `dev` branch.

## Prerequisites

- Railway account (https://railway.app)
- GitHub repository connected
- Anthropic API key

## Architecture on Railway

```
Railway Project
├── Backend Service (FastAPI)
│   ├── Branch: dev
│   ├── Root: /backend
│   └── Port: $PORT (auto-assigned)
├── Frontend Service (Next.js)
│   ├── Branch: dev
│   ├── Root: /frontend
│   └── Port: 3000
└── Volume (for JSON data persistence)
    └── Mount: /app/data
```

## Step-by-Step Deployment

### 1. Create New Railway Project

```bash
# Install Railway CLI (optional)
npm i -g @railway/cli

# Login
railway login
```

Or use the web UI: https://railway.app/new

### 2. Deploy Backend Service

**Option A: Using Railway Web UI**

1. Go to Railway Dashboard
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Click "Add Service" → "GitHub Repo"

**Backend Configuration:**
- **Name**: `workout-tracker-backend`
- **Branch**: `dev`
- **Root Directory**: `/backend`
- **Build Command**: Auto-detected from `railway.json`
- **Start Command**: Auto-detected from `Procfile`

**Environment Variables:**
```
ANTHROPIC_API_KEY=sk-ant-xxx...
CLAUDE_MODEL=claude-sonnet-4-20250514
DATA_DIR=/app/data
HOST=0.0.0.0
PORT=${{PORT}}
```

**Volume Setup:**
1. Go to Backend Service → Settings → Volumes
2. Click "New Volume"
3. Mount Path: `/app/data`
4. Size: 1GB (free tier)

### 3. Deploy Frontend Service

**Add another service to the same project:**

1. Click "New Service" in your Railway project
2. Select "GitHub Repo" → Same repository

**Frontend Configuration:**
- **Name**: `workout-tracker-frontend`
- **Branch**: `dev`
- **Root Directory**: `/frontend`
- **Build Command**: Auto-detected from `railway.json`
- **Start Command**: `npm start`

**Environment Variables:**
```
NEXT_PUBLIC_API_URL=${{workout-tracker-backend.RAILWAY_PUBLIC_DOMAIN}}
```

Note: Railway will auto-populate the backend URL reference.

### 4. Generate Public Domains

**Backend:**
1. Go to Backend Service → Settings
2. Click "Generate Domain"
3. Copy the URL (e.g., `https://workout-backend.up.railway.app`)

**Frontend:**
1. Go to Frontend Service → Settings
2. Click "Generate Domain"
3. Copy the URL (e.g., `https://workout-frontend.up.railway.app`)

### 5. Update Frontend Environment

Go back to Frontend Service → Variables:
```
NEXT_PUBLIC_API_URL=https://workout-backend.up.railway.app
```

Save and redeploy if needed.

### 6. Verify Deployment

**Backend:**
```bash
curl https://your-backend.up.railway.app/
# Should return: {"status":"healthy",...}

# Check API docs
open https://your-backend.up.railway.app/docs
```

**Frontend:**
```bash
# Open in browser
open https://your-frontend.up.railway.app
```

## Branch Configuration

Railway is configured to auto-deploy from the `dev` branch:

### Automatic Deployments

Every push to `dev` branch will trigger:
1. Backend rebuild and redeploy
2. Frontend rebuild and redeploy

### Manual Deploy

You can also manually trigger deployment:
1. Go to Service → Deployments
2. Click "Deploy" → Select commit

### Change Branch

To use a different branch:
1. Service → Settings → Source
2. Change "Branch" to your desired branch

## Environment Variables Reference

### Backend
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxx...

# Optional (with defaults)
CLAUDE_MODEL=claude-sonnet-4-20250514
DATA_DIR=/app/data
HOST=0.0.0.0
PORT=${{PORT}}  # Auto-assigned by Railway
```

### Frontend
```bash
# Required
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

## Volume Management

Railway provides persistent storage via Volumes:

### Backup Data

```bash
# Using Railway CLI
railway run --service backend tar -czf backup.tar.gz /app/data
railway run --service backend cat /app/data/logs/2025-01-15.json
```

### Restore Data

```bash
# Upload to volume
railway run --service backend -- sh -c 'cat > /app/data/logs/2025-01-15.json' < local-file.json
```

### Access Logs

```bash
# List all logs
railway run --service backend ls -la /app/data/logs/

# View specific log
railway run --service backend cat /app/data/logs/2025-01-15.json
```

## Monitoring

### View Logs

**Web UI:**
1. Go to Service → Deployments
2. Click on latest deployment
3. View "Deploy Logs" and "Build Logs"

**CLI:**
```bash
# Backend logs
railway logs --service workout-tracker-backend

# Frontend logs
railway logs --service workout-tracker-frontend
```

### Metrics

Railway provides built-in metrics:
1. Service → Metrics
2. View CPU, Memory, Network usage

## Troubleshooting

### Backend Not Starting

**Check logs:**
```bash
railway logs --service workout-tracker-backend
```

**Common issues:**
- Missing `ANTHROPIC_API_KEY`
- Port binding (ensure using `$PORT`)
- Volume not mounted

### Frontend Can't Connect to Backend

**Check:**
1. `NEXT_PUBLIC_API_URL` is correct
2. Backend domain is public
3. CORS settings in `backend/main.py`

**Update CORS if needed:**
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.up.railway.app"  # Add your Railway domain
    ],
    ...
)
```

### Volume Data Lost

Volumes are persistent, but can be lost if:
- Volume is deleted
- Service is redeployed to different region

**Prevention:**
- Regular backups
- Use git to version control important logs
- Enable Railway backups (paid feature)

## Cost Estimation

**Free Tier:**
- $5 credit per month
- Shared CPU
- 512MB RAM per service
- 1GB volume

**Typical Usage:**
- Backend: ~$3-4/month
- Frontend: ~$2-3/month
- Volume: Included in service cost

**Total:** ~$5/month (within free tier)

## CI/CD Setup

### Automatic Deployment on Push

Already configured! Every push to `dev` triggers deployment.

### Manual Deploy Only

To disable auto-deploy:
1. Service → Settings → Source
2. Toggle "Automatic Deployments" OFF

### Deploy Specific Commit

```bash
railway up --service workout-tracker-backend --detach
```

## Custom Domain (Optional)

### Add Custom Domain

1. Service → Settings → Domains
2. Click "Custom Domain"
3. Enter your domain (e.g., `workout.yourdomain.com`)
4. Add CNAME record in your DNS:
   ```
   workout CNAME your-app.up.railway.app
   ```

## Scaling

### Vertical Scaling
1. Service → Settings → Resources
2. Upgrade RAM/CPU (requires paid plan)

### Horizontal Scaling
1. Service → Settings → Replicas
2. Increase replica count (requires paid plan)

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Your repository issues

---

## Quick Reference

```bash
# Deploy to Railway
railway up

# View logs
railway logs

# Open service
railway open

# Run command in service
railway run <command>

# Link to project
railway link
```

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Railway
3. ✅ Configure environment variables
4. ✅ Set up volume for data persistence
5. ✅ Generate public domains
6. ✅ Test the application
7. 🔄 Set up regular backups
8. 🔄 Configure custom domain (optional)

Happy deploying! 🚀
