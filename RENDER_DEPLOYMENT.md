# 🚀 Render Deployment Guide for Wealth Portfolio RAG Agent

## Prerequisites

Before deploying, ensure you have:

1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **External Databases**: Set up MongoDB Atlas and MySQL on PlanetScale or Render
4. **Cohere API Key**: Get from [dashboard.cohere.ai](https://dashboard.cohere.ai/api-keys)

## 📋 Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [render.com/dashboard](https://render.com/dashboard)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select your repository and branch
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables**
   Set these in Render Dashboard for backend service:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `MYSQL_HOST`: Your MySQL host
   - `MYSQL_USER`: Your MySQL username
   - `MYSQL_PASSWORD`: Your MySQL password
   - `COHERE_API_KEY`: Your Cohere API key
   - `REDIS_URL`: Redis URL (optional)

### Option 2: Manual Deployment

#### Backend Service
1. **Create Web Service**
   - New → Web Service
   - Connect repository
   - Set root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Frontend Service
1. **Create Static Site**
   - New → Static Site
   - Connect repository
   - Set root directory: `frontend`
   - Build command: `npm install && npm run build`
   - Publish directory: `build`

## 🗄️ Database Setup

### MongoDB Atlas
1. Create cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Get connection string
3. Add to `MONGODB_URL` environment variable

### MySQL (PlanetScale Recommended)
1. Create database at [planetscale.com](https://planetscale.com)
2. Get connection details
3. Set MySQL environment variables

### Alternative: Render PostgreSQL
If you prefer PostgreSQL over MySQL:
1. Create PostgreSQL database in Render
2. Update backend code to use PostgreSQL instead of MySQL

## 🔧 Post-Deployment Configuration

### Update Frontend API URL
After backend deployment, update the frontend environment variable:
```
REACT_APP_API_BASE_URL=https://your-backend-service.onrender.com
```

### Initialize Sample Data
After both services are deployed:
1. Go to frontend URL
2. Login with demo credentials
3. Navigate to Data Management
4. Click "Initialize Sample Data"

## 🌐 Access Your Application

- **Frontend**: `https://wealth-portfolio-frontend.onrender.com`
- **Backend API**: `https://wealth-portfolio-backend.onrender.com`
- **API Docs**: `https://wealth-portfolio-backend.onrender.com/docs`

## 🔑 Demo Credentials

- **Admin**: username `admin`, password `admin123`
- **Manager**: username `manager`, password `manager123`
- **Analyst**: username `analyst`, password `analyst123`

## ⚡ Performance Notes

- **Free Tier**: Services may sleep after 15 minutes of inactivity
- **Upgrade**: Consider upgrading to paid plans for production use
- **Cold Starts**: First request after sleep may take 30-60 seconds

## 🔧 Troubleshooting

### Backend Won't Start
- Check environment variables are set correctly
- Verify database connections
- Check logs in Render dashboard

### Frontend Not Connecting to Backend
- Verify `REACT_APP_API_BASE_URL` is set correctly
- Check CORS settings in backend
- Ensure backend is running

### Database Connection Issues
- Verify database URLs and credentials
- Check firewall settings (MongoDB Atlas, PlanetScale)
- Ensure databases allow connections from Render IPs

## 🎯 Production Optimizations

### Security
- Use secure JWT secret keys
- Set up proper CORS origins
- Enable HTTPS only

### Performance
- Consider upgrading to paid Render plans
- Implement Redis caching
- Optimize database queries

### Monitoring
- Set up error tracking (Sentry)
- Monitor API performance
- Set up health checks

## 📞 Support

If you encounter issues:
1. Check Render service logs
2. Verify environment variables
3. Test API endpoints directly
4. Check database connectivity

Your complete Wealth Portfolio RAG Agent with frontend, backend, and databases will be fully functional on Render! 🎉
