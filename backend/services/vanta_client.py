"""
Vanta API client for compliance verification with OAuth 2.0
"""

import requests
import logging
import base64
from typing import Dict, List, Optional, Any
from core.config import settings

logger = logging.getLogger(__name__)

class VantaClient:
    """Client for interacting with Vanta API using OAuth 2.0"""
    
    def __init__(self):
        self.client_id = settings.VANTA_CLIENT_ID
        self.client_secret = settings.VANTA_CLIENT_SECRET
        self.base_url = settings.VANTA_API_BASE_URL
        self.redirect_uri = settings.VANTA_REDIRECT_URI
        self.access_token = None
        self.token_type = "Bearer"
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers for API requests"""
        if not self.access_token:
            raise ValueError("No access token available. Please authenticate first.")
        
        return {
            "Authorization": f"{self.token_type} {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_authorization_url(self, state: str = None) -> str:
        """Generate OAuth 2.0 authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "read:controls read:risks read:evidence read:organization"
        }
        
        if state:
            params["state"] = state
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://app.vanta.com/oauth/authorize?{query_string}"
    
    def exchange_code_for_token(self, authorization_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        try:
            # Prepare credentials for basic auth
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": self.redirect_uri
            }
            
            response = requests.post(
                "https://app.vanta.com/oauth/token",
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.token_type = token_data.get("token_type", "Bearer")
            
            logger.info("Successfully obtained Vanta access token")
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error exchanging code for token: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to obtain access token: {str(e)}"
            )
    
    def set_access_token(self, access_token: str, token_type: str = "Bearer"):
        """Set access token manually (for testing or if you have a token)"""
        self.access_token = access_token
        self.token_type = token_type
    
    async def get_controls(self) -> Dict[str, Any]:
        """Get compliance controls from Vanta"""
        try:
            response = requests.get(
                f"{self.base_url}/controls",
                headers=self._get_auth_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            logger.info("Successfully retrieved Vanta controls")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Vanta controls: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch compliance controls: {str(e)}"
            )
    
    async def get_risk_findings(self) -> Dict[str, Any]:
        """Get risk findings from Vanta"""
        try:
            response = requests.get(
                f"{self.base_url}/risk-findings",
                headers=self._get_auth_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            logger.info("Successfully retrieved Vanta risk findings")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Vanta risk findings: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch risk findings: {str(e)}"
            )
    
    async def get_evidence(self, control_id: str) -> Dict[str, Any]:
        """Get evidence for a specific control"""
        try:
            response = requests.get(
                f"{self.base_url}/controls/{control_id}/evidence",
                headers=self._get_auth_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"Successfully retrieved evidence for control {control_id}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching evidence for control {control_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch evidence: {str(e)}"
            )
    
    async def get_organization_status(self) -> Dict[str, Any]:
        """Get overall organization compliance status"""
        try:
            response = requests.get(
                f"{self.base_url}/organization/status",
                headers=self._get_auth_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            logger.info("Successfully retrieved organization status")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching organization status: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch organization status: {str(e)}"
            )
    
    async def check_compliance_posture(self) -> Dict[str, Any]:
        """Check overall compliance posture for FinTrust AI analysis"""
        try:
            # Get multiple compliance indicators
            controls = await self.get_controls()
            risk_findings = await self.get_risk_findings()
            org_status = await self.get_organization_status()
            
            # Analyze compliance posture
            compliance_score = self._calculate_compliance_score(controls, risk_findings)
            
            return {
                "compliance_score": compliance_score,
                "controls": controls,
                "risk_findings": risk_findings,
                "organization_status": org_status,
                "timestamp": "2024-01-01T00:00:00Z",
                "status": "compliant" if compliance_score >= 80 else "needs_attention"
            }
            
        except Exception as e:
            logger.error(f"Error checking compliance posture: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to check compliance posture: {str(e)}"
            )
    
    def _calculate_compliance_score(self, controls: Dict, risk_findings: Dict) -> int:
        """Calculate overall compliance score based on controls and risk findings"""
        try:
            # Simple scoring logic - in production, this would be more sophisticated
            total_controls = len(controls.get('data', []))
            passed_controls = sum(1 for control in controls.get('data', []) 
                                if control.get('status') == 'passed')
            
            if total_controls == 0:
                return 0
            
            base_score = (passed_controls / total_controls) * 100
            
            # Adjust for risk findings
            risk_count = len(risk_findings.get('data', []))
            risk_penalty = min(risk_count * 5, 20)  # Max 20 point penalty
            
            final_score = max(base_score - risk_penalty, 0)
            return int(final_score)
            
        except Exception as e:
            logger.error(f"Error calculating compliance score: {e}")
            return 0

# Global Vanta client instance
vanta_client = VantaClient()
