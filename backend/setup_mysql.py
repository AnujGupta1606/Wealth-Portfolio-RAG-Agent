"""
MySQL Database Setup Script for MAMP
"""

import asyncio
import aiomysql
from app.config import settings

async def create_database():
    """Create the MySQL database and tables"""
    print("🔄 Setting up MySQL database...")
    
    # First connect without specifying database to create it
    connection = await aiomysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        autocommit=True
    )
    
    try:
        cursor = await connection.cursor()
        
        # Create database if it doesn't exist
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE}")
        print(f"  ✅ Database '{settings.MYSQL_DATABASE}' created/verified")
        
        # Use the database
        await cursor.execute(f"USE {settings.MYSQL_DATABASE}")
        
        # Create transactions table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            transaction_id VARCHAR(50) UNIQUE NOT NULL,
            client_id VARCHAR(50) NOT NULL,
            transaction_type ENUM('BUY', 'SELL') NOT NULL,
            asset_type VARCHAR(50) NOT NULL,
            asset_name VARCHAR(100) NOT NULL,
            symbol VARCHAR(20),
            quantity DECIMAL(15,2) NOT NULL,
            price_per_unit DECIMAL(15,2) NOT NULL,
            total_amount DECIMAL(20,2) NOT NULL,
            fees DECIMAL(15,2) DEFAULT 0,
            transaction_date DATETIME NOT NULL,
            settlement_date DATETIME,
            broker VARCHAR(100),
            exchange VARCHAR(50),
            status ENUM('PENDING', 'COMPLETED', 'FAILED') DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_client_id (client_id),
            INDEX idx_transaction_date (transaction_date),
            INDEX idx_asset_type (asset_type),
            INDEX idx_status (status)
        )
        """
        
        await cursor.execute(create_table_sql)
        print("  ✅ Transactions table created/verified")
        
        await cursor.close()
        
    finally:
        connection.close()
    
    print("  ✅ MySQL setup completed!")

if __name__ == "__main__":
    asyncio.run(create_database())
