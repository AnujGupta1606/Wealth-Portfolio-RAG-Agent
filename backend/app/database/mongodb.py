import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.database = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.database = self.client.get_default_database()
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB")
            
            # Create indexes for better performance
            await self._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("🔌 Disconnected from MongoDB")
    
    async def health_check(self):
        """Check MongoDB health"""
        try:
            if self.client:
                await self.client.admin.command('ping')
                return {"status": "healthy", "database": "mongodb"}
            return {"status": "disconnected", "database": "mongodb"}
        except Exception as e:
            return {"status": "unhealthy", "database": "mongodb", "error": str(e)}
    
    async def _create_indexes(self):
        """Create necessary indexes"""
        try:
            # Client profiles collection
            clients_collection = self.database.clients
            await clients_collection.create_index("client_id", unique=True)
            await clients_collection.create_index("relationship_manager_id")
            await clients_collection.create_index("risk_appetite")
            
            # Portfolio holdings collection
            holdings_collection = self.database.portfolio_holdings
            await holdings_collection.create_index("client_id")
            await holdings_collection.create_index("stock_symbol")
            await holdings_collection.create_index("relationship_manager_id")
            
            logger.info("✅ MongoDB indexes created")
        except Exception as e:
            logger.error(f"❌ Failed to create MongoDB indexes: {e}")
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        if self.database is not None:
            return self.database[collection_name]
        raise ConnectionError("Database not connected")
    
    async def insert_sample_data(self):
        """Insert sample data for testing"""
        clients_data = [
            {
                "client_id": "CL001",
                "name": "Rajesh Kumar",
                "type": "Film Star",
                "address": "Mumbai, Maharashtra",
                "phone": "+91-9876543210",
                "email": "rajesh.kumar@email.com",
                "risk_appetite": "Moderate",
                "investment_preferences": ["Equity", "Mutual Funds", "Gold"],
                "relationship_manager_id": "RM001",
                "relationship_manager_name": "Amit Sharma",
                "total_portfolio_value": 15000000000,  # 150 crores
                "join_date": "2020-01-15"
            },
            {
                "client_id": "CL002", 
                "name": "Priya Singh",
                "type": "Sports Personality",
                "address": "Delhi, India",
                "phone": "+91-9876543211",
                "email": "priya.singh@email.com",
                "risk_appetite": "Aggressive",
                "investment_preferences": ["Equity", "Derivatives", "Real Estate"],
                "relationship_manager_id": "RM002",
                "relationship_manager_name": "Sneha Patel",
                "total_portfolio_value": 20000000000,  # 200 crores
                "join_date": "2019-06-20"
            },
            {
                "client_id": "CL003",
                "name": "Vikram Reddy",
                "type": "Film Star",
                "address": "Hyderabad, Telangana",
                "phone": "+91-9876543212",
                "email": "vikram.reddy@email.com",
                "risk_appetite": "Conservative",
                "investment_preferences": ["Fixed Deposits", "Bonds", "Gold"],
                "relationship_manager_id": "RM001",
                "relationship_manager_name": "Amit Sharma",
                "total_portfolio_value": 12000000000,  # 120 crores
                "join_date": "2021-03-10"
            },
            {
                "client_id": "CL004",
                "name": "Anita Mehta",
                "type": "Sports Personality",
                "address": "Bangalore, Karnataka",
                "phone": "+91-9876543213",
                "email": "anita.mehta@email.com",
                "risk_appetite": "Moderate",
                "investment_preferences": ["Equity", "Mutual Funds"],
                "relationship_manager_id": "RM003",
                "relationship_manager_name": "Rahul Gupta",
                "total_portfolio_value": 18000000000,  # 180 crores
                "join_date": "2020-09-05"
            },
            {
                "client_id": "CL005",
                "name": "Suresh Iyer",
                "type": "Film Star",
                "address": "Chennai, Tamil Nadu",
                "phone": "+91-9876543214",
                "email": "suresh.iyer@email.com",
                "risk_appetite": "Aggressive",
                "investment_preferences": ["Equity", "Crypto", "International Stocks"],
                "relationship_manager_id": "RM002",
                "relationship_manager_name": "Sneha Patel",
                "total_portfolio_value": 25000000000,  # 250 crores
                "join_date": "2018-12-01"
            }
        ]
        
        portfolio_holdings = [
            # Rajesh Kumar's holdings
            {"client_id": "CL001", "stock_symbol": "RELIANCE", "stock_name": "Reliance Industries", "quantity": 50000, "avg_price": 2400, "current_value": 120000000, "relationship_manager_id": "RM001"},
            {"client_id": "CL001", "stock_symbol": "TCS", "stock_name": "Tata Consultancy Services", "quantity": 30000, "avg_price": 3200, "current_value": 96000000, "relationship_manager_id": "RM001"},
            
            # Priya Singh's holdings
            {"client_id": "CL002", "stock_symbol": "HDFC", "stock_name": "HDFC Bank", "quantity": 80000, "avg_price": 1500, "current_value": 120000000, "relationship_manager_id": "RM002"},
            {"client_id": "CL002", "stock_symbol": "INFY", "stock_name": "Infosys", "quantity": 60000, "avg_price": 1400, "current_value": 84000000, "relationship_manager_id": "RM002"},
            
            # Vikram Reddy's holdings
            {"client_id": "CL003", "stock_symbol": "ITC", "stock_name": "ITC Limited", "quantity": 100000, "avg_price": 400, "current_value": 40000000, "relationship_manager_id": "RM001"},
            {"client_id": "CL003", "stock_symbol": "SBIN", "stock_name": "State Bank of India", "quantity": 70000, "avg_price": 500, "current_value": 35000000, "relationship_manager_id": "RM001"},
            
            # Anita Mehta's holdings
            {"client_id": "CL004", "stock_symbol": "WIPRO", "stock_name": "Wipro Limited", "quantity": 90000, "avg_price": 600, "current_value": 54000000, "relationship_manager_id": "RM003"},
            {"client_id": "CL004", "stock_symbol": "BAJFINANCE", "stock_name": "Bajaj Finance", "quantity": 20000, "avg_price": 7000, "current_value": 140000000, "relationship_manager_id": "RM003"},
            
            # Suresh Iyer's holdings
            {"client_id": "CL005", "stock_symbol": "ADANIPORTS", "stock_name": "Adani Ports", "quantity": 150000, "avg_price": 800, "current_value": 120000000, "relationship_manager_id": "RM002"},
            {"client_id": "CL005", "stock_symbol": "ASIANPAINT", "stock_name": "Asian Paints", "quantity": 40000, "avg_price": 3000, "current_value": 120000000, "relationship_manager_id": "RM002"},
        ]
        
        try:
            # Insert clients
            clients_collection = self.get_collection("clients")
            await clients_collection.delete_many({})  # Clear existing data
            await clients_collection.insert_many(clients_data)
            
            # Insert portfolio holdings
            holdings_collection = self.get_collection("portfolio_holdings")
            await holdings_collection.delete_many({})  # Clear existing data
            await holdings_collection.insert_many(portfolio_holdings)
            
            logger.info("✅ Sample data inserted successfully")
        except Exception as e:
            logger.error(f"❌ Failed to insert sample data: {e}")
