# FinTrust AI Setup Guide

## 🔑 **Complete .env Configuration**

Here's exactly what to put in your `backend/.env` file:

```bash
# AWS Configuration (for Bedrock, S3, CloudWatch)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...your_actual_aws_access_key
AWS_SECRET_ACCESS_KEY=your_actual_aws_secret_key

# Vanta API Configuration (OAuth 2.0)
VANTA_CLIENT_ID=your_actual_vanta_client_id
VANTA_CLIENT_SECRET=your_actual_vanta_client_secret
VANTA_API_BASE_URL=https://api.vanta.com/v1
VANTA_REDIRECT_URI=http://localhost:8000/auth/vanta/callback

# Application Configuration
APP_NAME=FinTrust AI
APP_VERSION=1.0.0
DEBUG=True

# Security Configuration (JWT for API authentication)
SECRET_KEY=your_jwt_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# S3 Configuration (for storing reports and SARs)
S3_BUCKET_NAME=fintrust-ai-reports
KMS_KEY_ID=your_kms_key_id

# CloudWatch Configuration (for logging)
CLOUDWATCH_LOG_GROUP=fintrust-ai-logs

# Bedrock Configuration (Claude 3 Sonnet 4)
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_MAX_TOKENS=4000
BEDROCK_TEMPERATURE=0.1
```

## 🧠 **How Bedrock is Used (Already Integrated!)**

**Bedrock IS the core AI engine** - it's used for:

1. **KYC Analysis** (`/analyze/kyc`)
   - Analyzes customer profiles for risk assessment
   - Returns risk level (LOW/MEDIUM/HIGH)
   - Provides risk factors and recommendations

2. **Transaction Analysis** (`/analyze/transaction`)
   - Detects suspicious activity in transactions
   - Identifies red flags and AML concerns
   - Suggests investigation steps

3. **SAR Generation** (`/analyze/comprehensive`)
   - Automatically generates Suspicious Activity Reports
   - Combines KYC and transaction analysis
   - Creates FinCEN-ready reports

## 🔐 **Security Configuration Explained**

### **SECRET_KEY** (Line 18)
- **Purpose**: JWT token signing for API authentication
- **What to put**: A random string (32+ characters)
- **Example**: `SECRET_KEY=my-super-secret-jwt-key-12345-change-in-production`

### **How to generate a secure SECRET_KEY**:
```bash
# Option 1: Use Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 2: Use OpenSSL
openssl rand -hex 32

# Option 3: Use online generator
# Visit: https://generate-secret.vercel.app/32
```

## 🚀 **Step-by-Step Setup**

### **Step 1: Create .env file**
```bash
cd backend
copy env.example .env
```

### **Step 2: Edit .env with your credentials**
Replace these values:

```bash
# AWS Credentials (for Bedrock access)
AWS_ACCESS_KEY_ID=AKIA...your_actual_key
AWS_SECRET_ACCESS_KEY=your_actual_secret

# Vanta Credentials (OAuth)
VANTA_CLIENT_ID=your_actual_client_id
VANTA_CLIENT_SECRET=your_actual_client_secret

# JWT Secret (generate a random string)
SECRET_KEY=your_generated_jwt_secret_here
```

### **Step 3: Test the setup**
```bash
# Start backend
cd backend
uvicorn main:app --reload

# Test Bedrock connection
curl http://localhost:8000/analyze/status

# Test Vanta OAuth
curl http://localhost:8000/vanta/auth/authorize
```

## 🎯 **What Each Service Does**

| Service | Purpose | Credentials Needed |
|---------|---------|-------------------|
| **AWS Bedrock** | AI analysis (KYC, transactions, SARs) | AWS Access Key + Secret |
| **Vanta API** | Compliance monitoring | Client ID + Client Secret |
| **AWS S3** | Store reports and SARs | Same AWS credentials |
| **JWT Auth** | API authentication | SECRET_KEY |

## 🔍 **Testing Your Setup**

### **Test 1: Bedrock Connection**
```bash
curl -X POST http://localhost:8000/analyze/kyc \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "name": "John Doe",
    "date_of_birth": "1985-01-01",
    "address": "123 Main St",
    "occupation": "Engineer",
    "annual_income": 75000,
    "source_of_funds": "Employment",
    "pep_status": "No",
    "sanctions_check": "Clear"
  }'
```

### **Test 2: Vanta OAuth**
```bash
# Get authorization URL
curl http://localhost:8000/vanta/auth/authorize

# Follow the URL in browser to authorize
# Then set the token
curl -X POST http://localhost:8000/vanta/auth/token \
  -H "Content-Type: application/json" \
  -d '{"access_token": "your_vanta_token"}'
```

## ⚠️ **Important Notes**

1. **Bedrock uses AWS credentials** - no separate API key needed
2. **SECRET_KEY is for JWT** - not for external APIs
3. **Vanta uses OAuth 2.0** - requires authorization flow
4. **All data is encrypted** - KMS + TLS
5. **Never commit .env** - it's in .gitignore

## 🆘 **Troubleshooting**

### **Bedrock Access Denied**
- Check if Bedrock is enabled in your AWS region
- Verify IAM permissions include `bedrock:InvokeModel`
- Ensure you're using the correct AWS region

### **Vanta OAuth Issues**
- Verify Client ID and Secret are correct
- Check redirect URI matches exactly
- Ensure Vanta app is configured for OAuth

### **JWT Token Issues**
- Generate a new SECRET_KEY
- Ensure it's at least 32 characters
- Don't use common passwords
