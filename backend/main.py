"""
FinTrust AI - Secure FinTech Compliance Copilot
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

from routers import analyze, vanta, audit, auth
from core.config import settings
from core.logging_config import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting FinTrust AI - Secure FinTech Compliance Copilot")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"AWS Region: {settings.AWS_REGION}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down FinTrust AI")

# Create FastAPI app
app = FastAPI(
    title="FinTrust AI",
    description="Secure FinTech Compliance Copilot using AWS Bedrock and Vanta API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analyze.router, prefix="/analyze", tags=["Risk Analysis"])
app.include_router(vanta.router, prefix="/vanta", tags=["Compliance"])
app.include_router(audit.router, prefix="/audit", tags=["Audit & Reports"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FinTrust AI - Secure FinTech Compliance Copilot",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "AWS Bedrock Claude 3 Sonnet 4 integration",
            "Vanta API compliance verification",
            "Real-time risk assessment",
            "SAR generation and storage",
            "Full audit trail with CloudTrail"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "api": "operational",
            "bedrock": "checking...",
            "vanta": "checking...",
            "s3": "checking..."
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
