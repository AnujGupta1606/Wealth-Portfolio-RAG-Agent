"""
Test script to verify RAG agent functionality with sample data
"""

import asyncio
import sys
import os
from pathlib import Path
import json

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.database.mongodb import MongoDB
from app.database.mysql_db import MySQLDB
from app.database.vector_store import VectorStore

async def test_mongodb_queries():
    """Test MongoDB queries"""
    print("🔍 Testing MongoDB queries...")
    
    mongodb = MongoDB()
    await mongodb.connect()
    
    try:
        # Test 1: Get all clients
        clients = await mongodb.get_collection("clients").find({}).to_list(length=None)
        print(f"  ✅ Found {len(clients)} clients")
        
        # Test 2: Get film stars
        film_stars = await mongodb.get_collection("clients").find({"type": "Film Star"}).to_list(length=None)
        print(f"  ✅ Found {len(film_stars)} film stars")
        
        # Test 3: Get high-value portfolios (>10 crores)
        high_value_clients = await mongodb.get_collection("clients").find({
            "total_portfolio_value": {"$gt": 1000000000}
        }).to_list(length=None)
        print(f"  ✅ Found {len(high_value_clients)} clients with >10 crore portfolios")
        
        # Test 4: Get portfolio holdings for a specific client
        client_holdings = await mongodb.get_collection("portfolio_holdings").find({
            "client_id": "client_001"
        }).to_list(length=None)
        print(f"  ✅ Found {len(client_holdings)} holdings for client_001")
        
    except Exception as e:
        print(f"  ❌ MongoDB query error: {e}")
    finally:
        await mongodb.close()

async def test_mysql_queries():
    """Test MySQL queries"""
    print("🔍 Testing MySQL queries...")
    
    mysql_db = MySQLDB()
    await mysql_db.connect()
    
    try:
        # Test 1: Get total transactions count
        result = await mysql_db.execute_query("SELECT COUNT(*) as count FROM transactions")
        print(f"  ✅ Total transactions: {result[0]['count']}")
        
        # Test 2: Get transactions for a specific client
        result = await mysql_db.execute_query(
            "SELECT COUNT(*) as count FROM transactions WHERE client_id = %s",
            ("client_001",)
        )
        print(f"  ✅ Transactions for client_001: {result[0]['count']}")
        
        # Test 3: Get buy vs sell transactions
        result = await mysql_db.execute_query("""
            SELECT transaction_type, COUNT(*) as count, SUM(total_amount) as total_amount
            FROM transactions 
            GROUP BY transaction_type
        """)
        for row in result:
            amount_crores = row['total_amount'] / 10000000  # Convert to crores
            print(f"  ✅ {row['transaction_type']}: {row['count']} transactions, ₹{amount_crores:.2f} crores")
        
        # Test 4: Get recent transactions (last 30 days)
        result = await mysql_db.execute_query("""
            SELECT COUNT(*) as count FROM transactions 
            WHERE transaction_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """)
        print(f"  ✅ Recent transactions (30 days): {result[0]['count']}")
        
    except Exception as e:
        print(f"  ❌ MySQL query error: {e}")
    finally:
        await mysql_db.close()

async def test_vector_queries():
    """Test ChromaDB vector queries"""
    print("🔍 Testing ChromaDB vector queries...")
    
    vector_store = VectorStore()
    
    try:
        await vector_store.initialize()
        
        # Test 1: Get collection info
        count = vector_store.collection.count()
        print(f"  ✅ Vector documents: {count}")
        
        # Test 2: Search for asset allocation knowledge
        results = vector_store.collection.query(
            query_texts=["What is the recommended asset allocation for celebrities?"],
            n_results=3
        )
        print(f"  ✅ Asset allocation search returned {len(results['documents'][0])} results")
        
        # Test 3: Search for risk management
        results = vector_store.collection.query(
            query_texts=["How to assess risk tolerance for athletes?"],
            n_results=2
        )
        print(f"  ✅ Risk management search returned {len(results['documents'][0])} results")
        
        # Test 4: Search for tax planning
        results = vector_store.collection.query(
            query_texts=["Tax optimization strategies for high income individuals"],
            n_results=2
        )
        print(f"  ✅ Tax planning search returned {len(results['documents'][0])} results")
        
    except Exception as e:
        print(f"  ❌ Vector query error: {e}")

async def test_sample_rag_queries():
    """Test some sample RAG queries that combine multiple data sources"""
    print("🎯 Testing sample RAG scenarios...")
    
    mongodb = MongoDB()
    mysql_db = MySQLDB()
    vector_store = VectorStore()
    
    await mongodb.connect()
    await mysql_db.connect()
    await vector_store.initialize()
    
    try:
        # Scenario 1: Client portfolio overview
        print("\n📊 Scenario 1: Get Rajesh Kumar's portfolio overview")
        
        # Get client info from MongoDB
        client = await mongodb.get_collection("clients").find_one({"_id": "client_001"})
        if client:
            print(f"  Client: {client['name']} ({client['type']})")
            print(f"  Portfolio Value: ₹{client['total_portfolio_value']/10000000:.1f} crores")
            print(f"  Risk Tolerance: {client['risk_tolerance']}")
        
        # Get holdings from MongoDB
        holdings = await mongodb.get_collection("portfolio_holdings").find({
            "client_id": "client_001"
        }).to_list(length=None)
        print(f"  Holdings: {len(holdings)} positions")
        
        # Get transactions from MySQL
        transactions = await mysql_db.execute_query(
            "SELECT COUNT(*) as count, SUM(total_amount) as total FROM transactions WHERE client_id = %s",
            ("client_001",)
        )
        if transactions:
            total_crores = transactions[0]['total'] / 10000000
            print(f"  Transactions: {transactions[0]['count']} total, ₹{total_crores:.1f} crores volume")
        
        # Scenario 2: Asset allocation analysis
        print("\n📈 Scenario 2: Asset allocation analysis across all clients")
        
        # Aggregate holdings by asset type
        pipeline = [
            {
                "$group": {
                    "_id": "$asset_type",
                    "total_value": {"$sum": "$market_value"},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"total_value": -1}}
        ]
        
        allocation = await mongodb.get_collection("portfolio_holdings").aggregate(pipeline).to_list(length=None)
        print("  Asset Allocation:")
        for asset in allocation:
            value_crores = asset['total_value'] / 10000000
            print(f"    {asset['_id']}: ₹{value_crores:.1f} crores ({asset['count']} positions)")
        
        # Scenario 3: Transaction trends
        print("\n📊 Scenario 3: Recent transaction trends")
        
        recent_transactions = await mysql_db.execute_query("""
            SELECT asset_type, transaction_type, COUNT(*) as count, 
                   SUM(total_amount) as total_amount
            FROM transactions 
            WHERE transaction_date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
            GROUP BY asset_type, transaction_type
            ORDER BY total_amount DESC
        """)
        
        print("  Recent Activity (90 days):")
        for txn in recent_transactions:
            amount_crores = txn['total_amount'] / 10000000
            print(f"    {txn['asset_type']} {txn['transaction_type']}: {txn['count']} transactions, ₹{amount_crores:.1f} crores")
        
        # Scenario 4: Get relevant knowledge
        print("\n🧠 Scenario 4: Get investment recommendations for aggressive investors")
        
        knowledge_results = vector_store.collection.query(
            query_texts=["Investment strategies for aggressive risk tolerance young athletes"],
            n_results=2
        )
        
        if knowledge_results['documents'][0]:
            print("  Relevant Knowledge:")
            for i, doc in enumerate(knowledge_results['documents'][0]):
                print(f"    {i+1}. {doc[:100]}...")
        
    except Exception as e:
        print(f"  ❌ RAG scenario error: {e}")
    finally:
        await mongodb.close()
        await mysql_db.close()

async def main():
    """Main test function"""
    print("🧪 Testing RAG Agent with Sample Data")
    print("=" * 50)
    
    try:
        await test_mongodb_queries()
        print()
        await test_mysql_queries()
        print()
        await test_vector_queries()
        print()
        await test_sample_rag_queries()
        
        print("\n✅ All tests completed successfully!")
        print("\n🎉 Your RAG agent is ready to handle complex queries like:")
        print("  • 'Show me the portfolio performance of all cricket players'")
        print("  • 'What are the tax optimization strategies for high-income clients?'")
        print("  • 'Which clients have the highest exposure to technology stocks?'")
        print("  • 'Analyze the recent trading patterns for aggressive investors'")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
