# Wealth Portfolio RAG Agent - Technical Architecture

## Overview

The Wealth Portfolio RAG Agent is a sophisticated natural language query system designed for high-net-worth portfolio management. It combines cutting-edge AI technology with robust data management to serve the unique needs of managing 100+ crore portfolios for film stars and sports personalities.

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │────│   FastAPI Backend│────│   Data Layer    │
│   (TypeScript)   │    │   (Python)      │    │   (Multi-DB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       ├── MongoDB
         │                       │                       ├── MySQL
         │                       │                       └── ChromaDB
         │                       │
         │              ┌─────────────────┐
         └──────────────│   LangChain RAG │
                        │   (Cohere)      │
                        └─────────────────┘
```

### Component Details

#### Frontend Layer (React TypeScript)
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS for responsive design
- **Charts**: Chart.js for data visualizations
- **Routing**: React Router for navigation
- **State Management**: Context API for authentication
- **API Client**: Axios for HTTP requests

#### Backend Layer (FastAPI Python)
- **API Framework**: FastAPI for high-performance REST APIs
- **Authentication**: JWT-based security system
- **LangChain Integration**: RAG implementation with Cohere
- **Database Abstraction**: Async drivers for multi-database support
- **Middleware**: CORS, logging, error handling

#### Data Layer
1. **MongoDB**: Client profiles and portfolio holdings
2. **MySQL**: Transaction history and trading data
3. **ChromaDB**: Vector database for domain knowledge

#### AI/ML Layer
- **LangChain**: Orchestrates the RAG pipeline
- **Cohere Command-R-Plus**: Large language model for query processing
- **Sentence Transformers**: Embedding generation
- **ChromaDB**: Vector storage and similarity search

## Data Flow

### Query Processing Pipeline

```
User Query → Frontend → Backend API → LangChain Agent
                                           │
                                           ├── Vector Search (ChromaDB)
                                           ├── MongoDB Query (Client Data)
                                           ├── MySQL Query (Transactions)
                                           └── Response Generation (Cohere)
                                                     │
Response ← Frontend ← Backend API ← Formatted Response
```

### Authentication Flow

```
Login Request → Backend Auth → JWT Generation → Frontend Storage
                   │
                   └── Role-based Access Control
                       ├── Admin (Full Access)
                       ├── Manager (Portfolio Management)
                       └── Analyst (Read-only)
```

## Database Schema Design

### MongoDB Collections

#### clients Collection
```javascript
{
  _id: ObjectId,
  client_id: "CL001",
  name: "Client Name",
  type: "Film Star" | "Sports Personality",
  address: "Complete Address",
  phone: "+91-XXXXXXXXXX",
  email: "client@email.com",
  risk_appetite: "Conservative" | "Moderate" | "Aggressive",
  investment_preferences: ["Equity", "Mutual Funds", "Gold"],
  relationship_manager_id: "RM001",
  relationship_manager_name: "Manager Name",
  total_portfolio_value: 15000000000, // 150 crores
  join_date: "2020-01-15",
  created_at: Date,
  updated_at: Date
}
```

#### portfolio_holdings Collection
```javascript
{
  _id: ObjectId,
  client_id: "CL001",
  stock_symbol: "RELIANCE",
  stock_name: "Reliance Industries",
  quantity: 50000,
  avg_price: 2400,
  current_value: 120000000,
  relationship_manager_id: "RM001",
  sector: "Energy",
  created_at: Date,
  updated_at: Date
}
```

### MySQL Tables

#### transactions Table
```sql
CREATE TABLE transactions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  client_id VARCHAR(50) NOT NULL,
  transaction_type ENUM('BUY', 'SELL') NOT NULL,
  stock_symbol VARCHAR(20) NOT NULL,
  stock_name VARCHAR(100) NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  total_amount DECIMAL(15,2) NOT NULL,
  transaction_date DATETIME NOT NULL,
  relationship_manager_id VARCHAR(20) NOT NULL,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_client_id (client_id),
  INDEX idx_stock_symbol (stock_symbol),
  INDEX idx_transaction_date (transaction_date),
  INDEX idx_rm_id (relationship_manager_id)
);
```

### ChromaDB Collections

#### wealth_portfolio_knowledge
- **Domain Knowledge**: Wealth management concepts, regulations, best practices
- **Query Examples**: Sample questions and expected patterns
- **Business Rules**: Investment guidelines and risk management principles

## RAG Implementation

### Knowledge Base Components

1. **Domain Expertise**
   - Wealth management principles
   - Risk assessment frameworks
   - Investment strategies
   - Regulatory compliance

2. **Business Context**
   - Client profiling methodologies
   - Portfolio construction guidelines
   - Performance measurement standards
   - Relationship management best practices

3. **Query Patterns**
   - Common business questions
   - Expected response formats
   - Context understanding examples

### LangChain Pipeline

```python
# Simplified RAG Pipeline
Query → Embedding → Vector Search → Context Retrieval
  ↓
Database Queries → Data Aggregation → Response Generation
  ↓
Formatted Response + Charts → Frontend Display
```

## Security Architecture

### Authentication & Authorization
- **JWT Tokens**: Secure session management
- **Role-based Access**: Admin, Manager, Analyst roles
- **API Security**: Protected endpoints with middleware
- **CORS Protection**: Configurable cross-origin requests

### Data Security
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: Parameterized queries
- **Connection Security**: Encrypted database connections
- **Environment Variables**: Secure credential management

## Performance Optimizations

### Database Performance
- **Connection Pooling**: Efficient connection management
- **Indexing Strategy**: Optimized database indexes
- **Query Optimization**: Efficient aggregation pipelines
- **Caching Layer**: Redis for frequent queries (future enhancement)

### API Performance
- **Async Operations**: Non-blocking database operations
- **Response Compression**: Gzip compression for large responses
- **Pagination**: Efficient data loading for large datasets
- **Background Tasks**: Celery for heavy computations (future)

### Frontend Performance
- **Code Splitting**: Lazy loading of components
- **Memoization**: React.memo for expensive components
- **Virtual Scrolling**: Efficient rendering of large lists
- **Image Optimization**: Compressed assets

## Deployment Architecture

### Development Environment
```
Local Machine
├── Frontend (localhost:3000)
├── Backend (localhost:8000)
├── MongoDB (localhost:27017)
├── MySQL (localhost:3306)
└── ChromaDB (local file system)
```

### Production Environment (Recommended)
```
Cloud Infrastructure
├── Load Balancer
├── Frontend (CDN + Static Hosting)
├── Backend (Container Orchestration)
├── Database Cluster
│   ├── MongoDB Atlas
│   ├── MySQL Cloud
│   └── ChromaDB Persistent Storage
└── Monitoring & Logging
```

## Scalability Considerations

### Horizontal Scaling
- **Microservices**: Decompose backend into specialized services
- **Database Sharding**: Distribute data across multiple instances
- **Load Balancing**: Multiple backend instances
- **CDN Integration**: Global content delivery

### Vertical Scaling
- **Resource Optimization**: CPU and memory tuning
- **Database Indexing**: Query performance optimization
- **Caching Strategies**: Multiple cache layers
- **Connection Pooling**: Efficient resource utilization

## Future Enhancements

### MCP (Model Context Protocol) Integration
- **Enhanced Context Management**: Better conversation memory
- **Multi-modal Support**: Handle text, images, and documents
- **Advanced Reasoning**: Complex multi-step analysis
- **Scalable Architecture**: Distributed context management

### Advanced Features
- **Real-time Data**: Live market data integration
- **Automated Insights**: Proactive portfolio alerts
- **Mobile Application**: React Native companion app
- **Advanced Analytics**: ML-powered predictions
- **Compliance Automation**: Regulatory reporting

### Technical Improvements
- **GraphQL API**: Flexible query interface
- **Event Sourcing**: Audit trail and versioning
- **CQRS Pattern**: Separate read/write operations
- **Microservices**: Service decomposition
- **Kubernetes**: Container orchestration

## Monitoring & Observability

### Application Monitoring
- **Health Checks**: Endpoint monitoring
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Exception monitoring
- **User Analytics**: Usage patterns

### Infrastructure Monitoring
- **Resource Utilization**: CPU, memory, disk
- **Database Performance**: Query performance
- **Network Monitoring**: Latency and throughput
- **Security Monitoring**: Access patterns and threats

## Development Workflow

### Code Quality
- **Type Safety**: TypeScript for frontend, Pydantic for backend
- **Testing**: Unit tests, integration tests, E2E tests
- **Code Review**: Pull request workflows
- **Linting**: ESLint, Prettier, Black, isort

### CI/CD Pipeline
- **Automated Testing**: Run tests on every commit
- **Code Quality Checks**: Linting and type checking
- **Security Scanning**: Dependency vulnerability checks
- **Deployment Automation**: Automated deployment to staging/production

This architecture provides a solid foundation for a production-ready wealth portfolio management system while maintaining flexibility for future enhancements and scalability requirements.
