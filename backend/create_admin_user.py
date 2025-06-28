"""
Create admin user for the wealth portfolio application
"""

import asyncio
from passlib.context import CryptContext
from app.database.mongodb import MongoDBConnection

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin_user():
    """Create a default admin user"""
    print("🔐 Creating admin user...")
    
    # User credentials
    username = "admin"
    password = "admin123"  # You can change this
    email = "admin@wealth.com"
    
    # Hash the password
    hashed_password = pwd_context.hash(password)
    
    # Connect to MongoDB
    mongodb = MongoDBConnection()
    await mongodb.connect()
    
    try:
        users_collection = mongodb.get_collection("users")
        
        # Check if admin user already exists
        existing_user = await users_collection.find_one({"username": username})
        if existing_user:
            print(f"  ⚠️  Admin user '{username}' already exists")
            return
        
        # Create admin user document
        admin_user = {
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "role": "admin",
            "is_active": True,
            "permissions": ["read", "write", "admin"],
            "created_at": "2025-06-28T00:00:00",
            "last_login": None
        }
        
        # Insert the user
        result = await users_collection.insert_one(admin_user)
        print(f"  ✅ Admin user created successfully!")
        print(f"  📧 Username: {username}")
        print(f"  🔑 Password: {password}")
        print(f"  🆔 User ID: {result.inserted_id}")
        
        # Create index on username for faster lookups
        await users_collection.create_index("username", unique=True)
        print(f"  📊 Created index on username field")
        
    except Exception as e:
        print(f"  ❌ Error creating admin user: {e}")
        raise
    finally:
        await mongodb.disconnect()

if __name__ == "__main__":
    asyncio.run(create_admin_user())
