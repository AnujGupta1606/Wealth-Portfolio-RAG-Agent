"""
Test MySQL connection to MAMP
"""

import asyncio
import aiomysql
from app.config import settings

async def test_connection():
    """Test MySQL connection"""
    print(f"Testing connection to MySQL...")
    print(f"Host: {settings.MYSQL_HOST}")
    print(f"Port: {settings.MYSQL_PORT}")
    print(f"User: {settings.MYSQL_USER}")
    print(f"Password: {'*' * len(settings.MYSQL_PASSWORD)}")
    
    try:
        connection = await aiomysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            autocommit=True
        )
        print("✅ Successfully connected to MySQL!")
        connection.close()
        
        # Now test with database
        connection = await aiomysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DATABASE,
            autocommit=True
        )
        print(f"✅ Successfully connected to database '{settings.MYSQL_DATABASE}'!")
        connection.close()
        
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure MAMP is running")
        print("2. Check that MySQL is started in MAMP")
        print("3. Verify MAMP MySQL settings:")
        print("   - Host: usually 127.0.0.1 or localhost")
        print("   - Port: usually 8889 (MAMP default) or 3306")
        print("   - Username: usually 'root'")
        print("   - Password: usually 'root' or empty")

if __name__ == "__main__":
    asyncio.run(test_connection())
