"""
Data insertion script to populate MongoDB, MySQL, and ChromaDB with sample data
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.database.mongodb import MongoDBConnection
from app.database.mysql_db import MySQLConnection
from app.database.vector_store import VectorStore
from app.config import settings

# Import sample data
from sample_data.mongodb_data import SAMPLE_CLIENTS, SAMPLE_PORTFOLIO_HOLDINGS
from sample_data.mysql_data import SAMPLE_TRANSACTIONS
from sample_data.vector_data import DOMAIN_KNOWLEDGE

async def insert_mongodb_data():
    """Insert sample data into MongoDB collections"""
    print("🔄 Inserting data into MongoDB...")
    
    mongodb = MongoDBConnection()
    await mongodb.connect()
    
    try:
        # Insert clients
        clients_collection = mongodb.get_collection("clients")
        
        # Clear existing data
        await clients_collection.delete_many({})
        print("  ✅ Cleared existing clients data")
        
        # Insert new clients
        if SAMPLE_CLIENTS:
            result = await clients_collection.insert_many(SAMPLE_CLIENTS)
            print(f"  ✅ Inserted {len(result.inserted_ids)} clients")
        
        # Insert portfolio holdings
        holdings_collection = mongodb.get_collection("portfolio_holdings")
        
        # Clear existing data
        await holdings_collection.delete_many({})
        print("  ✅ Cleared existing portfolio holdings data")
        
        # Insert new holdings
        if SAMPLE_PORTFOLIO_HOLDINGS:
            result = await holdings_collection.insert_many(SAMPLE_PORTFOLIO_HOLDINGS)
            print(f"  ✅ Inserted {len(result.inserted_ids)} portfolio holdings")
            
    except Exception as e:
        print(f"  ❌ Error inserting MongoDB data: {e}")
        raise
    finally:
        await mongodb.disconnect()

async def insert_mysql_data():
    """Insert sample data into MySQL transactions table"""
    print("🔄 Inserting data into MySQL...")
    
    mysql_db = MySQLConnection()
    await mysql_db.connect()
    
    try:
        # Create transactions table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            transaction_id VARCHAR(50) UNIQUE NOT NULL,
            client_id VARCHAR(50) NOT NULL,
            transaction_type ENUM('BUY', 'SELL', 'DIVIDEND', 'INTEREST', 'FEE') NOT NULL,
            asset_type VARCHAR(50) NOT NULL,
            asset_name VARCHAR(200) NOT NULL,
            symbol VARCHAR(50) NOT NULL,
            quantity DECIMAL(15, 2) NOT NULL,
            price_per_unit DECIMAL(15, 2) NOT NULL,
            total_amount DECIMAL(15, 2) NOT NULL,
            fees DECIMAL(15, 2) DEFAULT 0,
            transaction_date DATETIME NOT NULL,
            settlement_date DATETIME,
            broker VARCHAR(100),
            exchange VARCHAR(50),
            status ENUM('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_client_id (client_id),
            INDEX idx_transaction_date (transaction_date),
            INDEX idx_asset_type (asset_type),
            INDEX idx_symbol (symbol)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        await mysql_db.execute_query(create_table_query)
        print("  ✅ Created/verified transactions table")
        
        # Clear existing data
        await mysql_db.execute_query("DELETE FROM transactions")
        print("  ✅ Cleared existing transactions data")
        
        # Insert new transactions
        if SAMPLE_TRANSACTIONS:
            insert_query = """
            INSERT INTO transactions (
                transaction_id, client_id, transaction_type, asset_type, asset_name,
                symbol, quantity, price_per_unit, total_amount, fees,
                transaction_date, settlement_date, broker, exchange, status
            ) VALUES (
                %(transaction_id)s, %(client_id)s, %(transaction_type)s, %(asset_type)s, %(asset_name)s,
                %(symbol)s, %(quantity)s, %(price_per_unit)s, %(total_amount)s, %(fees)s,
                %(transaction_date)s, %(settlement_date)s, %(broker)s, %(exchange)s, %(status)s
            )
            """
            
            for transaction in SAMPLE_TRANSACTIONS:
                await mysql_db.execute_query(insert_query, transaction)
            
            print(f"  ✅ Inserted {len(SAMPLE_TRANSACTIONS)} transactions")
            
    except Exception as e:
        print(f"  ❌ Error inserting MySQL data: {e}")
        raise
    finally:
        await mysql_db.disconnect()

async def insert_vector_data():
    """Insert sample data into ChromaDB vector store"""
    print("🔄 Inserting data into ChromaDB...")
    
    vector_store = VectorStore()
    
    try:
        # Initialize vector store
        await vector_store.initialize()
        
        # Clear existing data
        try:
            vector_store.client.delete_collection("wealth_knowledge")
            print("  ✅ Cleared existing vector data")
        except:
            pass  # Collection might not exist
        
        # Recreate collection
        vector_store.collection = vector_store.client.create_collection(
            name="wealth_knowledge",
            metadata={"description": "Wealth management domain knowledge"}
        )
        
        # Insert domain knowledge
        if DOMAIN_KNOWLEDGE:
            documents = [item["content"] for item in DOMAIN_KNOWLEDGE]
            metadatas = [item["metadata"] for item in DOMAIN_KNOWLEDGE]
            ids = [item["id"] for item in DOMAIN_KNOWLEDGE]
            
            vector_store.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"  ✅ Inserted {len(DOMAIN_KNOWLEDGE)} knowledge documents")
            
    except Exception as e:
        print(f"  ❌ Error inserting vector data: {e}")
        raise

async def verify_data():
    """Verify that data was inserted correctly"""
    print("🔍 Verifying data insertion...")
    
    # Verify MongoDB
    mongodb = MongoDBConnection()
    await mongodb.connect()
    try:
        clients_count = await mongodb.get_collection("clients").count_documents({})
        holdings_count = await mongodb.get_collection("portfolio_holdings").count_documents({})
        print(f"  📊 MongoDB: {clients_count} clients, {holdings_count} holdings")
    finally:
        await mongodb.disconnect()
    
    # Verify MySQL
    mysql_db = MySQLConnection()
    await mysql_db.connect()
    try:
        result = await mysql_db.execute_query("SELECT COUNT(*) as count FROM transactions")
        transactions_count = result[0]['count']
        print(f"  📊 MySQL: {transactions_count} transactions")
    finally:
        await mysql_db.disconnect()
    
    # Verify ChromaDB
    vector_store = VectorStore()
    try:
        await vector_store.initialize()
        vector_count = vector_store.collection.count()
        print(f"  📊 ChromaDB: {vector_count} knowledge documents")
    except Exception as e:
        print(f"  ⚠️ ChromaDB verification failed: {e}")

async def main():
    """Main function to insert all sample data"""
    print("🚀 Starting data insertion process...")
    print(f"Using environment: {settings.ENVIRONMENT}")
    
    try:
        # Insert data into all databases
        await insert_mongodb_data()
        await insert_mysql_data()
        await insert_vector_data()
        
        # Verify data insertion
        await verify_data()
        
        print("✅ Data insertion completed successfully!")
        print("\n📋 Summary:")
        print(f"  • {len(SAMPLE_CLIENTS)} clients inserted into MongoDB")
        print(f"  • {len(SAMPLE_PORTFOLIO_HOLDINGS)} portfolio holdings inserted into MongoDB")
        print(f"  • {len(SAMPLE_TRANSACTIONS)} transactions inserted into MySQL")
        print(f"  • {len(DOMAIN_KNOWLEDGE)} knowledge documents inserted into ChromaDB")
        
        print("\n🎯 Your RAG agent is now ready to answer queries about:")
        print("  • Client portfolios and profiles")
        print("  • Transaction history and analytics")
        print("  • Investment strategies and recommendations")
        print("  • Wealth management best practices")
        
    except Exception as e:
        print(f"❌ Data insertion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
