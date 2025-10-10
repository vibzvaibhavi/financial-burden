"""
S3 client for secure document storage with KMS encryption
"""

import json
import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from core.config import settings

logger = logging.getLogger(__name__)

class S3Client:
    """Client for S3 operations with KMS encryption"""
    
    def __init__(self):
        self.bucket_name = settings.S3_BUCKET_NAME
        self.kms_key_id = settings.KMS_KEY_ID
        self.region = settings.AWS_REGION
        
        # Initialize S3 client
        try:
            self.s3 = boto3.client(
                's3',
                region_name=self.region,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            logger.info("S3 client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise
    
    async def store_sar(self, sar_data: Dict[str, Any], customer_id: str) -> Dict[str, Any]:
        """Store SAR document in S3 with encryption"""
        
        try:
            # Generate unique SAR ID
            sar_id = f"SAR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            sar_data['sar_id'] = sar_id
            sar_data['created_at'] = datetime.now().isoformat()
            sar_data['customer_id'] = customer_id
            
            # Create file path
            file_path = f"sars/{customer_id}/{sar_id}.json"
            
            # Prepare upload parameters
            upload_params = {
                'Bucket': self.bucket_name,
                'Key': file_path,
                'Body': json.dumps(sar_data, indent=2),
                'ContentType': 'application/json'
            }
            
            # Add KMS encryption if key is available
            if self.kms_key_id:
                upload_params['ServerSideEncryption'] = 'aws:kms'
                upload_params['SSEKMSKeyId'] = self.kms_key_id
            
            # Upload to S3
            self.s3.put_object(**upload_params)
            
            logger.info(f"SAR stored successfully: {sar_id}")
            
            return {
                "sar_id": sar_id,
                "file_path": file_path,
                "bucket": self.bucket_name,
                "status": "stored",
                "encrypted": bool(self.kms_key_id),
                "created_at": sar_data['created_at']
            }
            
        except ClientError as e:
            logger.error(f"Error storing SAR in S3: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to store SAR: {str(e)}"
            )
    
    async def store_analysis_report(self, analysis_data: Dict[str, Any], report_type: str, customer_id: str) -> Dict[str, Any]:
        """Store analysis report in S3"""
        
        try:
            # Generate unique report ID
            report_id = f"{report_type.upper()}-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            analysis_data['report_id'] = report_id
            analysis_data['created_at'] = datetime.now().isoformat()
            analysis_data['customer_id'] = customer_id
            analysis_data['report_type'] = report_type
            
            # Create file path
            file_path = f"reports/{report_type}/{customer_id}/{report_id}.json"
            
            # Prepare upload parameters
            upload_params = {
                'Bucket': self.bucket_name,
                'Key': file_path,
                'Body': json.dumps(analysis_data, indent=2),
                'ContentType': 'application/json'
            }
            
            # Add KMS encryption if key is available
            if self.kms_key_id:
                upload_params['ServerSideEncryption'] = 'aws:kms'
                upload_params['SSEKMSKeyId'] = self.kms_key_id
            
            # Upload to S3
            self.s3.put_object(**upload_params)
            
            logger.info(f"Analysis report stored successfully: {report_id}")
            
            return {
                "report_id": report_id,
                "file_path": file_path,
                "bucket": self.bucket_name,
                "status": "stored",
                "encrypted": bool(self.kms_key_id),
                "created_at": analysis_data['created_at']
            }
            
        except ClientError as e:
            logger.error(f"Error storing analysis report in S3: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to store analysis report: {str(e)}"
            )
    
    async def retrieve_sar(self, sar_id: str, customer_id: str) -> Dict[str, Any]:
        """Retrieve SAR document from S3"""
        
        try:
            file_path = f"sars/{customer_id}/{sar_id}.json"
            
            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            
            sar_data = json.loads(response['Body'].read().decode('utf-8'))
            
            logger.info(f"SAR retrieved successfully: {sar_id}")
            return sar_data
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise HTTPException(
                    status_code=404,
                    detail=f"SAR not found: {sar_id}"
                )
            else:
                logger.error(f"Error retrieving SAR from S3: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to retrieve SAR: {str(e)}"
                )
    
    async def list_sars(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """List SAR documents in S3"""
        
        try:
            prefix = f"sars/{customer_id}/" if customer_id else "sars/"
            
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            sars = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    sars.append({
                        "sar_id": obj['Key'].split('/')[-1].replace('.json', ''),
                        "file_path": obj['Key'],
                        "size": obj['Size'],
                        "last_modified": obj['LastModified'].isoformat(),
                        "customer_id": obj['Key'].split('/')[1] if len(obj['Key'].split('/')) > 1 else None
                    })
            
            logger.info(f"Listed {len(sars)} SAR documents")
            return {
                "sars": sars,
                "count": len(sars),
                "customer_id": customer_id
            }
            
        except ClientError as e:
            logger.error(f"Error listing SARs from S3: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list SARs: {str(e)}"
            )
    
    async def create_audit_log(self, action: str, details: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Create audit log entry in S3"""
        
        try:
            # Generate unique log ID
            log_id = f"AUDIT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            
            log_entry = {
                "log_id": log_id,
                "action": action,
                "details": details,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "service": "FinTrust AI"
            }
            
            # Create file path
            file_path = f"audit-logs/{datetime.now().strftime('%Y/%m/%d')}/{log_id}.json"
            
            # Prepare upload parameters
            upload_params = {
                'Bucket': self.bucket_name,
                'Key': file_path,
                'Body': json.dumps(log_entry, indent=2),
                'ContentType': 'application/json'
            }
            
            # Add KMS encryption if key is available
            if self.kms_key_id:
                upload_params['ServerSideEncryption'] = 'aws:kms'
                upload_params['SSEKMSKeyId'] = self.kms_key_id
            
            # Upload to S3
            self.s3.put_object(**upload_params)
            
            logger.info(f"Audit log created successfully: {log_id}")
            
            return {
                "log_id": log_id,
                "file_path": file_path,
                "status": "logged",
                "timestamp": log_entry['timestamp']
            }
            
        except ClientError as e:
            logger.error(f"Error creating audit log in S3: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create audit log: {str(e)}"
            )

# Global S3 client instance
s3_client = S3Client()
