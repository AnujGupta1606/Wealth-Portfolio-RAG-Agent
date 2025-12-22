# Wealth Portfolio RAG Agent

A comprehensive Natural Language Cross-Platform Data Query System for wealth portfolio management, specifically designed for high net worth individuals including film stars and sports personalities with 100+ crore investments.

## 🚀 Features

### Core Capabilities
- **Natural Language Processing**: Query complex portfolio data using plain English
- **Multi-Database Integration**: Seamlessly connects MongoDB (client profiles) and MySQL (transactions)
- **AI-Powered Analytics**: LangChain-powered RAG system for intelligent responses
- **Real-time Visualizations**: Interactive charts and graphs using Chart.js
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS

### Business Intelligence Queries
- "What are the top five portfolios of our wealth members?"
- "Give me the breakup of portfolio values per relationship manager."
- "Tell me the top relationship managers in my firm"
- "Which clients are the highest holders of [specific stock]?"
- Risk distribution analysis across portfolios
- Portfolio concentration and diversification metrics

## 🏗️ Architecture

### Backend (Python)
- **FastAPI**: High-performance API framework
- **LangChain**: RAG implementation with Cohere integration
- **MongoDB**: Client profiles and portfolio holdings
- **MySQL**: Transaction data and trading history
- **ChromaDB**: Vector database for domain knowledge
- **Authentication**: JWT-based security system

### Frontend (React TypeScript)
- **React 18**: Modern component-based UI
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Chart.js**: Interactive data visualizations
- **Axios**: API communication
- **React Router**: Navigation and routing

## 📊 Data Model

### MongoDB Collections
```javascript
// clients collection
{
  client_id: "CL001",
  name: "Client Name",
  type: "Film Star" | "Sports Personality",
  risk_appetite: "Conservative" | "Moderate" | "Aggressive",
  total_portfolio_value: 15000000000, // 150 crores
  relationship_manager_id: "RM001",
  // ... other fields
}

// portfolio_holdings collection
{
  client_id: "CL001",
  stock_symbol: "RELIANCE",
  stock_name: "Reliance Industries",
  quantity: 50000,
  current_value: 120000000,
  // ... other fields
}
```

### MySQL Tables
```sql
-- transactions table
CREATE TABLE transactions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  client_id VARCHAR(50) NOT NULL,
  transaction_type VARCHAR(20) NOT NULL, -- BUY/SELL
  stock_symbol VARCHAR(20) NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  total_amount DECIMAL(15,2) NOT NULL,
  transaction_date DATETIME NOT NULL,
  relationship_manager_id VARCHAR(20) NOT NULL
);
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB
- MySQL
- Cohere API Key

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your database URLs and Cohere API key

# Run the application
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Database Setup
```bash
# MongoDB (using Docker)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# MySQL (using Docker)
docker run -d -p 3306:3306 --name mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=wealth_transactions \
  mysql:8.0
```

## 🔐 Authentication

The system includes a simple authentication system with three demo roles:

- **admin/admin123**: Full access to all features
- **manager/manager123**: Portfolio management access
- **analyst/analyst123**: Read-only analytics access

## 🎯 Business Use Cases

### Portfolio Management
- Track and analyze 100+ crore portfolios for celebrities
- Monitor risk distribution across client segments
- Relationship manager performance tracking
- Asset allocation optimization

### Risk Management
- Portfolio concentration analysis
- Risk appetite alignment checking
- Diversification metrics
- Regulatory compliance monitoring

### Client Analytics
- Top performing portfolios identification
- Client segmentation by investment patterns
- Historical performance tracking
- Custom reporting and insights

## 🔮 Advanced Features

### RAG Implementation
- Domain-specific knowledge base in ChromaDB
- Contextual query understanding
- Multi-source data fusion
- Intelligent response generation

### Visualization Engine
- Real-time portfolio charts
- Risk distribution visualizations
- Performance trend analysis
- Interactive dashboards

### Natural Language Processing
- Complex query parsing
- Intent recognition
- Context-aware responses
- Conversational memory

## 🏆 Technical Highlights

### Performance Optimizations
- Async database connections
- Connection pooling
- Efficient query patterns
- Caching strategies

### Security Features
- JWT authentication
- CORS protection
- Input validation
- SQL injection prevention

### Scalability
- Microservices architecture
- Database abstraction layers
- Horizontal scaling support
- Load balancing ready

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production
```bash
# Backend
cd backend
docker build -t wealth-portfolio-backend .

# Frontend
cd frontend
npm run build
```

## 📈 Future Enhancements

### MCP (Model Context Protocol) Integration
- Enhanced context management
- Improved scalability
- Better multi-modal support
- Advanced reasoning capabilities

### Additional Features
- Real-time market data integration
- Automated portfolio rebalancing
- Advanced risk modeling
- Mobile application
- API rate limiting
- Advanced caching
- Multi-tenant support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Screenshots


---

**Built with ❤️ for the wealth management industry**

*Last updated: December 2024*
