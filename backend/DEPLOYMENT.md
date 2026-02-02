# Railway Deployment Guide

## Prerequisites

1. **Neon PostgreSQL Database**
   - Create database at https://neon.tech
   - Copy connection string (starts with `postgresql://`)

2. **Railway Account**
   - Sign up at https://railway.app
   - Connect your GitHub account

## Step 1: Prepare Database

Run these scripts locally BEFORE deploying:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Create auth table
python create_auth_table.py

# Fix tasks table schema
python fix_tasks_schema.py
```

## Step 2: Push to GitHub

```bash
git add .
git commit -m "feat: add Railway deployment configuration"
git push origin main
```

## Step 3: Deploy to Railway

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Click "Add variables" and set:

```
DATABASE_URL=your-neon-postgres-connection-string
FRONTEND_URL=https://your-frontend-url.vercel.app
JWT_SECRET=generate-a-secure-random-string-here
```

5. Railway will auto-detect Python and deploy
6. Your API will be live at: `https://your-project.railway.app`

## Step 4: Generate JWT Secret

Generate a secure random secret:

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or online
# https://www.random.org/strings/
```

## Step 5: Update Frontend

Update your frontend `.env.local`:

```
NEXT_PUBLIC_API_URL=https://your-project.railway.app
```

## Verify Deployment

Test your deployed API:

```bash
# Health check
curl https://your-project.railway.app

# Should return:
# {"status":"ok","message":"Todo Backend API is running"}

# Test signup
curl -X POST https://your-project.railway.app/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test"}'
```

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | ✅ Yes | Neon PostgreSQL connection string | `postgresql://user:pass@host.neon.tech/db` |
| `FRONTEND_URL` | ✅ Yes | Your frontend deployment URL | `https://app.vercel.app` |
| `JWT_SECRET` | ✅ Yes | Secret key for JWT signing | `random-32-char-string` |
| `PORT` | ❌ No | Railway provides automatically | `8000` |

## Troubleshooting

### Database Connection Issues
- Ensure DATABASE_URL includes `?sslmode=require`
- Verify Neon database is active (not paused)

### CORS Errors
- Check FRONTEND_URL matches your actual frontend domain
- Ensure no trailing slash in URL

### Build Failures
- Check Railway build logs
- Verify all dependencies in requirements.txt

### 500 Errors
- Check Railway deployment logs
- Run migrations locally first
- Verify all environment variables are set

## Auto-Deploy

Railway automatically deploys when you push to main branch:

```bash
git add .
git commit -m "update: feature xyz"
git push origin main
# Railway will auto-deploy in ~2 minutes
```

## Local Development

To run locally with production-like environment:

```bash
# Copy production env template
cp .env.production .env

# Update .env with your values
# Then run
uvicorn app.main:app --reload --port 8000
```

## Monitoring

- **Railway Dashboard**: View logs, metrics, and deployments
- **Health Check**: `GET /` endpoint
- **API Docs**: `GET /docs` (Swagger UI)
- **API Schema**: `GET /openapi.json`

## Security Notes

⚠️ **NEVER commit:**
- `.env` files
- Database credentials
- JWT secrets

✅ **Always use:**
- Environment variables
- Railway's secure variable storage
- Strong random JWT secrets (32+ characters)

## Support

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- Neon Docs: https://neon.tech/docs
