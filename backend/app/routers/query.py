"""Natural language query router with Cohere integration"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging

import cohere
from langchain.memory import ConversationBufferWindowMemory

from app.database import mongodb, mysql_db, vector_store
from app.routers.auth import verify_token
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    include_charts: bool = True

class QueryResponse(BaseModel):
    answer: str
    data: Optional[Dict[str, Any]] = None
    chart_data: Optional[Dict[str, Any]] = None
    conversation_id: str
    sources: List[str] = []

# Memory store for conversations
conversation_memories = {}

# Initialize Cohere client
def get_cohere_client():
    """Get Cohere client instance"""
    return cohere.Client(api_key=settings.COHERE_API_KEY)

async def query_mongodb_data(question: str) -> str:
    """Query MongoDB for relevant data based on the question"""
    try:
        # Parse the question to determine what data to fetch
        question_lower = question.lower()
        
        if "top" in question_lower and "portfolio" in question_lower:
            # Query for top portfolios
            collection = mongodb.get_collection("clients")
            cursor = collection.find().sort("total_portfolio_value", -1).limit(5)
            results = await cursor.to_list(length=5)
            return f"Top portfolios: {json.dumps(results, default=str)}"
        
        elif "relationship manager" in question_lower:
            if "top" in question_lower:
                # Top relationship managers by AUM
                pipeline = [
                    {"$group": {
                        "_id": "$relationship_manager_id",
                        "manager_name": {"$first": "$relationship_manager_name"},
                        "total_aum": {"$sum": "$total_portfolio_value"},
                        "client_count": {"$sum": 1}
                    }},
                    {"$sort": {"total_aum": -1}},
                    {"$limit": 5}
                ]
                collection = mongodb.get_collection("clients")
                results = await collection.aggregate(pipeline).to_list(length=5)
                return f"Top relationship managers: {json.dumps(results, default=str)}"
            else:
                # Portfolio breakup by relationship manager
                pipeline = [
                    {"$group": {
                        "_id": "$relationship_manager_id",
                        "manager_name": {"$first": "$relationship_manager_name"},
                        "total_portfolio_value": {"$sum": "$total_portfolio_value"},
                        "client_count": {"$sum": 1}
                    }},
                    {"$sort": {"total_portfolio_value": -1}}
                ]
                collection = mongodb.get_collection("clients")
                results = await collection.aggregate(pipeline).to_list(length=10)
                return f"Portfolio distribution by RM: {json.dumps(results, default=str)}"
        
        elif "portfolio" in question_lower:
            # General portfolio query
            collection = mongodb.get_collection("clients")
            cursor = collection.find().limit(10)
            results = await cursor.to_list(length=10)
            return f"Portfolio data: {json.dumps(results, default=str)}"
        
        return "No relevant MongoDB data found"
        
    except Exception as e:
        logger.error(f"MongoDB query error: {e}")
        return f"Error querying MongoDB: {str(e)}"

async def query_mysql_data(question: str) -> str:
    """Query MySQL for relevant transaction data"""
    try:
        question_lower = question.lower()
        
        if "transaction" in question_lower or "trading" in question_lower:
            cursor = await mysql_db.execute_query(
                "SELECT client_id, transaction_type, amount, transaction_date FROM transactions ORDER BY transaction_date DESC LIMIT 10"
            )
            results = await cursor.fetchall()
            return f"Recent transactions: {json.dumps(results, default=str)}"
        
        elif "volume" in question_lower:
            cursor = await mysql_db.execute_query(
                "SELECT transaction_type, SUM(amount) as total_volume FROM transactions GROUP BY transaction_type"
            )
            results = await cursor.fetchall()
            return f"Transaction volumes: {json.dumps(results, default=str)}"
        
        return "No relevant MySQL data found"
        
    except Exception as e:
        logger.error(f"MySQL query error: {e}")
        return f"Error querying MySQL: {str(e)}"

async def generate_ai_response(question: str, context: str, database_data: str) -> str:
    """Generate AI response using Cohere"""
    try:
        client = get_cohere_client()
        
        prompt = f"""
You are an expert wealth management analyst for a high-net-worth asset management firm. 
You help analyze portfolios for film stars and sports personalities who have invested 100+ crores.

Context from knowledge base:
{context}

Relevant data from databases:
{database_data}

Question: {question}

Please provide a comprehensive answer that:
1. Analyzes the relevant data from the context and databases
2. Presents the information in a clear, business-friendly format
3. Includes specific numbers and insights where relevant
4. Suggests actionable recommendations when appropriate

Answer:
"""
        
        response = client.generate(
            model=settings.LLM_MODEL,
            prompt=prompt,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE
        )
        
        if response and response.generations and len(response.generations) > 0:
            return response.generations[0].text.strip()
        else:
            return "I apologize, but I couldn't generate a response. Please try again."
        
    except Exception as e:
        logger.error(f"Cohere API error: {e}")
        return f"I apologize, but I encountered an error while processing your question. Please try again later. Error: {str(e)}"

@router.post("/ask", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    current_user: dict = Depends(verify_token)
):
    """Process natural language query"""
    try:
        # Get or create conversation memory
        if request.conversation_id and request.conversation_id in conversation_memories:
            memory = conversation_memories[request.conversation_id]
        else:
            conversation_id = f"conv_{len(conversation_memories) + 1}"
            memory = ConversationBufferWindowMemory(k=5, return_messages=True)
            conversation_memories[conversation_id] = memory
            request.conversation_id = conversation_id
        
        # Get relevant context from vector store
        context = ""
        try:
            if vector_store.vectorstore:
                retriever = vector_store.vectorstore.as_retriever(k=3)
                relevant_docs = retriever.get_relevant_documents(request.question)
                context = "\n".join([doc.page_content for doc in relevant_docs])
            else:
                context = "Vector store not initialized"
        except Exception as e:
            logger.warning(f"Vector store query failed: {e}")
            context = "No vector store context available"
        
        # Query relevant data from databases
        mongodb_data = await query_mongodb_data(request.question)
        mysql_data = await query_mysql_data(request.question)
        database_data = f"MongoDB: {mongodb_data}\nMySQL: {mysql_data}"
        
        # Generate AI response
        answer_text = await generate_ai_response(request.question, context, database_data)
        
        # Extract data for charts (simplified)
        chart_data = None
        if request.include_charts:
            chart_data = await generate_chart_data(request.question)
        
        return QueryResponse(
            answer=answer_text,
            chart_data=chart_data,
            conversation_id=request.conversation_id,
            sources=["MongoDB", "MySQL", "Knowledge Base"]
        )
        
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")

async def generate_chart_data(question: str) -> Optional[Dict[str, Any]]:
    """Generate chart data based on the question"""
    try:
        if "portfolio" in question.lower() and "top" in question.lower():
            # Generate data for top portfolios chart
            collection = mongodb.get_collection("clients")
            cursor = collection.find().sort("total_portfolio_value", -1).limit(5)
            results = await cursor.to_list(length=5)
            
            return {
                "type": "bar",
                "title": "Top 5 Portfolios by Value",
                "data": {
                    "labels": [client["name"] for client in results],
                    "datasets": [{
                        "label": "Portfolio Value (₹ Crores)",
                        "data": [client["total_portfolio_value"] / 10000000 for client in results],
                        "backgroundColor": "rgba(54, 162, 235, 0.6)"
                    }]
                }
            }
        
        elif "relationship manager" in question.lower():
            # Generate data for RM performance
            pipeline = [
                {"$group": {
                    "_id": "$relationship_manager_id",
                    "manager_name": {"$first": "$relationship_manager_name"},
                    "total_aum": {"$sum": "$total_portfolio_value"},
                    "client_count": {"$sum": 1}
                }},
                {"$sort": {"total_aum": -1}}
            ]
            collection = mongodb.get_collection("clients")
            results = await collection.aggregate(pipeline).to_list(length=10)
            
            return {
                "type": "pie",
                "title": "Portfolio Distribution by Relationship Manager",
                "data": {
                    "labels": [rm["manager_name"] for rm in results],
                    "datasets": [{
                        "data": [rm["total_aum"] / 10000000 for rm in results],
                        "backgroundColor": [
                            "rgba(255, 99, 132, 0.6)",
                            "rgba(54, 162, 235, 0.6)", 
                            "rgba(255, 205, 86, 0.6)",
                            "rgba(75, 192, 192, 0.6)",
                            "rgba(153, 102, 255, 0.6)"
                        ]
                    }]
                }
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Chart generation error: {e}")
        return None

@router.get("/conversations")
async def get_conversations(current_user: dict = Depends(verify_token)):
    """Get list of conversation IDs"""
    return {"conversations": list(conversation_memories.keys())}

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: dict = Depends(verify_token)
):
    """Delete a conversation"""
    if conversation_id in conversation_memories:
        del conversation_memories[conversation_id]
        return {"message": "Conversation deleted"}
    raise HTTPException(status_code=404, detail="Conversation not found")
