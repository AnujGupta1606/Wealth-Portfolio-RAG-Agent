"""
Sample data for MongoDB collections - wealth portfolio management
"""

from datetime import datetime, timedelta
import random

# Sample clients data - film stars and sports personalities
SAMPLE_CLIENTS = [
    {
        "_id": "client_001",
        "client_id": "client_001",
        "name": "Rajesh Kumar",
        "type": "Film Star",
        "age": 45,
        "gender": "Male",
        "location": "Mumbai",
        "risk_tolerance": "Moderate",
        "investment_horizon": "Long-term",
        "total_portfolio_value": 15000000000,  # 150 crores
        "annual_income": 2500000000,  # 25 crores
        "contact": {
            "email": "rajesh.kumar@filmstar.com",
            "phone": "+91-9876543210"
        },
        "created_at": datetime.now() - timedelta(days=365*3),
        "last_updated": datetime.now() - timedelta(days=30)
    },
    {
        "_id": "client_002",
        "client_id": "client_002", 
        "name": "Priya Sharma",
        "type": "Cricket Player",
        "age": 28,
        "gender": "Female",
        "location": "Delhi",
        "risk_tolerance": "Aggressive",
        "investment_horizon": "Medium-term",
        "total_portfolio_value": 8500000000,  # 85 crores
        "annual_income": 1200000000,  # 12 crores
        "contact": {
            "email": "priya.sharma@cricket.com",
            "phone": "+91-9876543211"
        },
        "created_at": datetime.now() - timedelta(days=365*2),
        "last_updated": datetime.now() - timedelta(days=15)
    },
    {
        "_id": "client_003",
        "client_id": "client_003",
        "name": "Arjun Malhotra", 
        "type": "Film Director",
        "age": 52,
        "gender": "Male",
        "location": "Bangalore",
        "risk_tolerance": "Conservative",
        "investment_horizon": "Long-term",
        "total_portfolio_value": 12000000000,  # 120 crores
        "annual_income": 800000000,  # 8 crores
        "contact": {
            "email": "arjun.malhotra@director.com",
            "phone": "+91-9876543212"
        },
        "created_at": datetime.now() - timedelta(days=365*5),
        "last_updated": datetime.now() - timedelta(days=7)
    },
    {
        "_id": "client_004",
        "client_id": "client_004",
        "name": "Sneha Patel",
        "type": "Tennis Player", 
        "age": 24,
        "gender": "Female",
        "location": "Chennai",
        "risk_tolerance": "Moderate",
        "investment_horizon": "Short-term",
        "total_portfolio_value": 5500000000,  # 55 crores
        "annual_income": 900000000,  # 9 crores
        "contact": {
            "email": "sneha.patel@tennis.com",
            "phone": "+91-9876543213"
        },
        "created_at": datetime.now() - timedelta(days=365*1),
        "last_updated": datetime.now() - timedelta(days=5)
    },
    {
        "_id": "client_005",
        "client_id": "client_005",
        "name": "Vikram Singh",
        "type": "Football Player",
        "age": 31,
        "gender": "Male", 
        "location": "Kolkata",
        "risk_tolerance": "Aggressive",
        "investment_horizon": "Medium-term",
        "total_portfolio_value": 7200000000,  # 72 crores
        "annual_income": 1500000000,  # 15 crores
        "contact": {
            "email": "vikram.singh@football.com",
            "phone": "+91-9876543214"
        },
        "created_at": datetime.now() - timedelta(days=365*4),
        "last_updated": datetime.now() - timedelta(days=20)
    }
]

# Sample portfolio holdings data
SAMPLE_PORTFOLIO_HOLDINGS = [
    # Rajesh Kumar's holdings
    {
        "_id": "holding_001",
        "client_id": "client_001",
        "asset_type": "Equity",
        "asset_name": "Reliance Industries",
        "symbol": "RELIANCE",
        "quantity": 500000,
        "purchase_price": 2400,
        "current_price": 2650,
        "market_value": 1325000000,  # 13.25 crores
        "allocation_percentage": 8.83,
        "sector": "Energy",
        "purchase_date": datetime.now() - timedelta(days=180),
        "last_updated": datetime.now()
    },
    {
        "_id": "holding_002", 
        "client_id": "client_001",
        "asset_type": "Equity",
        "asset_name": "Tata Consultancy Services",
        "symbol": "TCS",
        "quantity": 300000,
        "purchase_price": 3200,
        "current_price": 3450,
        "market_value": 1035000000,  # 10.35 crores
        "allocation_percentage": 6.9,
        "sector": "Technology",
        "purchase_date": datetime.now() - timedelta(days=120),
        "last_updated": datetime.now()
    },
    {
        "_id": "holding_003",
        "client_id": "client_001", 
        "asset_type": "Real Estate",
        "asset_name": "Mumbai Commercial Property",
        "symbol": "REAL_001",
        "quantity": 1,
        "purchase_price": 2500000000,
        "current_price": 3200000000,
        "market_value": 3200000000,  # 32 crores
        "allocation_percentage": 21.33,
        "sector": "Real Estate",
        "purchase_date": datetime.now() - timedelta(days=730),
        "last_updated": datetime.now() - timedelta(days=30)
    },
    {
        "_id": "holding_004",
        "client_id": "client_001",
        "asset_type": "Fixed Income", 
        "asset_name": "Government Bonds",
        "symbol": "GOV_BOND_10Y",
        "quantity": 5000,
        "purchase_price": 100000,
        "current_price": 102000,
        "market_value": 510000000,  # 5.1 crores
        "allocation_percentage": 3.4,
        "sector": "Government Securities",
        "purchase_date": datetime.now() - timedelta(days=365),
        "last_updated": datetime.now()
    },
    
    # Priya Sharma's holdings
    {
        "_id": "holding_005",
        "client_id": "client_002",
        "asset_type": "Equity",
        "asset_name": "HDFC Bank",
        "symbol": "HDFCBANK",
        "quantity": 400000,
        "purchase_price": 1450,
        "current_price": 1620,
        "market_value": 648000000,  # 6.48 crores
        "allocation_percentage": 7.62,
        "sector": "Banking",
        "purchase_date": datetime.now() - timedelta(days=90),
        "last_updated": datetime.now()
    },
    {
        "_id": "holding_006",
        "client_id": "client_002",
        "asset_type": "Cryptocurrency",
        "asset_name": "Bitcoin", 
        "symbol": "BTC",
        "quantity": 15,
        "purchase_price": 2800000,
        "current_price": 3200000,
        "market_value": 480000000,  # 4.8 crores
        "allocation_percentage": 5.65,
        "sector": "Cryptocurrency",
        "purchase_date": datetime.now() - timedelta(days=45),
        "last_updated": datetime.now()
    },
    {
        "_id": "holding_007",
        "client_id": "client_002",
        "asset_type": "Mutual Fund",
        "asset_name": "SBI Large Cap Fund",
        "symbol": "SBI_LARGE_CAP",
        "quantity": 2000000,
        "purchase_price": 180,
        "current_price": 195,
        "market_value": 390000000,  # 3.9 crores
        "allocation_percentage": 4.59,
        "sector": "Mutual Funds",
        "purchase_date": datetime.now() - timedelta(days=200),
        "last_updated": datetime.now()
    },
    
    # Arjun Malhotra's holdings
    {
        "_id": "holding_008",
        "client_id": "client_003",
        "asset_type": "Equity",
        "asset_name": "Infosys Limited",
        "symbol": "INFY",
        "quantity": 600000,
        "purchase_price": 1200,
        "current_price": 1380,
        "market_value": 828000000,  # 8.28 crores
        "allocation_percentage": 6.9,
        "sector": "Technology",
        "purchase_date": datetime.now() - timedelta(days=300),
        "last_updated": datetime.now()
    },
    {
        "_id": "holding_009",
        "client_id": "client_003",
        "asset_type": "Fixed Income",
        "asset_name": "Corporate Bonds AAA",
        "symbol": "CORP_BOND_AAA",
        "quantity": 8000,
        "purchase_price": 100000,
        "current_price": 103000,
        "market_value": 824000000,  # 8.24 crores
        "allocation_percentage": 6.87,
        "sector": "Corporate Bonds",
        "purchase_date": datetime.now() - timedelta(days=400),
        "last_updated": datetime.now()
    },
    
    # Sneha Patel's holdings
    {
        "_id": "holding_010",
        "client_id": "client_004",
        "asset_type": "Equity",
        "asset_name": "Asian Paints",
        "symbol": "ASIANPAINT",
        "quantity": 150000,
        "purchase_price": 2800,
        "current_price": 3100,
        "market_value": 465000000,  # 4.65 crores
        "allocation_percentage": 8.45,
        "sector": "Consumer Goods",
        "purchase_date": datetime.now() - timedelta(days=60),
        "last_updated": datetime.now()
    },
    
    # Vikram Singh's holdings  
    {
        "_id": "holding_011",
        "client_id": "client_005",
        "asset_type": "Equity",
        "asset_name": "Bajaj Finance",
        "symbol": "BAJFINANCE",
        "quantity": 200000,
        "purchase_price": 6500,
        "current_price": 7200,
        "market_value": 1440000000,  # 14.4 crores
        "allocation_percentage": 20.0,
        "sector": "Financial Services",
        "purchase_date": datetime.now() - timedelta(days=150),
        "last_updated": datetime.now()
    }
]
