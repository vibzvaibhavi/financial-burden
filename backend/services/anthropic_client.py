"""
Alternative: Direct Anthropic API client (uses API key)
"""

import requests
import logging
from typing import Dict, Any
from core.config import settings

logger = logging.getLogger(__name__)

class AnthropicClient:
    """Client for Anthropic API using API key authentication"""
    
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY  # You'd add this to config
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    async def analyze_kyc_profile(self, kyc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze KYC profile using Anthropic API"""
        
        prompt = self._build_kyc_analysis_prompt(kyc_data)
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json={
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_analysis_response(result['content'][0]['text'])
            
        except Exception as e:
            logger.error(f"Error analyzing KYC profile: {e}")
            raise
    
    def _build_kyc_analysis_prompt(self, kyc_data: Dict[str, Any]) -> str:
        """Build prompt for KYC analysis"""
        return f"""
You are a financial compliance expert analyzing a KYC profile for risk assessment.

Customer Data:
- Customer ID: {kyc_data.get('customer_id', 'N/A')}
- Name: {kyc_data.get('name', 'N/A')}
- Date of Birth: {kyc_data.get('date_of_birth', 'N/A')}
- Address: {kyc_data.get('address', 'N/A')}
- Occupation: {kyc_data.get('occupation', 'N/A')}
- Annual Income: {kyc_data.get('annual_income', 'N/A')}
- Source of Funds: {kyc_data.get('source_of_funds', 'N/A')}
- PEP Status: {kyc_data.get('pep_status', 'N/A')}
- Sanctions Check: {kyc_data.get('sanctions_check', 'N/A')}

Please analyze this KYC profile and provide:
1. Risk Level: LOW, MEDIUM, or HIGH
2. Risk Factors: List specific factors contributing to the risk assessment
3. Recommendations: Specific actions to mitigate identified risks
4. Compliance Notes: Any regulatory considerations

Format your response as JSON with the following structure:
{{
    "risk_level": "LOW|MEDIUM|HIGH",
    "risk_score": 0-100,
    "risk_factors": ["factor1", "factor2", ...],
    "recommendations": ["recommendation1", "recommendation2", ...],
    "compliance_notes": "Additional compliance considerations",
    "analysis_summary": "Brief summary of the analysis"
}}
"""
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse model response for analysis"""
        try:
            import json
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error parsing analysis response: {e}")
            return {
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_factors": ["Unable to parse analysis"],
                "recommendations": ["Manual review required"],
                "compliance_notes": "Analysis parsing failed",
                "analysis_summary": "Error in analysis processing"
            }
