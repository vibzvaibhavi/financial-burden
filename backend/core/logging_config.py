"""
Logging configuration for FinTrust AI
"""

import logging
import sys
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from core.config import settings

def setup_logging():
    """Setup application logging with CloudWatch integration"""
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add console handler
    logger.addHandler(console_handler)
    
    # CloudWatch handler (if AWS credentials are available)
    try:
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            cloudwatch_handler = CloudWatchHandler()
            cloudwatch_handler.setLevel(logging.INFO)
            cloudwatch_handler.setFormatter(formatter)
            logger.addHandler(cloudwatch_handler)
            logger.info("CloudWatch logging enabled")
    except Exception as e:
        logger.warning(f"CloudWatch logging not available: {e}")

class CloudWatchHandler(logging.Handler):
    """Custom CloudWatch logging handler"""
    
    def __init__(self):
        super().__init__()
        self.cloudwatch_logs = boto3.client(
            'logs',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.log_group = settings.CLOUDWATCH_LOG_GROUP
        self.log_stream = f"fintrust-ai-{datetime.now().strftime('%Y-%m-%d')}"
        
        # Ensure log group exists
        self._ensure_log_group()
        self._ensure_log_stream()
    
    def _ensure_log_group(self):
        """Ensure CloudWatch log group exists"""
        try:
            self.cloudwatch_logs.describe_log_groups(
                logGroupNamePrefix=self.log_group
            )
        except ClientError:
            try:
                self.cloudwatch_logs.create_log_group(
                    logGroupName=self.log_group
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    raise
    
    def _ensure_log_stream(self):
        """Ensure CloudWatch log stream exists"""
        try:
            self.cloudwatch_logs.describe_log_streams(
                logGroupName=self.log_group,
                logStreamNamePrefix=self.log_stream
            )
        except ClientError:
            try:
                self.cloudwatch_logs.create_log_stream(
                    logGroupName=self.log_group,
                    logStreamName=self.log_stream
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    raise
    
    def emit(self, record):
        """Emit log record to CloudWatch"""
        try:
            log_entry = self.format(record)
            timestamp = int(record.created * 1000)  # CloudWatch expects milliseconds
            
            self.cloudwatch_logs.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=[
                    {
                        'timestamp': timestamp,
                        'message': log_entry
                    }
                ]
            )
        except Exception:
            # Don't let logging errors break the application
            pass
