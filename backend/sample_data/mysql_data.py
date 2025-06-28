"""
Sample data for MySQL transactions table
"""

from datetime import datetime, timedelta
import random

# Sample transactions data
SAMPLE_TRANSACTIONS = [
    # Rajesh Kumar transactions
    {
        'transaction_id': 'TXN_001',
        'client_id': 'client_001',
        'transaction_type': 'BUY',
        'asset_type': 'Equity',
        'asset_name': 'Reliance Industries',
        'symbol': 'RELIANCE',
        'quantity': 500000,
        'price_per_unit': 2400.00,
        'total_amount': 1200000000.00,  # 12 crores
        'fees': 1200000.00,  # 12 lakhs
        'transaction_date': datetime.now() - timedelta(days=180),
        'settlement_date': datetime.now() - timedelta(days=178),
        'broker': 'HDFC Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_002',
        'client_id': 'client_001', 
        'transaction_type': 'BUY',
        'asset_type': 'Equity',
        'asset_name': 'Tata Consultancy Services',
        'symbol': 'TCS',
        'quantity': 300000,
        'price_per_unit': 3200.00,
        'total_amount': 960000000.00,  # 9.6 crores
        'fees': 960000.00,  # 9.6 lakhs
        'transaction_date': datetime.now() - timedelta(days=120),
        'settlement_date': datetime.now() - timedelta(days=118),
        'broker': 'HDFC Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_003',
        'client_id': 'client_001',
        'transaction_type': 'BUY',
        'asset_type': 'Real Estate',
        'asset_name': 'Mumbai Commercial Property',
        'symbol': 'REAL_001',
        'quantity': 1,
        'price_per_unit': 2500000000.00,
        'total_amount': 2500000000.00,  # 25 crores
        'fees': 12500000.00,  # 1.25 crores (5% fees)
        'transaction_date': datetime.now() - timedelta(days=730),
        'settlement_date': datetime.now() - timedelta(days=725),
        'broker': 'Knight Frank',
        'exchange': 'Real Estate',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_004',
        'client_id': 'client_001',
        'transaction_type': 'BUY',
        'asset_type': 'Fixed Income',
        'asset_name': 'Government Bonds',
        'symbol': 'GOV_BOND_10Y',
        'quantity': 5000,
        'price_per_unit': 100000.00,
        'total_amount': 500000000.00,  # 5 crores
        'fees': 500000.00,  # 5 lakhs
        'transaction_date': datetime.now() - timedelta(days=365),
        'settlement_date': datetime.now() - timedelta(days=363),
        'broker': 'SBI Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    
    # Priya Sharma transactions
    {
        'transaction_id': 'TXN_005',
        'client_id': 'client_002',
        'transaction_type': 'BUY',
        'asset_type': 'Equity',
        'asset_name': 'HDFC Bank',
        'symbol': 'HDFCBANK',
        'quantity': 400000,
        'price_per_unit': 1450.00,
        'total_amount': 580000000.00,  # 5.8 crores
        'fees': 580000.00,  # 5.8 lakhs
        'transaction_date': datetime.now() - timedelta(days=90),
        'settlement_date': datetime.now() - timedelta(days=88),
        'broker': 'Zerodha',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_006',
        'client_id': 'client_002',
        'transaction_type': 'BUY',
        'asset_type': 'Cryptocurrency',
        'asset_name': 'Bitcoin',
        'symbol': 'BTC',
        'quantity': 15,
        'price_per_unit': 2800000.00,
        'total_amount': 420000000.00,  # 4.2 crores
        'fees': 2100000.00,  # 21 lakhs (0.5% fees)
        'transaction_date': datetime.now() - timedelta(days=45),
        'settlement_date': datetime.now() - timedelta(days=45),
        'broker': 'WazirX',
        'exchange': 'WazirX',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_007',
        'client_id': 'client_002',
        'transaction_type': 'BUY',
        'asset_type': 'Mutual Fund',
        'asset_name': 'SBI Large Cap Fund',
        'symbol': 'SBI_LARGE_CAP',
        'quantity': 2000000,
        'price_per_unit': 180.00,
        'total_amount': 360000000.00,  # 3.6 crores
        'fees': 0.00,  # No fees for direct mutual funds
        'transaction_date': datetime.now() - timedelta(days=200),
        'settlement_date': datetime.now() - timedelta(days=198),
        'broker': 'SBI Mutual Fund',
        'exchange': 'AMC Direct',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_008',
        'client_id': 'client_002',
        'transaction_type': 'SELL',
        'asset_type': 'Equity',
        'asset_name': 'HDFC Bank',
        'symbol': 'HDFCBANK',
        'quantity': 50000,
        'price_per_unit': 1580.00,
        'total_amount': 79000000.00,  # 79 lakhs
        'fees': 79000.00,  # 79 thousand
        'transaction_date': datetime.now() - timedelta(days=30),
        'settlement_date': datetime.now() - timedelta(days=28),
        'broker': 'Zerodha',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    
    # Arjun Malhotra transactions
    {
        'transaction_id': 'TXN_009',
        'client_id': 'client_003',
        'transaction_type': 'BUY',
        'asset_type': 'Equity',
        'asset_name': 'Infosys Limited',
        'symbol': 'INFY',
        'quantity': 600000,
        'price_per_unit': 1200.00,
        'total_amount': 720000000.00,  # 7.2 crores
        'fees': 720000.00,  # 7.2 lakhs
        'transaction_date': datetime.now() - timedelta(days=300),
        'settlement_date': datetime.now() - timedelta(days=298),
        'broker': 'ICICI Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_010',
        'client_id': 'client_003',
        'transaction_type': 'BUY',
        'asset_type': 'Fixed Income',
        'asset_name': 'Corporate Bonds AAA',
        'symbol': 'CORP_BOND_AAA',
        'quantity': 8000,
        'price_per_unit': 100000.00,
        'total_amount': 800000000.00,  # 8 crores
        'fees': 400000.00,  # 4 lakhs
        'transaction_date': datetime.now() - timedelta(days=400),
        'settlement_date': datetime.now() - timedelta(days=398),
        'broker': 'ICICI Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    
    # Sneha Patel transactions
    {
        'transaction_id': 'TXN_011',
        'client_id': 'client_004',
        'transaction_type': 'BUY',
        'asset_type': 'Equity',
        'asset_name': 'Asian Paints',
        'symbol': 'ASIANPAINT',
        'quantity': 150000,
        'price_per_unit': 2800.00,
        'total_amount': 420000000.00,  # 4.2 crores
        'fees': 420000.00,  # 4.2 lakhs
        'transaction_date': datetime.now() - timedelta(days=60),
        'settlement_date': datetime.now() - timedelta(days=58),
        'broker': 'Angel Broking',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_012',
        'client_id': 'client_004',
        'transaction_type': 'SELL',
        'asset_type': 'Equity',
        'asset_name': 'Asian Paints',
        'symbol': 'ASIANPAINT',
        'quantity': 25000,
        'price_per_unit': 3050.00,
        'total_amount': 76250000.00,  # 76.25 lakhs
        'fees': 76250.00,  # 76.25 thousand
        'transaction_date': datetime.now() - timedelta(days=15),
        'settlement_date': datetime.now() - timedelta(days=13),
        'broker': 'Angel Broking',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    
    # Vikram Singh transactions
    {
        'transaction_id': 'TXN_013',
        'client_id': 'client_005',
        'transaction_type': 'BUY',
        'asset_type': 'Equity',
        'asset_name': 'Bajaj Finance',
        'symbol': 'BAJFINANCE',
        'quantity': 200000,
        'price_per_unit': 6500.00,
        'total_amount': 1300000000.00,  # 13 crores
        'fees': 1300000.00,  # 13 lakhs
        'transaction_date': datetime.now() - timedelta(days=150),
        'settlement_date': datetime.now() - timedelta(days=148),
        'broker': 'Kotak Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_014',
        'client_id': 'client_005',
        'transaction_type': 'DIVIDEND',
        'asset_type': 'Equity',
        'asset_name': 'Bajaj Finance',
        'symbol': 'BAJFINANCE',
        'quantity': 200000,
        'price_per_unit': 25.00,  # Dividend per share
        'total_amount': 5000000.00,  # 50 lakhs dividend
        'fees': 0.00,
        'transaction_date': datetime.now() - timedelta(days=30),
        'settlement_date': datetime.now() - timedelta(days=28),
        'broker': 'Kotak Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    
    # Additional recent transactions for better data variety
    {
        'transaction_id': 'TXN_015',
        'client_id': 'client_001',
        'transaction_type': 'SELL',
        'asset_type': 'Equity',
        'asset_name': 'Reliance Industries',
        'symbol': 'RELIANCE',
        'quantity': 100000,
        'price_per_unit': 2600.00,
        'total_amount': 260000000.00,  # 2.6 crores
        'fees': 260000.00,  # 2.6 lakhs
        'transaction_date': datetime.now() - timedelta(days=10),
        'settlement_date': datetime.now() - timedelta(days=8),
        'broker': 'HDFC Securities',
        'exchange': 'NSE',
        'status': 'COMPLETED'
    },
    {
        'transaction_id': 'TXN_016',
        'client_id': 'client_002',
        'transaction_type': 'BUY',
        'asset_type': 'Cryptocurrency',
        'asset_name': 'Ethereum',
        'symbol': 'ETH',
        'quantity': 50,
        'price_per_unit': 180000.00,
        'total_amount': 90000000.00,  # 90 lakhs
        'fees': 450000.00,  # 4.5 lakhs
        'transaction_date': datetime.now() - timedelta(days=20),
        'settlement_date': datetime.now() - timedelta(days=20),
        'broker': 'WazirX',
        'exchange': 'WazirX',
        'status': 'COMPLETED'
    }
]
