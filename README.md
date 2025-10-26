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

## 🛡️ Security Features and Architecture
| Security Feature           | Description                                                                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **IAM Role-Based Access**  | No static API keys — all AWS service calls use IAM roles with least-privilege permissions.                                             |
| **End-to-End Encryption**  | All data encrypted at rest and in transit via **AWS KMS** and **TLS 1.2+**.                                                            |
| **Full Audit Trail**       | All actions logged through **AWS CloudTrail** for traceability and compliance evidence.                                                |
| **Compliance Cross-Check** | **Vanta API** integration ensures real-time adherence to SOC 2, ISO 27001, and other frameworks.                                       |
| **AWS Data Boundary**      | All computation and storage occur within the **AWS regional compliance boundary**, ensuring data sovereignty and regulatory alignment. |

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
# AWS Bedrock Credentials
AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_KEY"
AWS_REGION_NAME="us-east-1"

# Vanta Compliance API
VANTA_API_KEY="YOUR_VANTA_API_KEY"

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
