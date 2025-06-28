"""
Enhanced data insertion script to populate MongoDB, MySQL, and ChromaDB with hundreds of records
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database.mongodb import MongoDBConnection
from app.database.mysql_db import MySQLConnection
from app.database.vector_store import VectorStore
from app.config import settings

# Import enhanced sample data
from sample_data.mongodb_data_enhanced import generate_client_data, generate_portfolio_holdings
from sample_data.mysql_data_enhanced import generate_enhanced_transactions
from sample_data.vector_data import DOMAIN_KNOWLEDGE

async def insert_mongodb_data():
    """Insert enhanced sample data into MongoDB collections"""
    print("🔄 Inserting enhanced data into MongoDB...")
    
    mongodb = MongoDBConnection()
    await mongodb.connect()
    
    try:
        # Generate enhanced data
        print("  🔄 Generating 200+ clients...")
        clients = generate_client_data(count=200)
        
        print("  🔄 Generating 500+ portfolio holdings...")
        holdings = generate_portfolio_holdings(client_count=200)
        
        # Insert clients
        clients_collection = mongodb.get_collection("clients")
        
        # Clear existing data
        await clients_collection.delete_many({})
        print("  ✅ Cleared existing clients data")
        
        # Insert new clients
        if clients:
            result = await clients_collection.insert_many(clients)
            print(f"  ✅ Inserted {len(result.inserted_ids)} clients")
        
        # Insert portfolio holdings
        holdings_collection = mongodb.get_collection("portfolio_holdings")
        
        # Clear existing data
        await holdings_collection.delete_many({})
        print("  ✅ Cleared existing portfolio holdings data")
        
        # Insert new holdings
        if holdings:
            result = await holdings_collection.insert_many(holdings)
            print(f"  ✅ Inserted {len(result.inserted_ids)} portfolio holdings")
            
    except Exception as e:
        print(f"  ❌ Error inserting MongoDB data: {e}")
        raise
    finally:
        await mongodb.disconnect()

async def insert_mysql_data():
    """Insert enhanced sample data into MySQL transactions table"""
    print("🔄 Inserting enhanced data into MySQL...")
    
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
            quantity DECIMAL(20, 6) NOT NULL,
            price_per_unit DECIMAL(20, 6) NOT NULL,
            total_amount DECIMAL(20, 6) NOT NULL,
            fees DECIMAL(20, 6) DEFAULT 0,
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
        
        # Generate enhanced transactions
        print("  🔄 Generating 2000+ transactions...")
        transactions = generate_enhanced_transactions(num_clients=200)
        
        # Insert new transactions in batches
        if transactions:
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
            
            # Insert in batches of 100 to avoid memory issues
            batch_size = 100
            total_inserted = 0
            
            for i in range(0, len(transactions), batch_size):
                batch = transactions[i:i + batch_size]
                for transaction in batch:
                    await mysql_db.execute_query(insert_query, transaction)
                total_inserted += len(batch)
                print(f"  📝 Inserted {total_inserted}/{len(transactions)} transactions")
            
            print(f"  ✅ Inserted {len(transactions)} transactions")
            
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
        
        # The vector store is already initialized with domain knowledge
        # in the initialize method if the collection is empty
        print(f"  ✅ Vector store ready with domain knowledge")
            
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
        
        # Sample data verification
        sample_client = await mongodb.get_collection("clients").find_one({})
        if sample_client:
            print(f"  👤 Sample client: {sample_client.get('name', 'N/A')} ({sample_client.get('profession', 'N/A')})")
        
    finally:
        await mongodb.disconnect()
    
    # Verify MySQL
    mysql_db = MySQLConnection()
    await mysql_db.connect()
    try:
        result = await mysql_db.execute_query("SELECT COUNT(*) as count FROM transactions")
        transactions_count = result[0]['count']
        print(f"  📊 MySQL: {transactions_count} transactions")
        
        # Sample transaction verification
        sample_txn = await mysql_db.execute_query("SELECT * FROM transactions LIMIT 1")
        if sample_txn:
            txn = sample_txn[0]
            print(f"  💰 Sample transaction: {txn['asset_name']} - {txn['transaction_type']} ₹{txn['total_amount']:,.2f}")
        
    finally:
        await mysql_db.disconnect()
    
    # Verify ChromaDB
    vector_store = VectorStore()
    try:
        await vector_store.initialize()
        if vector_store.collection:
            vector_count = vector_store.collection.count()
            print(f"  📊 ChromaDB: {vector_count} knowledge documents")
        else:
            print(f"  📊 ChromaDB: initialized")
    except Exception as e:
        print(f"  ⚠️ ChromaDB verification failed: {e}")

async def main():
    """Main function to insert all enhanced sample data"""
    print("🚀 Starting enhanced data insertion process...")
    print(f"Using environment: {settings.ENVIRONMENT}")
    print("📈 This will populate the database with hundreds of realistic records")
    
    try:
        # Insert data into all databases
        await insert_mongodb_data()
        await insert_mysql_data()
        await insert_vector_data()
        
        # Verify data insertion
        await verify_data()
        
        print("\n✅ Enhanced data insertion completed successfully!")
        print("\n📋 Summary:")
        print("  • 200+ film stars and sports personalities as clients")
        print("  • 500+ portfolio holdings across multiple asset classes")
        print("  • 2000+ realistic transactions with proper pricing")
        print("  • Comprehensive domain knowledge for RAG queries")
        
        print("\n🎯 Your enhanced RAG agent is now ready to handle:")
        print("  • Complex portfolio analytics for high net worth clients")
        print("  • Detailed transaction history analysis")
        print("  • Investment performance tracking")
        print("  • Risk assessment and asset allocation queries")
        print("  • Natural language queries across all data sources")
        
        print("\n💡 Try asking queries like:")
        print("  • 'Show me the top 10 clients by portfolio value'")
        print("  • 'What are the recent crypto transactions?'")
        print("  • 'Which clients have the highest returns?'")
        print("  • 'Analyze equity vs real estate allocation'")
        
    except Exception as e:
        print(f"❌ Enhanced data insertion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
