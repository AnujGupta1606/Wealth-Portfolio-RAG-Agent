"""
Sample domain knowledge for ChromaDB vector store
"""

DOMAIN_KNOWLEDGE = [
    {
        "id": "knowledge_001",
        "content": "Wealth management for high-net-worth individuals requires a comprehensive approach that includes asset allocation, risk management, tax optimization, and estate planning. For film stars and sports personalities, additional considerations include irregular income patterns, career longevity risks, and public image management.",
        "metadata": {
            "category": "wealth_management_basics",
            "relevance": "general",
            "source": "internal_guidelines"
        }
    },
    {
        "id": "knowledge_002", 
        "content": "Asset allocation for celebrities should typically include: 40-60% equity investments (diversified across large-cap, mid-cap, and international markets), 20-30% fixed income securities (government bonds, corporate bonds, FDs), 10-20% alternative investments (real estate, private equity), and 5-10% liquid assets for immediate needs.",
        "metadata": {
            "category": "asset_allocation",
            "relevance": "portfolio_construction",
            "source": "investment_strategy"
        }
    },
    {
        "id": "knowledge_003",
        "content": "Risk tolerance assessment for entertainment industry professionals must consider career volatility, age, income stability, and future earning potential. Young athletes (20-30 years) can typically handle aggressive portfolios with 70-80% equity allocation, while established film stars (40+ years) may prefer moderate allocations with 50-60% equity.",
        "metadata": {
            "category": "risk_assessment",
            "relevance": "client_profiling", 
            "source": "risk_management_framework"
        }
    },
    {
        "id": "knowledge_004",
        "content": "Tax optimization strategies for high-income individuals include: ELSS mutual funds for 80C deductions (up to 1.5 lakh), NPS contributions for additional 50k deduction under 80CCD(1B), tax-efficient debt instruments, and strategic asset location between taxable and tax-advantaged accounts.",
        "metadata": {
            "category": "tax_planning",
            "relevance": "tax_optimization",
            "source": "tax_advisory"
        }
    },
    {
        "id": "knowledge_005",
        "content": "Real estate investments should not exceed 25-30% of total portfolio for liquidity reasons. Commercial properties in metro cities like Mumbai, Delhi, Bangalore offer better rental yields (4-6%) compared to residential properties (2-3%). REITs provide exposure to real estate with better liquidity.",
        "metadata": {
            "category": "real_estate",
            "relevance": "alternative_investments",
            "source": "real_estate_guidelines"
        }
    },
    {
        "id": "knowledge_006",
        "content": "Emergency fund requirements for celebrities should be 12-18 months of expenses (higher than standard 6 months) due to irregular income patterns. This fund should be kept in liquid instruments like savings accounts, liquid mutual funds, or short-term FDs.",
        "metadata": {
            "category": "liquidity_management",
            "relevance": "cash_planning",
            "source": "liquidity_framework"
        }
    },
    {
        "id": "knowledge_007",
        "content": "International diversification is crucial for high-net-worth clients. Recommended allocation: 10-20% in international equity funds or direct foreign stocks, focusing on developed markets (US, Europe) and emerging markets (China, other Asian markets) for geographic diversification.",
        "metadata": {
            "category": "international_investing",
            "relevance": "diversification",
            "source": "global_investment_strategy"
        }
    },
    {
        "id": "knowledge_008",
        "content": "Cryptocurrency allocation should be limited to 2-5% of total portfolio due to high volatility. Bitcoin and Ethereum are considered relatively stable crypto assets. Clients should understand the regulatory risks and tax implications of crypto investments in India.",
        "metadata": {
            "category": "cryptocurrency",
            "relevance": "alternative_investments",
            "source": "crypto_investment_guidelines"
        }
    },
    {
        "id": "knowledge_009",
        "content": "Insurance requirements for celebrities include: Term life insurance (10-15x annual income), health insurance with high coverage (minimum 1 crore), disability insurance for income protection, and umbrella liability insurance for public figures. Key person insurance may be relevant for those with business ventures.",
        "metadata": {
            "category": "insurance_planning",
            "relevance": "risk_protection",
            "source": "insurance_framework"
        }
    },
    {
        "id": "knowledge_010",
        "content": "Estate planning essentials include will preparation, nomination updates across all investments, trust structures for tax efficiency and asset protection, power of attorney documentation, and succession planning for any business interests.",
        "metadata": {
            "category": "estate_planning",
            "relevance": "wealth_transfer",
            "source": "estate_planning_guidelines"
        }
    },
    {
        "id": "knowledge_011",
        "content": "Performance benchmarking should compare portfolio returns against relevant indices: Nifty 50 for large-cap equity, Nifty Midcap 100 for mid-cap exposure, and CRISIL Composite Bond Fund Index for debt portions. Alpha generation and risk-adjusted returns (Sharpe ratio) are key metrics.",
        "metadata": {
            "category": "performance_measurement",
            "relevance": "portfolio_analytics",
            "source": "performance_framework"
        }
    },
    {
        "id": "knowledge_012",
        "content": "Rebalancing frequency should be quarterly for active portfolios or when asset allocation drifts beyond +/- 5% from target allocation. Tax-loss harvesting opportunities should be considered during rebalancing, especially in equity positions.",
        "metadata": {
            "category": "portfolio_management",
            "relevance": "rebalancing_strategy",
            "source": "portfolio_management_guidelines"
        }
    },
    {
        "id": "knowledge_013",
        "content": "ESG (Environmental, Social, Governance) investing is increasingly important for public figures. ESG-focused mutual funds and stocks can provide competitive returns while aligning with sustainable and socially responsible values, which can enhance public image.",
        "metadata": {
            "category": "esg_investing",
            "relevance": "sustainable_investing",
            "source": "esg_investment_framework"
        }
    },
    {
        "id": "knowledge_014",
        "content": "Cash flow management for irregular income requires sophisticated planning. Recommend maintaining higher cash reserves, using systematic withdrawal plans from mutual funds for regular income, and considering dividend-yielding stocks for steady cash flow.",
        "metadata": {
            "category": "cash_flow_planning",
            "relevance": "income_management",
            "source": "cash_flow_framework"
        }
    },
    {
        "id": "knowledge_015",
        "content": "Due diligence for direct equity investments should include fundamental analysis (P/E ratios, debt-to-equity, ROE, revenue growth), technical analysis for entry/exit timing, and sector-specific considerations. Avoid concentration risk by limiting single stock exposure to maximum 5-8% of equity portfolio.",
        "metadata": {
            "category": "equity_analysis",
            "relevance": "stock_selection",
            "source": "equity_research_guidelines"
        }
    }
]
