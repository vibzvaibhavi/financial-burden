"""
AWS Bedrock client for Claude 3 Sonnet 4 integration
"""

import json
import logging
import boto3
import os
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional
from core.config import settings

logger = logging.getLogger(__name__)

class BedrockClient:
    """Client for AWS Bedrock Claude 3 Sonnet 4"""
    
    def __init__(self):
        self.region = settings.AWS_REGION
        self.model_id = settings.BEDROCK_MODEL_ID
        self.max_tokens = settings.BEDROCK_MAX_TOKENS
        self.temperature = settings.BEDROCK_TEMPERATURE
        
        # Initialize Bedrock client with API key
        try:
            if settings.AWS_BEARER_TOKEN_BEDROCK:
                # Use Bedrock API key (Bearer Token)
                os.environ["AWS_BEARER_TOKEN_BEDROCK"] = settings.AWS_BEARER_TOKEN_BEDROCK
                self.bedrock = boto3.client(
                    'bedrock-runtime',
                    region_name=self.region
                )
                logger.info("Bedrock client initialized with API key")
            elif settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                # Use traditional AWS credentials
                self.bedrock = boto3.client(
                    'bedrock-runtime',
                    region_name=self.region,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                logger.info("Bedrock client initialized with AWS credentials")
            else:
                raise ValueError("Either AWS_BEARER_TOKEN_BEDROCK or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY must be provided")
                
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
    
    async def analyze_kyc_profile(self, kyc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze KYC profile for risk assessment"""
        
        prompt = self._build_kyc_analysis_prompt(kyc_data)
        
        try:
            response = await self._invoke_model(prompt)
            
            # Parse the response
            analysis = self._parse_analysis_response(response)
            
            logger.info(f"KYC analysis completed for customer: {kyc_data.get('customer_id', 'unknown')}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing KYC profile: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze KYC profile: {str(e)}"
            )
    
    async def analyze_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze transaction for suspicious activity"""
        
        prompt = self._build_transaction_analysis_prompt(transaction_data)
        
        try:
            response = await self._invoke_model(prompt)
            
            # Parse the response
            analysis = self._parse_analysis_response(response)
            
            logger.info(f"Transaction analysis completed for transaction: {transaction_data.get('transaction_id', 'unknown')}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing transaction: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze transaction: {str(e)}"
            )
    
    async def generate_sar(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Suspicious Activity Report"""
        
        prompt = self._build_sar_generation_prompt(analysis_data)
        
        try:
            response = await self._invoke_model(prompt)
            
            # Parse the response
            sar = self._parse_sar_response(response)
            
            logger.info("SAR generated successfully")
            return sar
            
        except Exception as e:
            logger.error(f"Error generating SAR: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate SAR: {str(e)}"
            )
    
    async def _invoke_model(self, prompt: str) -> str:
        """Invoke Claude 3 Sonnet 4 model"""
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except ClientError as e:
            logger.error(f"Bedrock invocation failed: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Model invocation failed: {str(e)}"
            )
    
    def _build_kyc_analysis_prompt(self, kyc_data: Dict[str, Any]) -> str:
        """Build prompt for KYC analysis"""
        
        return f"""
You are a financial compliance expert analyzing a KYC (Know Your Customer) profile for risk assessment.

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
    
    def _build_transaction_analysis_prompt(self, transaction_data: Dict[str, Any]) -> str:
        """Build prompt for transaction analysis"""
        
        return f"""
You are a financial compliance expert analyzing a transaction for suspicious activity.

Transaction Data:
- Transaction ID: {transaction_data.get('transaction_id', 'N/A')}
- Amount: {transaction_data.get('amount', 'N/A')}
- Currency: {transaction_data.get('currency', 'N/A')}
- Transaction Type: {transaction_data.get('transaction_type', 'N/A')}
- Date: {transaction_data.get('date', 'N/A')}
- Origin: {transaction_data.get('origin', 'N/A')}
- Destination: {transaction_data.get('destination', 'N/A')}
- Customer ID: {transaction_data.get('customer_id', 'N/A')}
- Purpose: {transaction_data.get('purpose', 'N/A')}

Please analyze this transaction and provide:
1. Suspicion Level: LOW, MEDIUM, or HIGH
2. Red Flags: List specific indicators of suspicious activity
3. AML Concerns: Anti-Money Laundering considerations
4. Recommendations: Next steps for investigation

Format your response as JSON with the following structure:
{{
    "suspicion_level": "LOW|MEDIUM|HIGH",
    "suspicion_score": 0-100,
    "red_flags": ["flag1", "flag2", ...],
    "aml_concerns": ["concern1", "concern2", ...],
    "recommendations": ["recommendation1", "recommendation2", ...],
    "analysis_summary": "Brief summary of the analysis"
}}
"""
    
    def _build_sar_generation_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Build prompt for SAR generation"""
        
        return f"""
You are a financial compliance expert generating a Suspicious Activity Report (SAR).

Analysis Data:
{json.dumps(analysis_data, indent=2)}

Please generate a comprehensive SAR that includes:
1. Executive Summary
2. Subject Information
3. Suspicious Activity Description
4. Supporting Evidence
5. Risk Assessment
6. Recommendations

Format your response as JSON with the following structure:
{{
    "sar_id": "SAR-YYYY-MM-DD-XXXX",
    "executive_summary": "Brief summary of the suspicious activity",
    "subject_information": {{
        "customer_id": "customer_id",
        "name": "customer_name",
        "other_details": "..."
    }},
    "suspicious_activity": {{
        "description": "Detailed description of suspicious activity",
        "timeframe": "When the activity occurred",
        "amount": "Total amount involved"
    }},
    "supporting_evidence": ["evidence1", "evidence2", ...],
    "risk_assessment": "Overall risk assessment",
    "recommendations": ["recommendation1", "recommendation2", ...],
    "filing_instructions": "Instructions for filing with FinCEN"
}}
"""
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse model response for analysis"""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error parsing analysis response: {e}")
            # Return fallback response
            return {
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_factors": ["Unable to parse analysis"],
                "recommendations": ["Manual review required"],
                "compliance_notes": "Analysis parsing failed",
                "analysis_summary": "Error in analysis processing"
            }
    
    def _parse_sar_response(self, response: str) -> Dict[str, Any]:
        """Parse model response for SAR"""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error parsing SAR response: {e}")
            # Return fallback SAR
            return {
                "sar_id": "SAR-ERROR-001",
                "executive_summary": "Error generating SAR",
                "subject_information": {},
                "suspicious_activity": {},
                "supporting_evidence": [],
                "risk_assessment": "Unable to assess",
                "recommendations": ["Manual review required"],
                "filing_instructions": "Contact compliance team"
            }

# Global Bedrock client instance
bedrock_client = BedrockClient()
