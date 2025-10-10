# FinTrust AI - Secure FinTech Compliance Copilot

FinTrust AI is a secure compliance copilot that helps financial institutions analyze customer activity, KYC profiles, and AML policies using AWS Bedrock (Claude 3 Sonnet 4) for reasoning and Vanta API for real-time compliance posture verification.

## 🎯 Key Features

- **Secure AI Analysis**: Uses AWS Bedrock Claude 3 Sonnet 4 for risk assessment
- **Real-time Compliance**: Integrates with Vanta API for SOC 2, ISO 27001 verification
- **Audit Trail**: Full CloudTrail logging and encrypted S3 storage
- **Risk Scoring**: Automated Low/Medium/High risk classification
- **SAR Generation**: Automatic Suspicious Activity Report creation

## 🏗️ Architecture

```
Frontend (React) → FastAPI Backend → AWS Bedrock + Vanta API
                                      ↓
                              S3 (Encrypted) + CloudTrail
```

## 🛡️ Security Features

- No static API keys - all calls via IAM roles
- End-to-end encryption (KMS + TLS)
- Full audit trail (CloudTrail)
- Compliance cross-check using Vanta API
- Secure data handling within AWS boundary

## 🚀 Quick Start

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Environment Configuration**:
   - Set up AWS credentials with Bedrock access
   - Configure Vanta API key
   - Set up IAM roles and KMS keys

## 📁 Project Structure

```
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── infrastructure/    # AWS deployment configs
├── docs/             # Documentation
└── README.md
```

## 🔧 Tech Stack

- **LLM**: AWS Bedrock Claude 3 Sonnet 4
- **Backend**: FastAPI + boto3
- **Frontend**: React (Vite)
- **Compliance**: Vanta API
- **Auth**: Amazon Cognito
- **Storage**: S3 + KMS Encryption
- **Logs**: CloudWatch + CloudTrail
