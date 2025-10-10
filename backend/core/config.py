"""
Configuration settings for FinTrust AI
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "FinTrust AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # AWS Configuration
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # Bedrock API Key (Bearer Token)
    AWS_BEARER_TOKEN_BEDROCK: Optional[str] = None
    
    # Vanta API
    VANTA_CLIENT_ID: str
    VANTA_CLIENT_SECRET: str
    VANTA_API_BASE_URL: str = "https://api.vanta.com/v1"
    VANTA_REDIRECT_URI: str = "http://localhost:8000/auth/vanta/callback"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # S3 Configuration
    S3_BUCKET_NAME: str = "fintrust-ai-reports"
    KMS_KEY_ID: Optional[str] = None
    
    # CloudWatch
    CLOUDWATCH_LOG_GROUP: str = "fintrust-ai-logs"
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID: str = "us.anthropic.claude-sonnet-4-20250514-v1:0"
    BEDROCK_MAX_TOKENS: int = 4000
    BEDROCK_TEMPERATURE: float = 0.1
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
