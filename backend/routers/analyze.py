"""
Risk analysis endpoints using AWS Bedrock
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

from services.bedrock_client import bedrock_client
from services.s3_client import s3_client
from services.vanta_client import vanta_client
from core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class KYCAnalysisRequest(BaseModel):
    customer_id: str
    name: str
    date_of_birth: str
    address: str
    occupation: str
    annual_income: float
    source_of_funds: str
    pep_status: str = "No"
    sanctions_check: str = "Clear"

class TransactionAnalysisRequest(BaseModel):
    transaction_id: str
    amount: float
    currency: str = "USD"
    transaction_type: str
    date: str
    origin: str
    destination: str
    customer_id: str
    purpose: str

class AnalysisResponse(BaseModel):
    analysis_id: str
    risk_level: str
    risk_score: int
    risk_factors: List[str]
    recommendations: List[str]
    compliance_notes: List[str]  # <-- THE ONLY CHANGE IS HERE
    analysis_summary: str
    timestamp: str
    compliance_status: str

@router.post("/kyc", response_model=AnalysisResponse)
async def analyze_kyc_profile(request: KYCAnalysisRequest):
    """
    Analyze KYC profile for risk assessment using Claude 3 Sonnet 4
    """
    try:
        logger.info(f"Starting KYC analysis for customer: {request.customer_id}")
        
        # Check compliance posture first (bypass in debug mode)
        compliance_status = {"status": "bypassed_in_debug"}
        if not settings.DEBUG:
            compliance_status = await vanta_client.check_compliance_posture()
        
        # Convert request to dict for analysis
        kyc_data = request.dict()
        
        # Perform AI analysis
        analysis_result = await bedrock_client.analyze_kyc_profile(kyc_data)
        
        # Create analysis response
        analysis_response = AnalysisResponse(
            analysis_id=f"KYC-{datetime.now().strftime('%Y%m%d')}-{request.customer_id}",
            risk_level=analysis_result.get("risk_level", "MEDIUM"),
            risk_score=analysis_result.get("risk_score", 50),
            risk_factors=analysis_result.get("risk_factors", []),
            recommendations=analysis_result.get("recommendations", []),
            compliance_notes=analysis_result.get("compliance_notes", []),
            analysis_summary=analysis_result.get("analysis_summary", ""),
            timestamp=datetime.now().isoformat(),
            compliance_status=compliance_status.get("status", "unknown")
        )
        
        # Store analysis report in S3
        await s3_client.store_analysis_report(
            analysis_data=analysis_result,
            report_type="kyc_analysis",
            customer_id=request.customer_id
        )
        
        # Create audit log
        await s3_client.create_audit_log(
            action="kyc_analysis",
            details={
                "customer_id": request.customer_id,
                "risk_level": analysis_response.risk_level,
                "risk_score": analysis_response.risk_score
            },
            user_id="system"
        )
        
        logger.info(f"KYC analysis completed for customer: {request.customer_id}")
        return analysis_response
        
    except Exception as e:
        logger.error(f"Error in KYC analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"KYC analysis failed: {str(e)}"
        )

@router.post("/transaction", response_model=AnalysisResponse)
async def analyze_transaction(request: TransactionAnalysisRequest):
    """
    Analyze transaction for suspicious activity using Claude 3 Sonnet 4
    """
    try:
        logger.info(f"Starting transaction analysis for transaction: {request.transaction_id}")
        
        # Check compliance posture first (bypass in debug mode)
        compliance_status = {"status": "bypassed_in_debug"}
        if not settings.DEBUG:
            compliance_status = await vanta_client.check_compliance_posture()
        
        # Convert request to dict for analysis
        transaction_data = request.dict()
        
        # Perform AI analysis
        analysis_result = await bedrock_client.analyze_transaction(transaction_data)
        
        # Create analysis response
        analysis_response = AnalysisResponse(
            analysis_id=f"TXN-{datetime.now().strftime('%Y%m%d')}-{request.transaction_id}",
            risk_level=analysis_result.get("suspicion_level", "MEDIUM"),
            risk_score=analysis_result.get("suspicion_score", 50),
            risk_factors=analysis_result.get("red_flags", []),
            recommendations=analysis_result.get("recommendations", []),
            compliance_notes=analysis_result.get("aml_concerns", []),
            analysis_summary=analysis_result.get("analysis_summary", ""),
            timestamp=datetime.now().isoformat(),
            compliance_status=compliance_status.get("status", "unknown")
        )
        
        # Store analysis report in S3
        await s3_client.store_analysis_report(
            analysis_data=analysis_result,
            report_type="transaction_analysis",
            customer_id=request.customer_id
        )
        
        # Create audit log
        await s3_client.create_audit_log(
            action="transaction_analysis",
            details={
                "transaction_id": request.transaction_id,
                "customer_id": request.customer_id,
                "suspicion_level": analysis_response.risk_level,
                "suspicion_score": analysis_response.risk_score
            },
            user_id="system"
        )
        
        logger.info(f"Transaction analysis completed for transaction: {request.transaction_id}")
        return analysis_response
        
    except Exception as e:
        logger.error(f"Error in transaction analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transaction analysis failed: {str(e)}"
        )

@router.post("/comprehensive")
async def comprehensive_analysis(
    kyc_request: KYCAnalysisRequest,
    transaction_requests: List[TransactionAnalysisRequest]
):
    """
    Perform comprehensive analysis combining KYC and transaction data
    """
    try:
        logger.info(f"Starting comprehensive analysis for customer: {kyc_request.customer_id}")
        
        # Check compliance posture first (bypass in debug mode)
        compliance_status = {"status": "bypassed_in_debug"}
        if not settings.DEBUG:
            compliance_status = await vanta_client.check_compliance_posture()
        
        # Perform KYC analysis
        kyc_analysis = await bedrock_client.analyze_kyc_profile(kyc_request.dict())
        
        # Perform transaction analyses
        transaction_analyses = []
        for txn_request in transaction_requests:
            txn_analysis = await bedrock_client.analyze_transaction(txn_request.dict())
            transaction_analyses.append(txn_analysis)
        
        # Generate comprehensive SAR if high risk detected
        sar_data = None
        if (kyc_analysis.get("risk_level") == "HIGH" or 
            any(txn.get("suspicion_level") == "HIGH" for txn in transaction_analyses)):
            
            sar_data = await bedrock_client.generate_sar({
                "kyc_analysis": kyc_analysis,
                "transaction_analyses": transaction_analyses,
                "customer_id": kyc_request.customer_id
            })
            
            # Store SAR in S3
            await s3_client.store_sar(sar_data, kyc_request.customer_id)
        
        # Create comprehensive response
        comprehensive_response = {
            "analysis_id": f"COMP-{datetime.now().strftime('%Y%m%d')}-{kyc_request.customer_id}",
            "customer_id": kyc_request.customer_id,
            "kyc_analysis": kyc_analysis,
            "transaction_analyses": transaction_analyses,
            "sar_generated": sar_data is not None,
            "sar_data": sar_data,
            "compliance_status": compliance_status,
            "timestamp": datetime.now().isoformat(),
            "overall_risk_level": "HIGH" if sar_data else "MEDIUM" if any(
                txn.get("suspicion_level") == "MEDIUM" for txn in transaction_analyses
            ) else "LOW"
        }
        
        # Store comprehensive report in S3
        await s3_client.store_analysis_report(
            analysis_data=comprehensive_response,
            report_type="comprehensive_analysis",
            customer_id=kyc_request.customer_id
        )
        
        # Create audit log
        await s3_client.create_audit_log(
            action="comprehensive_analysis",
            details={
                "customer_id": kyc_request.customer_id,
                "sar_generated": sar_data is not None,
                "overall_risk_level": comprehensive_response["overall_risk_level"]
            },
            user_id="system"
        )
        
        logger.info(f"Comprehensive analysis completed for customer: {kyc_request.customer_id}")
        return comprehensive_response
        
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comprehensive analysis failed: {str(e)}"
        )

@router.get("/status")
async def get_analysis_status():
    """
    Get current analysis service status
    """
    return {
        "service": "Risk Analysis",
        "status": "operational",
        "model": "Claude 3 Sonnet 4",
        "provider": "AWS Bedrock",
        "timestamp": datetime.now().isoformat()
    }
