"""Data management router"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from app.database import mongodb, mysql_db
from app.routers.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

class DataResponse(BaseModel):
    message: str
    count: int

@router.post("/initialize-sample-data")
async def initialize_sample_data(current_user: dict = Depends(verify_token)):
    """Initialize sample data for testing"""
    try:
        # Initialize MongoDB sample data
        await mongodb.insert_sample_data()
        
        # Initialize MySQL sample data  
        await mysql_db.insert_sample_data()
        
        return DataResponse(
            message="Sample data initialized successfully",
            count=1
        )
        
    except Exception as e:
        logger.error(f"Data initialization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clients")
async def get_clients(
    limit: int = 50,
    current_user: dict = Depends(verify_token)
):
    """Get all clients"""
    try:
        collection = mongodb.get_collection("clients")
        clients = await collection.find().limit(limit).to_list(length=limit)
        return {"clients": clients, "count": len(clients)}
        
    except Exception as e:
        logger.error(f"Get clients error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions")
async def get_transactions(
    limit: int = 50,
    current_user: dict = Depends(verify_token)
):
    """Get recent transactions"""
    try:
        query = "SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT %s"
        transactions = await mysql_db.execute_query(query, (limit,))
        return {"transactions": transactions, "count": len(transactions)}
        
    except Exception as e:
        logger.error(f"Get transactions error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio-holdings")
async def get_portfolio_holdings(
    client_id: Optional[str] = None,
    limit: int = 50,
    current_user: dict = Depends(verify_token)
):
    """Get portfolio holdings"""
    try:
        collection = mongodb.get_collection("portfolio_holdings")
        
        if client_id:
            holdings = await collection.find({"client_id": client_id}).limit(limit).to_list(length=limit)
        else:
            holdings = await collection.find().limit(limit).to_list(length=limit)
            
        return {"holdings": holdings, "count": len(holdings)}
        
    except Exception as e:
        logger.error(f"Get holdings error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/relationship-managers")
async def get_relationship_managers(current_user: dict = Depends(verify_token)):
    """Get relationship manager summary"""
    try:
        pipeline = [
            {"$group": {
                "_id": "$relationship_manager_id",
                "manager_name": {"$first": "$relationship_manager_name"},
                "client_count": {"$sum": 1},
                "total_aum": {"$sum": "$total_portfolio_value"},
                "avg_portfolio_value": {"$avg": "$total_portfolio_value"}
            }},
            {"$sort": {"total_aum": -1}}
        ]
        
        collection = mongodb.get_collection("clients")
        managers = await collection.aggregate(pipeline).to_list(length=100)
        
        return {"relationship_managers": managers, "count": len(managers)}
        
    except Exception as e:
        logger.error(f"Get RMs error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reset-data")
async def reset_all_data(current_user: dict = Depends(verify_token)):
    """Reset all data (use with caution)"""
    try:
        # Only allow admin users
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Clear MongoDB collections
        clients_collection = mongodb.get_collection("clients")
        await clients_collection.delete_many({})
        
        holdings_collection = mongodb.get_collection("portfolio_holdings")
        await holdings_collection.delete_many({})
        
        # Clear MySQL tables
        await mysql_db.execute_query("DELETE FROM transactions")
        
        return DataResponse(
            message="All data reset successfully",
            count=0
        )
        
    except Exception as e:
        logger.error(f"Data reset error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
