import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import settings
import logging
import os

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.chroma_client = None
        self.collection = None
        self.embeddings = None
        self.vectorstore = None
        
    async def initialize(self):
        """Initialize ChromaDB vector store"""
        try:
            # Initialize embeddings
            self.embeddings = SentenceTransformerEmbeddings(
                model_name=settings.EMBEDDING_MODEL
            )
            
            # Create persist directory if it doesn't exist
            os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
            
            # Initialize ChromaDB
            self.chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY
            )
            
            # Create or get collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="wealth_portfolio_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            
            # Initialize Langchain Chroma wrapper
            self.vectorstore = Chroma(
                client=self.chroma_client,
                collection_name="wealth_portfolio_knowledge",
                embedding_function=self.embeddings,
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY
            )
            
            logger.info("✅ Vector store initialized")
            
            # Add domain knowledge if collection is empty
            if self.collection.count() == 0:
                await self.add_domain_knowledge()
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize vector store: {e}")
            raise
    
    async def health_check(self):
        """Check vector store health"""
        try:
            if self.collection:
                count = self.collection.count()
                return {
                    "status": "healthy", 
                    "database": "chromadb",
                    "documents": count
                }
            return {"status": "disconnected", "database": "chromadb"}
        except Exception as e:
            return {"status": "unhealthy", "database": "chromadb", "error": str(e)}
    
    async def add_domain_knowledge(self):
        """Add wealth management domain knowledge to vector store"""
        
        domain_knowledge = [
            {
                "content": """
                Wealth Portfolio Management for High Net Worth Individuals:
                
                Our firm specializes in managing investment portfolios for film stars and sports personalities 
                with investments exceeding 100 crores. We provide comprehensive wealth management services 
                including portfolio construction, risk management, and relationship management.
                
                Key Services:
                - Portfolio diversification across asset classes
                - Risk assessment and appetite management  
                - Regular portfolio rebalancing
                - Tax optimization strategies
                - Dedicated relationship manager support
                """,
                "metadata": {"type": "service_overview", "category": "wealth_management"}
            },
            {
                "content": """
                Client Risk Profiles:
                
                Conservative: Clients who prefer stable returns with minimal risk. Typically invest in 
                fixed deposits, government bonds, and blue-chip stocks. Risk tolerance is low.
                
                Moderate: Clients who balance risk and return. Portfolio includes mix of equity, 
                mutual funds, and debt instruments. Medium risk tolerance.
                
                Aggressive: Clients seeking higher returns and willing to take higher risks. 
                Investments include growth stocks, derivatives, international markets, and alternative investments.
                """,
                "metadata": {"type": "risk_management", "category": "client_profiling"}
            },
            {
                "content": """
                Investment Categories and Asset Classes:
                
                Equity: Stocks of listed companies, both large-cap and mid-cap
                Mutual Funds: Diversified equity and debt mutual funds
                Fixed Deposits: Bank FDs and corporate FDs for stability
                Bonds: Government and corporate bonds
                Gold: Physical gold and gold ETFs
                Real Estate: Direct property investments and REITs
                Derivatives: Options and futures for hedging
                International Stocks: Global diversification
                Cryptocurrency: Digital assets (for aggressive investors)
                """,
                "metadata": {"type": "investment_products", "category": "asset_classes"}
            },
            {
                "content": """
                Key Performance Metrics for Portfolio Analysis:
                
                Total Portfolio Value: Sum of all investments across asset classes
                Asset Allocation: Percentage distribution across different investment types
                Portfolio Returns: Absolute and percentage returns over time periods
                Risk-Adjusted Returns: Sharpe ratio and other risk metrics
                Diversification Ratio: Measure of portfolio diversification
                Concentration Risk: Exposure to single stocks or sectors
                
                Relationship Manager Metrics:
                - Total Assets Under Management (AUM)
                - Number of clients managed
                - Portfolio performance across clients
                - Client satisfaction scores
                """,
                "metadata": {"type": "analytics", "category": "performance_metrics"}
            },
            {
                "content": """
                Common Query Types and Business Intelligence:
                
                Top Performers: Identify highest performing portfolios, clients, or relationship managers
                Risk Analysis: Analyze risk distribution across portfolios and client segments
                Asset Allocation: Understand investment distribution patterns
                Client Segmentation: Group clients by various attributes (type, risk appetite, portfolio size)
                Stock Holdings: Analyze holdings of specific stocks across all clients
                Performance Trends: Track portfolio performance over time
                Relationship Manager Performance: Evaluate RM effectiveness and client management
                """,
                "metadata": {"type": "business_intelligence", "category": "query_patterns"}
            },
            {
                "content": """
                Database Schema and Data Structure:
                
                MongoDB Collections:
                - clients: Client profile information including personal details, risk appetite, and preferences
                - portfolio_holdings: Current stock holdings with quantities and values
                
                MySQL Tables:  
                - transactions: All buy/sell transactions with details like stock, quantity, price, date
                
                Key Fields:
                - client_id: Unique identifier for each client
                - relationship_manager_id: RM assigned to client
                - stock_symbol: Stock ticker symbol
                - portfolio_value: Total investment value
                - risk_appetite: Conservative/Moderate/Aggressive
                """,
                "metadata": {"type": "data_structure", "category": "technical"}
            }
        ]
        
        try:
            # Convert to LangChain documents
            documents = []
            for knowledge in domain_knowledge:
                doc = Document(
                    page_content=knowledge["content"],
                    metadata=knowledge["metadata"]
                )
                documents.append(doc)
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            split_docs = text_splitter.split_documents(documents)
            
            # Add to vector store
            self.vectorstore.add_documents(split_docs)
            
            logger.info(f"✅ Added {len(split_docs)} knowledge chunks to vector store")
            
        except Exception as e:
            logger.error(f"❌ Failed to add domain knowledge: {e}")
    
    def similarity_search(self, query: str, k: int = 5):
        """Search for similar documents"""
        if self.vectorstore:
            return self.vectorstore.similarity_search(query, k=k)
        return []
    
    def as_retriever(self, k: int = 5):
        """Get retriever interface"""
        if self.vectorstore:
            return self.vectorstore.as_retriever(search_kwargs={"k": k})
        return None
