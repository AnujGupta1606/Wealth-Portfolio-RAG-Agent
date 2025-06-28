"""Analytics and reporting router"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import logging

from app.database import mongodb, mysql_db
from app.routers.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

class AnalyticsRequest(BaseModel):
    metric: str
    filters: Optional[Dict[str, Any]] = {}
    date_range: Optional[Dict[str, str]] = {}

class AnalyticsResponse(BaseModel):
    metric: str
    data: Dict[str, Any]
    summary: Dict[str, Any]
    chart_config: Optional[Dict[str, Any]] = None

@router.get("/portfolio-summary")
async def get_portfolio_summary(current_user: dict = Depends(verify_token)):
    """Get overall portfolio summary"""
    try:
        # Get client summary from MongoDB
        pipeline = [
            {"$group": {
                "_id": None,
                "total_clients": {"$sum": 1},
                "total_aum": {"$sum": "$total_portfolio_value"},
                "avg_portfolio_value": {"$avg": "$total_portfolio_value"},
                "film_stars": {"$sum": {"$cond": [{"$eq": ["$type", "Film Star"]}, 1, 0]}},
                "sports_personalities": {"$sum": {"$cond": [{"$eq": ["$type", "Sports Personality"]}, 1, 0]}}
            }}
        ]
        
        collection = mongodb.get_collection("clients")
        result = await collection.aggregate(pipeline).to_list(length=1)
        summary = result[0] if result else {}
        
        # Get risk distribution
        risk_pipeline = [
            {"$group": {
                "_id": "$risk_appetite",
                "count": {"$sum": 1},
                "total_value": {"$sum": "$total_portfolio_value"}
            }}
        ]
        risk_dist = await collection.aggregate(risk_pipeline).to_list(length=10)
        
        # Get RM performance
        rm_pipeline = [
            {"$group": {
                "_id": "$relationship_manager_id",
                "manager_name": {"$first": "$relationship_manager_name"},
                "client_count": {"$sum": 1},
                "total_aum": {"$sum": "$total_portfolio_value"}
            }},
            {"$sort": {"total_aum": -1}}
        ]
        rm_performance = await collection.aggregate(rm_pipeline).to_list(length=10)
        
        return {
            "summary": summary,
            "risk_distribution": risk_dist,
            "rm_performance": rm_performance,
            "charts": {
                "risk_distribution": {
                    "type": "pie",
                    "title": "Portfolio Distribution by Risk Appetite",
                    "data": {
                        "labels": [item["_id"] for item in risk_dist],
                        "datasets": [{
                            "data": [item["total_value"] / 10000000 for item in risk_dist],
                            "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56"]
                        }]
                    }
                },
                "rm_performance": {
                    "type": "bar",
                    "title": "Assets Under Management by Relationship Manager",
                    "data": {
                        "labels": [rm["manager_name"] for rm in rm_performance],
                        "datasets": [{
                            "label": "AUM (₹ Crores)",
                            "data": [rm["total_aum"] / 10000000 for rm in rm_performance],
                            "backgroundColor": "rgba(54, 162, 235, 0.6)"
                        }]
                    }
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Portfolio summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-performers")
async def get_top_performers(
    limit: int = 10,
    current_user: dict = Depends(verify_token)
):
    """Get top performing portfolios"""
    try:
        # Top portfolios by value
        collection = mongodb.get_collection("clients")
        top_portfolios = await collection.find().sort("total_portfolio_value", -1).limit(limit).to_list(length=limit)
        
        # Top relationship managers
        rm_pipeline = [
            {"$group": {
                "_id": "$relationship_manager_id",
                "manager_name": {"$first": "$relationship_manager_name"},
                "total_aum": {"$sum": "$total_portfolio_value"},
                "client_count": {"$sum": 1},
                "avg_portfolio_value": {"$avg": "$total_portfolio_value"}
            }},
            {"$sort": {"total_aum": -1}},
            {"$limit": limit}
        ]
        top_rms = await collection.aggregate(rm_pipeline).to_list(length=limit)
        
        # Top stock holdings
        holdings_collection = mongodb.get_collection("portfolio_holdings")
        stock_pipeline = [
            {"$group": {
                "_id": "$stock_symbol",
                "stock_name": {"$first": "$stock_name"},
                "total_value": {"$sum": "$current_value"},
                "total_quantity": {"$sum": "$quantity"},
                "holder_count": {"$sum": 1}
            }},
            {"$sort": {"total_value": -1}},
            {"$limit": limit}
        ]
        top_stocks = await holdings_collection.aggregate(stock_pipeline).to_list(length=limit)
        
        return {
            "top_portfolios": top_portfolios,
            "top_rms": top_rms,
            "top_stocks": top_stocks,
            "charts": {
                "top_portfolios": {
                    "type": "bar",
                    "title": f"Top {limit} Portfolios by Value",
                    "data": {
                        "labels": [p["name"] for p in top_portfolios],
                        "datasets": [{
                            "label": "Portfolio Value (₹ Crores)",
                            "data": [p["total_portfolio_value"] / 10000000 for p in top_portfolios],
                            "backgroundColor": "rgba(75, 192, 192, 0.6)"
                        }]
                    }
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Top performers error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stock-analysis/{stock_symbol}")
async def get_stock_analysis(
    stock_symbol: str,
    current_user: dict = Depends(verify_token)
):
    """Analyze specific stock holdings across all clients"""
    try:
        # Get holdings data
        holdings_collection = mongodb.get_collection("portfolio_holdings")
        holdings = await holdings_collection.find({"stock_symbol": stock_symbol.upper()}).to_list(length=100)
        
        if not holdings:
            raise HTTPException(status_code=404, detail=f"No holdings found for {stock_symbol}")
        
        # Get client details for holders
        client_ids = [h["client_id"] for h in holdings]
        clients_collection = mongodb.get_collection("clients")
        clients = await clients_collection.find({"client_id": {"$in": client_ids}}).to_list(length=100)
        client_map = {c["client_id"]: c for c in clients}
        
        # Get transaction history
        transactions = await mysql_db.execute_query(
            "SELECT * FROM transactions WHERE stock_symbol = %s ORDER BY transaction_date DESC",
            (stock_symbol.upper(),)
        )
        
        # Calculate analytics
        total_value = sum(h["current_value"] for h in holdings)
        total_quantity = sum(h["quantity"] for h in holdings)
        avg_price = sum(h["avg_price"] * h["quantity"] for h in holdings) / total_quantity if total_quantity > 0 else 0
        
        # Holder analysis
        holder_analysis = []
        for holding in holdings:
            client = client_map.get(holding["client_id"], {})
            holder_analysis.append({
                "client_name": client.get("name", "Unknown"),
                "client_type": client.get("type", "Unknown"),
                "quantity": holding["quantity"],
                "value": holding["current_value"],
                "percentage_of_portfolio": (holding["current_value"] / client.get("total_portfolio_value", 1)) * 100 if client.get("total_portfolio_value") else 0
            })
        
        # Sort by value
        holder_analysis.sort(key=lambda x: x["value"], reverse=True)
        
        return {
            "stock_symbol": stock_symbol.upper(),
            "stock_name": holdings[0]["stock_name"] if holdings else "Unknown",
            "summary": {
                "total_value": total_value,
                "total_quantity": total_quantity,
                "avg_price": avg_price,
                "holder_count": len(holdings),
                "transaction_count": len(transactions)
            },
            "top_holders": holder_analysis[:10],
            "recent_transactions": transactions[:20],
            "charts": {
                "holder_distribution": {
                    "type": "pie",
                    "title": f"Top Holders of {stock_symbol}",
                    "data": {
                        "labels": [h["client_name"] for h in holder_analysis[:5]],
                        "datasets": [{
                            "data": [h["value"] / 1000000 for h in holder_analysis[:5]],
                            "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
                        }]
                    }
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Stock analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/client-analysis/{client_id}")
async def get_client_analysis(
    client_id: str,
    current_user: dict = Depends(verify_token)
):
    """Detailed analysis of a specific client"""
    try:
        # Get client profile
        clients_collection = mongodb.get_collection("clients")
        client = await clients_collection.find_one({"client_id": client_id})
        
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        
        # Get portfolio holdings
        holdings_collection = mongodb.get_collection("portfolio_holdings")
        holdings = await holdings_collection.find({"client_id": client_id}).to_list(length=100)
        
        # Get transaction history
        transactions = await mysql_db.execute_query(
            "SELECT * FROM transactions WHERE client_id = %s ORDER BY transaction_date DESC",
            (client_id,)
        )
        
        # Calculate portfolio metrics
        total_holdings_value = sum(h["current_value"] for h in holdings)
        stock_count = len(holdings)
        
        # Asset allocation
        asset_allocation = {}
        for holding in holdings:
            sector = holding.get("sector", "Others")  # You can add sector info to holdings
            asset_allocation[sector] = asset_allocation.get(sector, 0) + holding["current_value"]
        
        return {
            "client": client,
            "portfolio_summary": {
                "total_value": total_holdings_value,
                "stock_count": stock_count,
                "transaction_count": len(transactions)
            },
            "holdings": holdings,
            "recent_transactions": transactions[:20],
            "asset_allocation": asset_allocation,
            "charts": {
                "holdings_distribution": {
                    "type": "pie",
                    "title": f"Portfolio Distribution - {client['name']}",
                    "data": {
                        "labels": [h["stock_name"] for h in holdings[:10]],
                        "datasets": [{
                            "data": [h["current_value"] / 1000000 for h in holdings[:10]],
                            "backgroundColor": [
                                "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
                                "#FF9F40", "#FF6384", "#C9CBCF", "#4BC0C0", "#FF6384"
                            ]
                        }]
                    }
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Client analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/custom-analytics")
async def run_custom_analytics(
    request: AnalyticsRequest,
    current_user: dict = Depends(verify_token)
):
    """Run custom analytics based on metric type"""
    try:
        if request.metric == "risk_analysis":
            return await analyze_risk_distribution(request.filters or {})
        elif request.metric == "performance_trends":
            return await analyze_performance_trends(request.date_range or {})
        elif request.metric == "concentration_risk":
            return await analyze_concentration_risk(request.filters or {})
        else:
            raise HTTPException(status_code=400, detail=f"Unknown metric: {request.metric}")
            
    except Exception as e:
        logger.error(f"Custom analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def analyze_risk_distribution(filters: Dict[str, Any]):
    """Analyze portfolio risk distribution"""
    # Implementation for risk analysis
    collection = mongodb.get_collection("clients")
    pipeline = [
        {"$group": {
            "_id": {
                "risk_appetite": "$risk_appetite",
                "client_type": "$type"
            },
            "count": {"$sum": 1},
            "total_value": {"$sum": "$total_portfolio_value"},
            "avg_value": {"$avg": "$total_portfolio_value"}
        }}
    ]
    results = await collection.aggregate(pipeline).to_list(length=100)
    
    return AnalyticsResponse(
        metric="risk_analysis",
        data={"risk_distribution": results},
        summary={"total_segments": len(results)}
    )

async def analyze_performance_trends(date_range: Dict[str, str]):
    """Analyze performance trends over time"""
    # Implementation for performance trends
    transactions = await mysql_db.execute_query("""
        SELECT DATE(transaction_date) as trade_date, 
               SUM(CASE WHEN transaction_type = 'BUY' THEN total_amount ELSE -total_amount END) as net_flow,
               COUNT(*) as transaction_count
        FROM transactions 
        GROUP BY DATE(transaction_date)
        ORDER BY trade_date DESC
        LIMIT 30
    """)
    
    return AnalyticsResponse(
        metric="performance_trends",
        data={"daily_flows": transactions},
        summary={"days_analyzed": len(transactions)}
    )

async def analyze_concentration_risk(filters: Dict[str, Any]):
    """Analyze concentration risk in portfolios"""
    # Implementation for concentration risk analysis
    holdings_collection = mongodb.get_collection("portfolio_holdings")
    pipeline = [
        {"$group": {
            "_id": "$client_id",
            "holdings": {"$push": {
                "stock_symbol": "$stock_symbol",
                "value": "$current_value"
            }},
            "total_value": {"$sum": "$current_value"},
            "stock_count": {"$sum": 1}
        }}
    ]
    results = await holdings_collection.aggregate(pipeline).to_list(length=100)
    
    return AnalyticsResponse(
        metric="concentration_risk",
        data={"concentration_analysis": results},
        summary={"portfolios_analyzed": len(results)}
    )
