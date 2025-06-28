# Quick Start Guide - Wealth Portfolio RAG Agent

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
```bash
python3 --version  # Should be 3.8+
node --version     # Should be 16+
```

### 1. Clone & Setup
```bash
# If you haven't already cloned the project
git clone <repository-url>
cd Wizizard

# Run automated setup
./setup.sh
```

### 2. Start Databases (using Docker)
```bash
# MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:latest

# MySQL
docker run -d -p 3306:3306 --name mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=wealth_transactions \
  mysql:8.0
```

### 3. Configure Environment
```bash
# Edit backend/.env with your settings
cd backend
cp .env.example .env
nano .env  # Add your Cohere API key
```

### 4. Start the Application

#### Option A: Manual Start (Recommended for development)
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm start
```

#### Option B: VS Code Tasks
- Open VS Code
- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
- Type "Tasks: Run Task"
- Select "Start Full Application"

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

### 6. Demo Login
Use these credentials to explore:
- **Admin**: `admin` / `admin123`
- **Manager**: `manager` / `manager123`  
- **Analyst**: `analyst` / `analyst123`

### 7. Initialize Sample Data
1. Login to the application
2. Go to "Data Management" tab
3. Click "Initialize Sample Data"
4. Wait for confirmation

### 8. Try Sample Queries
Go to "Query Interface" and try:
- "What are the top five portfolios of our wealth members?"
- "Give me the breakup of portfolio values per relationship manager"
- "Which clients are the highest holders of RELIANCE stock?"

## 🛠️ Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check if virtual environment is activated
which python  # Should show path to venv

# Install dependencies again
pip install -r requirements.txt

# Check environment variables
cat .env
```

#### Frontend won't start
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Database connection issues
```bash
# Check if containers are running
docker ps

# Restart containers
docker restart mongodb mysql
```

#### Missing Cohere API Key
1. Get API key from https://dashboard.cohere.ai/api-keys
2. Add to `backend/.env`: `COHERE_API_KEY=your_key_here`
3. Restart backend server

### Port Conflicts
If ports 3000 or 8000 are busy:
```bash
# Kill processes on ports
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

## 📱 Features to Explore

### 1. Dashboard
- Portfolio overview with charts
- Key performance metrics
- Risk distribution analysis

### 2. Query Interface
- Natural language queries
- Interactive charts in responses
- Conversation history

### 3. Analytics
- Top performers analysis
- Relationship manager performance
- Stock concentration analysis

### 4. Data Management
- Database health monitoring
- Sample data initialization
- Data export capabilities

## 🔧 Development Mode

### Hot Reload
Both frontend and backend support hot reload:
- Frontend: Changes auto-refresh browser
- Backend: API restarts on code changes

### Debug Mode
```bash
# Backend with debug logging
cd backend
python -m uvicorn app.main:app --reload --log-level debug

# Frontend with debug info
cd frontend
REACT_APP_DEBUG=true npm start
```

### Database Tools
```bash
# MongoDB shell
docker exec -it mongodb mongosh

# MySQL shell  
docker exec -it mysql mysql -u root -p wealth_transactions
```

## 📊 Sample Data Overview

The system includes realistic sample data:
- **5 Clients**: Mix of film stars and sports personalities
- **10+ Stock Holdings**: Major Indian stocks (RELIANCE, TCS, HDFC, etc.)
- **Transaction History**: Buy/sell transactions with dates
- **3 Relationship Managers**: With different client portfolios

## 🎯 Next Steps

1. **Customize Data**: Add your own client profiles and holdings
2. **Extend Queries**: Add more complex business logic
3. **Add Features**: Implement additional analytics
4. **Deploy**: Use the deployment guide for production

## 📞 Support

- Check `README.md` for detailed documentation
- Review `docs/ARCHITECTURE.md` for technical details
- Create issues for bugs or feature requests

---
**Happy coding! 🚀**
