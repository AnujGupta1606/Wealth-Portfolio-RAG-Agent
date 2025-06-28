"""
Enhanced sample data for MySQL transactions table
Generates hundreds of realistic transactions for wealth portfolio management
"""

from datetime import datetime, timedelta
import random
import uuid

# Asset data for realistic transactions
EQUITY_ASSETS = [
    {"name": "Reliance Industries", "symbol": "RELIANCE", "price_range": (2200, 2800)},
    {"name": "Tata Consultancy Services", "symbol": "TCS", "price_range": (3000, 3500)},
    {"name": "HDFC Bank", "symbol": "HDFCBANK", "price_range": (1400, 1700)},
    {"name": "Infosys", "symbol": "INFY", "price_range": (1300, 1600)},
    {"name": "ICICI Bank", "symbol": "ICICIBANK", "price_range": (900, 1200)},
    {"name": "State Bank of India", "symbol": "SBIN", "price_range": (500, 700)},
    {"name": "Bharti Airtel", "symbol": "BHARTIARTL", "price_range": (800, 1000)},
    {"name": "ITC", "symbol": "ITC", "price_range": (400, 500)},
    {"name": "Hindustan Unilever", "symbol": "HINDUNILVR", "price_range": (2400, 2800)},
    {"name": "Bajaj Finance", "symbol": "BAJFINANCE", "price_range": (6500, 8000)},
    {"name": "Asian Paints", "symbol": "ASIANPAINT", "price_range": (3000, 3500)},
    {"name": "Maruti Suzuki", "symbol": "MARUTI", "price_range": (9000, 11000)},
    {"name": "Axis Bank", "symbol": "AXISBANK", "price_range": (900, 1200)},
    {"name": "Larsen & Toubro", "symbol": "LT", "price_range": (2200, 2800)},
    {"name": "UltraTech Cement", "symbol": "ULTRACEMCO", "price_range": (8000, 10000)}
]

MUTUAL_FUNDS = [
    {"name": "SBI Large Cap Fund", "symbol": "SBI_LARGE_CAP", "price_range": (170, 190)},
    {"name": "HDFC Top 100 Fund", "symbol": "HDFC_TOP100", "price_range": (650, 750)},
    {"name": "ICICI Prudential Bluechip Fund", "symbol": "ICICI_BLUECHIP", "price_range": (500, 600)},
    {"name": "Axis Long Term Equity Fund", "symbol": "AXIS_LONGTERM", "price_range": (350, 450)},
    {"name": "Mirae Asset Large Cap Fund", "symbol": "MIRAE_LARGECAP", "price_range": (700, 800)},
    {"name": "Kotak Standard Multicap Fund", "symbol": "KOTAK_MULTICAP", "price_range": (400, 500)},
    {"name": "Franklin India Equity Fund", "symbol": "FRANKLIN_EQUITY", "price_range": (600, 700)},
    {"name": "DSP Top 100 Equity Fund", "symbol": "DSP_TOP100", "price_range": (250, 350)}
]

CRYPTO_ASSETS = [
    {"name": "Bitcoin", "symbol": "BTC", "price_range": (2500000, 3500000)},
    {"name": "Ethereum", "symbol": "ETH", "price_range": (180000, 250000)},
    {"name": "Binance Coin", "symbol": "BNB", "price_range": (25000, 35000)},
    {"name": "Cardano", "symbol": "ADA", "price_range": (35, 55)},
    {"name": "Polygon", "symbol": "MATIC", "price_range": (60, 100)},
    {"name": "Solana", "symbol": "SOL", "price_range": (8000, 12000)}
]

REAL_ESTATE_ASSETS = [
    {"name": "Mumbai Commercial Property", "symbol": "REAL_MUM_001", "price_range": (2000000000, 5000000000)},
    {"name": "Delhi Residential Complex", "symbol": "REAL_DEL_001", "price_range": (1500000000, 3000000000)},
    {"name": "Bangalore IT Park", "symbol": "REAL_BLR_001", "price_range": (3000000000, 6000000000)},
    {"name": "Chennai Industrial Land", "symbol": "REAL_CHE_001", "price_range": (1000000000, 2500000000)},
    {"name": "Pune Commercial Complex", "symbol": "REAL_PUN_001", "price_range": (800000000, 2000000000)},
    {"name": "Hyderabad Tech Hub", "symbol": "REAL_HYD_001", "price_range": (1200000000, 2800000000)}
]

FIXED_INCOME_ASSETS = [
    {"name": "Government Bonds 10Y", "symbol": "GOV_BOND_10Y", "price_range": (95000, 105000)},
    {"name": "Corporate Bonds AAA", "symbol": "CORP_BOND_AAA", "price_range": (98000, 102000)},
    {"name": "Treasury Bills 91D", "symbol": "TBILL_91D", "price_range": (99500, 100000)},
    {"name": "State Development Loans", "symbol": "SDL_10Y", "price_range": (96000, 104000)},
    {"name": "Infrastructure Bonds", "symbol": "INFRA_BOND", "price_range": (97000, 103000)}
]

BROKERS = [
    "HDFC Securities", "Zerodha", "Angel Broking", "ICICI Direct", "Kotak Securities",
    "Axis Direct", "SBI Securities", "Motilal Oswal", "Sharekhan", "5paisa",
    "Upstox", "Groww", "Edelweiss", "IIFL Securities", "Religare Securities"
]

CRYPTO_EXCHANGES = ["WazirX", "CoinDCX", "Binance", "Coinbase", "ZebPay", "BitBNS"]

REAL_ESTATE_BROKERS = ["Knight Frank", "CBRE", "JLL", "Cushman & Wakefield", "Colliers"]

EXCHANGES = ["NSE", "BSE"]

TRANSACTION_TYPES = ["BUY", "SELL"]
STATUSES = ["COMPLETED", "PENDING", "FAILED"]

def generate_transaction_id():
    """Generate unique transaction ID"""
    return f"TXN_{uuid.uuid4().hex[:8].upper()}"

def generate_client_ids(count=200):
    """Generate client IDs matching the MongoDB data"""
    return [f"client_{str(i+1).zfill(3)}" for i in range(count)]

def generate_transactions_for_client(client_id, num_transactions=None):
    """Generate transactions for a specific client"""
    if num_transactions is None:
        # Generate between 5-25 transactions per client
        num_transactions = random.randint(5, 25)
    
    transactions = []
    
    for _ in range(num_transactions):
        # Random transaction type
        transaction_type = random.choice(TRANSACTION_TYPES)
        
        # Random asset type
        asset_type = random.choice(["Equity", "Mutual Fund", "Cryptocurrency", "Real Estate", "Fixed Income"])
        
        # Generate transaction based on asset type
        if asset_type == "Equity":
            asset = random.choice(EQUITY_ASSETS)
            broker = random.choice(BROKERS)
            exchange = random.choice(EXCHANGES)
            quantity = random.randint(1000, 500000)  # 1K to 500K shares
            price_per_unit = random.uniform(asset["price_range"][0], asset["price_range"][1])
            fees_rate = random.uniform(0.001, 0.005)  # 0.1% to 0.5%
            
        elif asset_type == "Mutual Fund":
            asset = random.choice(MUTUAL_FUNDS)
            broker = "AMC Direct"
            exchange = "AMC Direct"
            quantity = random.randint(10000, 5000000)  # 10K to 5M units
            price_per_unit = random.uniform(asset["price_range"][0], asset["price_range"][1])
            fees_rate = 0.0  # Direct mutual funds have no fees
            
        elif asset_type == "Cryptocurrency":
            asset = random.choice(CRYPTO_ASSETS)
            broker = random.choice(CRYPTO_EXCHANGES)
            exchange = broker
            if asset["symbol"] == "BTC":
                quantity = random.uniform(0.1, 50)  # 0.1 to 50 BTC
            elif asset["symbol"] == "ETH":
                quantity = random.uniform(1, 500)  # 1 to 500 ETH
            else:
                quantity = random.uniform(100, 50000)  # Other cryptos
            price_per_unit = random.uniform(asset["price_range"][0], asset["price_range"][1])
            fees_rate = random.uniform(0.005, 0.02)  # 0.5% to 2%
            
        elif asset_type == "Real Estate":
            asset = random.choice(REAL_ESTATE_ASSETS)
            broker = random.choice(REAL_ESTATE_BROKERS)
            exchange = "Real Estate"
            quantity = 1  # Real estate is typically 1 unit
            price_per_unit = random.uniform(asset["price_range"][0], asset["price_range"][1])
            fees_rate = random.uniform(0.02, 0.05)  # 2% to 5%
            
        else:  # Fixed Income
            asset = random.choice(FIXED_INCOME_ASSETS)
            broker = random.choice(BROKERS)
            exchange = random.choice(EXCHANGES)
            quantity = random.randint(100, 10000)  # 100 to 10K bonds
            price_per_unit = random.uniform(asset["price_range"][0], asset["price_range"][1])
            fees_rate = random.uniform(0.001, 0.003)  # 0.1% to 0.3%
        
        # Calculate amounts
        total_amount = quantity * price_per_unit
        fees = total_amount * fees_rate
        
        # Random dates within last 2 years
        days_ago = random.randint(1, 730)
        transaction_date = datetime.now() - timedelta(days=days_ago)
        settlement_date = transaction_date + timedelta(days=random.randint(1, 3))
        
        # Random status (mostly completed)
        status = random.choices(STATUSES, weights=[90, 8, 2])[0]  # 90% completed, 8% pending, 2% failed
        
        transaction = {
            'transaction_id': generate_transaction_id(),
            'client_id': client_id,
            'transaction_type': transaction_type,
            'asset_type': asset_type,
            'asset_name': asset["name"],
            'symbol': asset["symbol"],
            'quantity': quantity,
            'price_per_unit': round(price_per_unit, 2),
            'total_amount': round(total_amount, 2),
            'fees': round(fees, 2),
            'transaction_date': transaction_date,
            'settlement_date': settlement_date,
            'broker': broker,
            'exchange': exchange,
            'status': status
        }
        
        transactions.append(transaction)
    
    return transactions

def generate_enhanced_transactions(num_clients=200):
    """Generate enhanced transaction data for multiple clients"""
    all_transactions = []
    client_ids = generate_client_ids(num_clients)
    
    print(f"Generating transactions for {num_clients} clients...")
    
    for i, client_id in enumerate(client_ids):
        if i % 20 == 0:
            print(f"Processing client {i+1}/{num_clients}")
        
        client_transactions = generate_transactions_for_client(client_id)
        all_transactions.extend(client_transactions)
    
    print(f"Generated {len(all_transactions)} total transactions")
    return all_transactions

# For backward compatibility with existing insert script
SAMPLE_TRANSACTIONS = generate_enhanced_transactions()
