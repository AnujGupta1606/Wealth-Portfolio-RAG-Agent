import asyncio
import aiomysql
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), index=True, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # BUY, SELL
    stock_symbol = Column(String(20), index=True, nullable=False)
    stock_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    relationship_manager_id = Column(String(20), index=True, nullable=False)
    notes = Column(Text)

class MySQLConnection:
    def __init__(self):
        self.pool = None
        self.engine = None
        self.SessionLocal = None
        
    async def connect(self):
        """Connect to MySQL"""
        try:
            # Create connection pool
            self.pool = await aiomysql.create_pool(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                db=settings.MYSQL_DATABASE,
                autocommit=False,
                minsize=1,
                maxsize=10
            )
            
            # Create SQLAlchemy engine for schema operations
            mysql_url = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
            self.engine = create_engine(mysql_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create tables
            # Base.metadata.create_all(bind=self.engine)  # Commented out - using manual table creation
            
            logger.info("✅ Connected to MySQL")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MySQL: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MySQL"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("🔌 Disconnected from MySQL")
    
    async def health_check(self):
        """Check MySQL health"""
        try:
            if self.pool:
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SELECT 1")
                        result = await cursor.fetchone()
                        if result:
                            return {"status": "healthy", "database": "mysql"}
            return {"status": "disconnected", "database": "mysql"}
        except Exception as e:
            return {"status": "unhealthy", "database": "mysql", "error": str(e)}
    
    async def execute_query(self, query: str, params=None):
        """Execute a query and return results"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    return await cursor.fetchall()
                else:
                    await conn.commit()
                    return cursor.rowcount
    
    async def insert_sample_data(self):
        """Insert sample transaction data"""
        sample_transactions = [
            {
                "client_id": "CL001",
                "transaction_type": "BUY",
                "stock_symbol": "RELIANCE",
                "stock_name": "Reliance Industries",
                "quantity": 10000,
                "price": 2350.50,
                "total_amount": 23505000,
                "transaction_date": "2024-01-15 10:30:00",
                "relationship_manager_id": "RM001",
                "notes": "Large cap investment"
            },
            {
                "client_id": "CL001",
                "transaction_type": "BUY",
                "stock_symbol": "TCS",
                "stock_name": "Tata Consultancy Services",
                "quantity": 5000,
                "price": 3180.75,
                "total_amount": 15903750,
                "transaction_date": "2024-01-20 14:15:00",
                "relationship_manager_id": "RM001",
                "notes": "IT sector diversification"
            },
            {
                "client_id": "CL002",
                "transaction_type": "BUY",
                "stock_symbol": "HDFC",
                "stock_name": "HDFC Bank",
                "quantity": 15000,
                "price": 1485.25,
                "total_amount": 22278750,
                "transaction_date": "2024-02-01 11:00:00",
                "relationship_manager_id": "RM002",
                "notes": "Banking sector exposure"
            },
            {
                "client_id": "CL002",
                "transaction_type": "SELL",
                "stock_symbol": "INFY",
                "stock_name": "Infosys",
                "quantity": 2000,
                "price": 1420.30,
                "total_amount": 2840600,
                "transaction_date": "2024-02-10 16:45:00",
                "relationship_manager_id": "RM002",
                "notes": "Profit booking"
            },
            {
                "client_id": "CL003",
                "transaction_type": "BUY",
                "stock_symbol": "ITC",
                "stock_name": "ITC Limited",
                "quantity": 20000,
                "price": 395.80,
                "total_amount": 7916000,
                "transaction_date": "2024-02-15 09:30:00",
                "relationship_manager_id": "RM001",
                "notes": "Defensive stock for conservative portfolio"
            },
            {
                "client_id": "CL004",
                "transaction_type": "BUY",
                "stock_symbol": "BAJFINANCE",
                "stock_name": "Bajaj Finance",
                "quantity": 3000,
                "price": 6950.40,
                "total_amount": 20851200,
                "transaction_date": "2024-03-01 13:20:00",
                "relationship_manager_id": "RM003",
                "notes": "NBFC sector investment"
            },
            {
                "client_id": "CL005",
                "transaction_type": "BUY",
                "stock_symbol": "ADANIPORTS",
                "stock_name": "Adani Ports",
                "quantity": 25000,
                "price": 785.60,
                "total_amount": 19640000,
                "transaction_date": "2024-03-10 10:15:00",
                "relationship_manager_id": "RM002",
                "notes": "Infrastructure play"
            }
        ]
        
        try:
            # Clear existing data
            await self.execute_query("DELETE FROM transactions")
            
            # Insert new data
            insert_query = """
            INSERT INTO transactions 
            (client_id, transaction_type, stock_symbol, stock_name, quantity, price, total_amount, transaction_date, relationship_manager_id, notes)
            VALUES (%(client_id)s, %(transaction_type)s, %(stock_symbol)s, %(stock_name)s, %(quantity)s, %(price)s, %(total_amount)s, %(transaction_date)s, %(relationship_manager_id)s, %(notes)s)
            """
            
            for transaction in sample_transactions:
                await self.execute_query(insert_query, transaction)
            
            logger.info("✅ Sample transaction data inserted successfully")
        except Exception as e:
            logger.error(f"❌ Failed to insert sample transaction data: {e}")
