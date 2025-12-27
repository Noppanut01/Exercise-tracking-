# Railway Quick Setup Guide

Quick reference for deploying to Railway on the `dev` branch.

## 🚀 One-Click Setup

1. **Push to `dev` branch:**
   ```bash
   git checkout -b dev  # Create dev branch if doesn't exist
   git push -u origin dev
   ```

2. **Create Railway Project:**
   - Go to https://railway.app/new
   - Click "Deploy from GitHub repo"
   - Select this repository
   - Branch: **dev** (Railway will auto-detect from configs)

3. **Deploy Backend:**
   - Railway will auto-detect `backend/` service
   - Add environment variables:
     ```
     ANTHROPIC_API_KEY=your_key_here
     CLAUDE_MODEL=claude-sonnet-4-20250514
     DATA_DIR=/app/data
     ```
   - Add Volume: Mount `/app/data` (1GB)
   - Generate Domain

4. **Deploy Frontend:**
   - Railway will auto-detect `frontend/` service
   - Add environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
     ```
   - Generate Domain

## 📁 Files Created

```
✅ railway.json                 - Root config
✅ .railway                     - Service detection (branch: dev)
✅ backend/railway.json         - Backend config
✅ backend/Procfile             - Start command
✅ backend/runtime.txt          - Python version
✅ frontend/railway.json        - Frontend config
✅ DEPLOYMENT.md                - Full deployment guide
✅ backend/main.py              - Updated CORS for Railway
```

## ⚙️ Environment Variables

### Backend
| Variable | Value | Required |
|----------|-------|----------|
| `ANTHROPIC_API_KEY` | Your Claude API key | ✅ Yes |
| `CLAUDE_MODEL` | claude-sonnet-4-20250514 | ⚠️ Optional |
| `DATA_DIR` | /app/data | ⚠️ Optional |
| `PORT` | Auto (Railway sets) | ✅ Auto |

### Frontend
| Variable | Value | Required |
|----------|-------|----------|
| `NEXT_PUBLIC_API_URL` | Backend Railway URL | ✅ Yes |

## 🔄 Auto-Deploy

Every push to `dev` branch triggers automatic deployment:

```bash
git checkout dev
git add .
git commit -m "Update feature"
git push origin dev
# 🚀 Railway auto-deploys!
```

## 💾 Data Persistence

**Important:** Add a Volume to backend service:
- Path: `/app/data`
- Size: 1GB (free tier)
- This stores your JSON workout logs

## 🧪 Test Deployment

```bash
# Health check
curl https://your-backend.up.railway.app/

# API docs
open https://your-backend.up.railway.app/docs

# Frontend
open https://your-frontend.up.railway.app/
```

## 📊 Cost

Free tier includes:
- $5/month credit
- Enough for this MVP
- ~500 hours of usage

## ❓ Troubleshooting

**Backend not starting?**
- Check logs in Railway dashboard
- Verify `ANTHROPIC_API_KEY` is set
- Ensure volume is mounted

**Frontend can't connect?**
- Check `NEXT_PUBLIC_API_URL` in frontend env vars
- Verify backend domain is public
- Check CORS settings (already configured)

**Need help?**
See full guide: `DEPLOYMENT.md`

---

**Ready to deploy? Push to `dev` and connect to Railway!** 🎉
