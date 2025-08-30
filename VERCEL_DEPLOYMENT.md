# Vercel Deployment Guide

## 🚨 Current Issues

Your Flask app **WILL NOT work on Vercel** without changes:

- ❌ SQLite database (Vercel has read-only filesystem)
- ❌ Local file uploads (no persistent storage)
- ❌ Hardcoded configuration

## 🔧 Required Changes

### 1. Database
Replace SQLite with PostgreSQL:
```python
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### 2. File Storage
Use cloud storage (AWS S3, Cloudinary):
```python
# Instead of local saves
# Use cloud storage API
```

### 3. Environment Variables
Set in Vercel dashboard:
```bash
SECRET_KEY=your-secret
DATABASE_URL=postgresql://...
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
```

## 🚀 Quick Fix Options

### Option 1: Use Railway/Render
- ✅ Supports SQLite
- ✅ Supports file uploads
- ✅ Works with current code

### Option 2: Migrate to Vercel
- ⏱️ 7-10 hours of work
- 💰 Free hosting
- ❌ Requires database migration

## 📁 Vercel Files Created

- `vercel.json` - Vercel configuration
- `config_vercel.py` - Environment-based config
- `requirements_vercel.txt` - Vercel dependencies

## 🎯 Recommendation

**Don't deploy to Vercel yet!** Use Railway or Render instead for now.
