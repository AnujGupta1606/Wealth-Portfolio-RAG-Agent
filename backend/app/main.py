from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import query, analytics, auth, data
from app.database import mongodb, mysql_db, vector_store
from app.core.exceptions import setup_exception_handlers
from app.middleware.logging import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Wealth Portfolio RAG Agent...")
    
    # Initialize databases
    await mongodb.connect()
    await mysql_db.connect()
    await vector_store.initialize()
    
    print("✅ All systems ready!")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down...")
    await mongodb.disconnect()
    await mysql_db.disconnect()
    print("✅ Shutdown complete!")

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A LangChain-powered system for natural language queries on wealth portfolio data",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Setup middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging and exception handlers
setup_logging()
setup_exception_handlers(app)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(query.router, prefix=f"{settings.API_V1_STR}/query", tags=["query"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(data.router, prefix=f"{settings.API_V1_STR}/data", tags=["data"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Wealth Portfolio RAG Agent",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mongodb": await mongodb.health_check(),
        "mysql": await mysql_db.health_check(),
        "vector_store": await vector_store.health_check()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
