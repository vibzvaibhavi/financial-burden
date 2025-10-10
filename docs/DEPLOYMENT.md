# FinTrust AI Deployment Guide

This guide covers deploying FinTrust AI - Secure FinTech Compliance Copilot using AWS infrastructure.

## Prerequisites

### Required Tools
- AWS CLI v2
- Docker and Docker Compose
- Python 3.9+
- Node.js 18+
- Git

### AWS Requirements
- AWS Account with appropriate permissions
- Bedrock access enabled in your region
- Vanta API key

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd fintrust-ai
```

### 2. Environment Configuration
```bash
# Copy environment template
cp backend/env.example backend/.env

# Edit the .env file with your configuration
nano backend/.env
```

### 3. Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## AWS Deployment

### 1. Infrastructure Setup
```bash
cd infrastructure

# Set your Vanta API key
export VANTA_API_KEY="your-vanta-api-key"

# Deploy infrastructure
./deploy.sh --environment dev --region us-east-1
```

### 2. Verify Deployment
```bash
# Check CloudFormation stack
aws cloudformation describe-stacks --stack-name fintrust-ai-dev

# Test S3 bucket
aws s3 ls s3://fintrust-ai-reports-dev-<account-id>

# Test Lambda function
aws lambda invoke --function-name fintrust-ai-dev /tmp/response.json
```

## Docker Deployment

### 1. Build and Run
```bash
cd infrastructure
docker-compose up -d
```

### 2. Access Services
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Security Configuration

### 1. IAM Roles
The deployment creates the following IAM roles:
- `FinTrustLambdaRole`: For Lambda function execution
- `FinTrustBackendRole`: For backend service access

### 2. KMS Encryption
- All S3 objects are encrypted with KMS
- KMS key alias: `alias/fintrust-ai-key-<environment>`

### 3. CloudTrail Logging
- All API calls are logged to CloudTrail
- Logs stored in S3 with encryption

## Environment Variables

### Backend (.env)
```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Vanta API
VANTA_API_KEY=your-vanta-api-key
VANTA_API_BASE_URL=https://api.vanta.com/v1

# Application
APP_NAME=FinTrust AI
DEBUG=True
SECRET_KEY=your-secret-key

# S3 Configuration
S3_BUCKET_NAME=fintrust-ai-reports-dev-<account-id>
KMS_KEY_ID=alias/fintrust-ai-key-dev
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
```

## Monitoring and Logging

### 1. CloudWatch Logs
- Log Group: `/aws/lambda/fintrust-ai-<environment>`
- Retention: 30 days

### 2. CloudTrail
- Trail Name: `fintrust-ai-trail-<environment>`
- Multi-region: Yes
- S3 bucket: `fintrust-ai-reports-<environment>-<account-id>`

### 3. S3 Access Logs
- All S3 access is logged
- Logs stored in the same bucket under `access-logs/`

## Troubleshooting

### Common Issues

#### 1. Bedrock Access Denied
```bash
# Check if Bedrock is enabled in your region
aws bedrock list-foundation-models --region us-east-1

# Request access if needed
aws bedrock request-model-access --model-id anthropic.claude-3-sonnet-20240229-v1:0
```

#### 2. Vanta API Connection Issues
```bash
# Test Vanta API connectivity
curl -H "Authorization: Bearer $VANTA_API_KEY" \
     https://api.vanta.com/v1/controls
```

#### 3. S3 Permission Issues
```bash
# Check S3 bucket permissions
aws s3api get-bucket-policy --bucket fintrust-ai-reports-dev-<account-id>
```

### Logs and Debugging

#### Backend Logs
```bash
# Local development
tail -f backend/logs/app.log

# AWS Lambda
aws logs tail /aws/lambda/fintrust-ai-dev --follow
```

#### Frontend Logs
```bash
# Browser console
# Check Network tab for API calls
```

## Production Deployment

### 1. Environment Setup
```bash
# Use production environment
./deploy.sh --environment prod --region us-east-1
```

### 2. Security Hardening
- Enable AWS WAF
- Configure VPC endpoints
- Set up monitoring alerts
- Enable AWS Config

### 3. Backup Strategy
- S3 versioning enabled
- Cross-region replication
- Regular backup testing

## Scaling

### Horizontal Scaling
- Lambda concurrency limits
- S3 request rate limits
- API Gateway throttling

### Vertical Scaling
- Lambda memory allocation
- S3 storage classes
- CloudWatch log retention

## Cost Optimization

### 1. S3 Storage
- Lifecycle policies for old versions
- Intelligent tiering for infrequent access

### 2. Lambda
- Right-size memory allocation
- Use provisioned concurrency for consistent performance

### 3. CloudWatch
- Set appropriate log retention periods
- Use log filters to reduce costs

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review AWS CloudWatch logs
3. Check CloudFormation stack events
4. Contact the development team

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use IAM roles** instead of access keys when possible
3. **Enable MFA** for all AWS accounts
4. **Regular security audits** using AWS Config
5. **Monitor access patterns** with CloudTrail
6. **Encrypt all data** at rest and in transit
7. **Use least privilege** access principles
8. **Regular backup testing** and disaster recovery drills
