"""
Vanta API integration endpoints for compliance verification
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request, Query
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import secrets

from services.vanta_client import vanta_client

logger = logging.getLogger(__name__)
router = APIRouter()

# Store OAuth state for security
oauth_states = {}

@router.get("/auth/authorize")
async def authorize_vanta():
    """
    Initiate OAuth 2.0 authorization with Vanta
    """
    try:
        # Generate a random state parameter for security
        state = secrets.token_urlsafe(32)
        oauth_states[state] = datetime.now()
        
        # Get authorization URL
        auth_url = vanta_client.get_authorization_url(state)
        
        return {
            "status": "success",
            "authorization_url": auth_url,
            "state": state,
            "message": "Visit the authorization URL to grant access to Vanta"
        }
        
    except Exception as e:
        logger.error(f"Error initiating Vanta authorization: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate authorization: {str(e)}"
        )

@router.get("/auth/callback")
async def vanta_callback(
    code: str = Query(..., description="Authorization code from Vanta"),
    state: str = Query(..., description="State parameter for security")
):
    """
    Handle OAuth 2.0 callback from Vanta
    """
    try:
        # Verify state parameter
        if state not in oauth_states:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid state parameter"
            )
        
        # Remove used state
        del oauth_states[state]
        
        # Exchange code for token
        token_data = vanta_client.exchange_code_for_token(code)
        
        return {
            "status": "success",
            "message": "Successfully authenticated with Vanta",
            "token_type": token_data.get("token_type"),
            "expires_in": token_data.get("expires_in"),
            "scope": token_data.get("scope")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling Vanta callback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete authorization: {str(e)}"
        )

@router.post("/auth/token")
async def set_vanta_token(
    access_token: str,
    token_type: str = "Bearer"
):
    """
    Manually set Vanta access token (for testing or if you have a token)
    """
    try:
        vanta_client.set_access_token(access_token, token_type)
        
        return {
            "status": "success",
            "message": "Vanta access token set successfully"
        }
        
    except Exception as e:
        logger.error(f"Error setting Vanta token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set token: {str(e)}"
        )

@router.get("/controls")
async def get_compliance_controls():
    """
    Get compliance controls from Vanta
    """
    try:
        logger.info("Fetching compliance controls from Vanta")
        
        controls = await vanta_client.get_controls()
        
        logger.info("Successfully retrieved compliance controls")
        return {
            "status": "success",
            "data": controls,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching compliance controls: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch compliance controls: {str(e)}"
        )

@router.get("/risks")
async def get_risk_findings():
    """
    Get risk findings from Vanta
    """
    try:
        logger.info("Fetching risk findings from Vanta")
        
        risk_findings = await vanta_client.get_risk_findings()
        
        logger.info("Successfully retrieved risk findings")
        return {
            "status": "success",
            "data": risk_findings,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching risk findings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch risk findings: {str(e)}"
        )

@router.get("/evidence/{control_id}")
async def get_control_evidence(control_id: str):
    """
    Get evidence for a specific control
    """
    try:
        logger.info(f"Fetching evidence for control: {control_id}")
        
        evidence = await vanta_client.get_evidence(control_id)
        
        logger.info(f"Successfully retrieved evidence for control: {control_id}")
        return {
            "status": "success",
            "control_id": control_id,
            "data": evidence,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching evidence for control {control_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch evidence: {str(e)}"
        )

@router.get("/organization/status")
async def get_organization_status():
    """
    Get overall organization compliance status
    """
    try:
        logger.info("Fetching organization compliance status from Vanta")
        
        org_status = await vanta_client.get_organization_status()
        
        logger.info("Successfully retrieved organization status")
        return {
            "status": "success",
            "data": org_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching organization status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch organization status: {str(e)}"
        )

@router.get("/compliance-posture")
async def check_compliance_posture():
    """
    Check overall compliance posture for FinTrust AI analysis
    """
    try:
        logger.info("Checking compliance posture for analysis")
        
        compliance_posture = await vanta_client.check_compliance_posture()
        
        logger.info("Successfully checked compliance posture")
        return {
            "status": "success",
            "data": compliance_posture,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error checking compliance posture: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check compliance posture: {str(e)}"
        )

@router.get("/health")
async def vanta_health_check():
    """
    Health check for Vanta API integration
    """
    try:
        # Test basic connectivity
        controls = await vanta_client.get_controls()
        
        return {
            "service": "Vanta API",
            "status": "healthy",
            "connectivity": "successful",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Vanta health check failed: {e}")
        return {
            "service": "Vanta API",
            "status": "unhealthy",
            "connectivity": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/summary")
async def get_compliance_summary():
    """
    Get a comprehensive compliance summary
    """
    try:
        logger.info("Generating compliance summary")
        
        # Get all compliance data
        controls = await vanta_client.get_controls()
        risk_findings = await vanta_client.get_risk_findings()
        org_status = await vanta_client.get_organization_status()
        compliance_posture = await vanta_client.check_compliance_posture()
        
        # Create summary
        summary = {
            "compliance_score": compliance_posture.get("compliance_score", 0),
            "status": compliance_posture.get("status", "unknown"),
            "total_controls": len(controls.get("data", [])),
            "passed_controls": sum(1 for control in controls.get("data", []) 
                                 if control.get("status") == "passed"),
            "risk_findings_count": len(risk_findings.get("data", [])),
            "organization_status": org_status,
            "last_updated": datetime.now().isoformat()
        }
        
        logger.info("Successfully generated compliance summary")
        return {
            "status": "success",
            "data": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating compliance summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate compliance summary: {str(e)}"
        )
