"""
Enhanced sample data for MongoDB collections - wealth portfolio management
Hundreds of clients and portfolio holdings for realistic testing
"""

from datetime import datetime, timedelta
import random

# Generate realistic Indian names for film stars and sports personalities
FIRST_NAMES = [
    "Rajesh", "Priya", "Arjun", "Sneha", "Vikram", "Anita", "Ravi", "Deepika", 
    "Akshay", "Kareena", "Shah Rukh", "Alia", "Salman", "Katrina", "Hrithik", 
    "Aishwarya", "Ranveer", "Kangana", "Varun", "Jacqueline", "Tiger", "Kriti",
    "Virat", "Anushka", "Rohit", "Sakshi", "Hardik", "Natasa", "KL", "Athiya",
    "Jasprit", "MS", "Suresh", "Harbhajan", "Yuvraj", "Hazel", "Shikhar", "Ayesha",
    "Rishabh", "Urvashi", "Kuldeep", "Yuzvendra", "Ajinkya", "Prithi", "Cheteshwar",
    "Ravindra", "Mayank", "Ishant", "Mohammed", "Washington", "Navdeep", "Shardul"
]

LAST_NAMES = [
    "Kumar", "Sharma", "Malhotra", "Patel", "Singh", "Mehta", "Gupta", "Agarwal",
    "Chopra", "Kapoor", "Khan", "Bhatt", "Johar", "Bahl", "Roshan", "Rai",
    "Padukone", "Kohli", "Dhoni", "Pandya", "Rahul", "Bumrah", "Raina", "Dhawan",
    "Pant", "Yadav", "Ashwin", "Saini", "Shami", "Sundar", "Jadeja", "Thakur"
]

PROFESSIONS = [
    "Film Star", "Cricket Player", "Football Player", "Tennis Player", "Film Director", 
    "Music Director", "Producer", "Badminton Player", "Hockey Player", "Boxing Champion",
    "Wrestling Champion", "Singer", "Television Actor", "Web Series Actor", "Comedian"
]

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", 
    "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal"
]

RISK_LEVELS = ["Conservative", "Moderate", "Aggressive"]
INVESTMENT_HORIZONS = ["Short-term", "Medium-term", "Long-term"]

def generate_client_data(count=200):
    """Generate realistic client data"""
    clients = []
    
    for i in range(count):
        # Generate basic info
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        # Generate wealth based on profession
        profession = random.choice(PROFESSIONS)
        base_wealth = {
            "Film Star": random.randint(50, 500),  # 50-500 crores
            "Cricket Player": random.randint(20, 300),
            "Football Player": random.randint(10, 100),
            "Tennis Player": random.randint(15, 150),
            "Film Director": random.randint(25, 200),
            "Music Director": random.randint(10, 80),
            "Producer": random.randint(30, 400),
            "Badminton Player": random.randint(5, 50),
            "Hockey Player": random.randint(3, 30),
            "Boxing Champion": random.randint(8, 60),
            "Wrestling Champion": random.randint(5, 40),
            "Singer": random.randint(15, 120),
            "Television Actor": random.randint(8, 80),
            "Web Series Actor": random.randint(5, 50),
            "Comedian": random.randint(10, 70)
        }
        
        portfolio_value = base_wealth.get(profession, 50) * 10000000  # Convert to actual amount
        annual_income = portfolio_value * random.uniform(0.15, 0.4)  # 15-40% of portfolio
        
        client = {
            "_id": f"client_{str(i+1).zfill(3)}",
            "client_id": f"client_{str(i+1).zfill(3)}",
            "name": name,
            "type": profession,
            "age": random.randint(22, 65),
            "gender": random.choice(["Male", "Female"]),
            "location": random.choice(CITIES),
            "risk_tolerance": random.choice(RISK_LEVELS),
            "investment_horizon": random.choice(INVESTMENT_HORIZONS),
            "total_portfolio_value": int(portfolio_value),
            "annual_income": int(annual_income),
            "contact": {
                "email": f"{first_name.lower()}.{last_name.lower()}@{profession.lower().replace(' ', '')}.com",
                "phone": f"+91-{random.randint(7000000000, 9999999999)}"
            },
            "created_at": datetime.now() - timedelta(days=random.randint(30, 1825)),  # 1 month to 5 years ago
            "last_updated": datetime.now() - timedelta(days=random.randint(1, 90))
        }
        
        clients.append(client)
    
    return clients

# Indian stock symbols and names
STOCKS = [
    {"symbol": "RELIANCE", "name": "Reliance Industries"},
    {"symbol": "TCS", "name": "Tata Consultancy Services"},
    {"symbol": "HDFCBANK", "name": "HDFC Bank"},
    {"symbol": "INFY", "name": "Infosys"},
    {"symbol": "ICICIBANK", "name": "ICICI Bank"},
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever"},
    {"symbol": "ITC", "name": "ITC Limited"},
    {"symbol": "SBIN", "name": "State Bank of India"},
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel"},
    {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank"},
    {"symbol": "LT", "name": "Larsen & Toubro"},
    {"symbol": "ASIANPAINT", "name": "Asian Paints"},
    {"symbol": "MARUTI", "name": "Maruti Suzuki"},
    {"symbol": "BAJFINANCE", "name": "Bajaj Finance"},
    {"symbol": "AXISBANK", "name": "Axis Bank"},
    {"symbol": "WIPRO", "name": "Wipro Limited"},
    {"symbol": "ULTRACEMCO", "name": "UltraTech Cement"},
    {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical"},
    {"symbol": "NTPC", "name": "NTPC Limited"},
    {"symbol": "TITAN", "name": "Titan Company"},
    {"symbol": "ADANIPORTS", "name": "Adani Ports"},
    {"symbol": "POWERGRID", "name": "Power Grid Corporation"},
    {"symbol": "NESTLEIND", "name": "Nestle India"},
    {"symbol": "DRREDDY", "name": "Dr. Reddy's Laboratories"},
    {"symbol": "JSWSTEEL", "name": "JSW Steel"},
    {"symbol": "TATAMOTORS", "name": "Tata Motors"},
    {"symbol": "TECHM", "name": "Tech Mahindra"},
    {"symbol": "HCLTECH", "name": "HCL Technologies"},
    {"symbol": "GRASIM", "name": "Grasim Industries"},
    {"symbol": "BAJAJFINSV", "name": "Bajaj Finserv"}
]

def generate_portfolio_holdings(client_count=200):
    """Generate portfolio holdings for all clients"""
    holdings = []
    
    for i in range(client_count):
        client_id = f"client_{str(i+1).zfill(3)}"
        
        # Each client has 3-8 different holdings
        num_holdings = random.randint(3, 8)
        client_stocks = random.sample(STOCKS, num_holdings)
        
        for stock in client_stocks:
            # Generate realistic holding amounts
            quantity = random.randint(1000, 500000)  # 1K to 500K shares
            avg_price = random.uniform(100, 5000)    # ₹100 to ₹5000 per share
            current_price = avg_price * random.uniform(0.7, 1.5)  # -30% to +50% change
            current_value = quantity * current_price
            
            holding = {
                "client_id": client_id,
                "stock_symbol": stock["symbol"],
                "stock_name": stock["name"],
                "quantity": quantity,
                "avg_price": round(avg_price, 2),
                "current_price": round(current_price, 2),
                "current_value": round(current_value, 2),
                "gain_loss": round(current_value - (quantity * avg_price), 2),
                "gain_loss_percent": round(((current_price - avg_price) / avg_price) * 100, 2),
                "last_updated": datetime.now() - timedelta(days=random.randint(0, 30))
            }
            
            holdings.append(holding)
    
    return holdings

# Generate the actual data
SAMPLE_CLIENTS = generate_client_data(200)
SAMPLE_PORTFOLIO_HOLDINGS = generate_portfolio_holdings(200)
