"""Database connection modules"""

from .mongodb import MongoDBConnection
from .mysql_db import MySQLConnection  
from .vector_store import VectorStore

# Create singleton instances
mongodb = MongoDBConnection()
mysql_db = MySQLConnection()
vector_store = VectorStore()

__all__ = ["mongodb", "mysql_db", "vector_store"]
