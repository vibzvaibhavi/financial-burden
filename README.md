# FinTrust AI - Secure FinTech Compliance Copilot

**Built for the 7-Hour AWS Loft FinTech Hackathon**

---

## The Problem

Financial institutions face a relentless barrage of complex regulations and sophisticated threats like money laundering and fraud. Manually reviewing every transaction is impossible, and legacy rule-based systems generate floods of false positives, wasting valuable time for compliance officers.

## Our Solution: FinTrust AI

**FinTrust AI** is a next-generation compliance copilot that leverages the power of Generative AI to automate and enhance the risk analysis process. In just 7 hours, we built a functional prototype that can:

1.  **Analyze Financial Transactions with AI:** Instead of rigid rules, we use AWS Bedrock (Claude 3 Sonnet) to analyze the *narrative* and *context* of financial transactions, detecting nuanced signs of illicit activity that traditional systems miss.
2.  **Generate Suspicious Activity Reports (SARs):** When a high-risk transaction is identified, the AI automatically generates a detailed, human-readable SAR, complete with a risk score and a justification for its findings.
3.  **Verify Compliance Status:** Integrates with the Vanta API to provide a real-time dashboard of the organization's compliance posture, ensuring that security controls are being met.

This is not just an alerting system; it's a co-pilot that empowers compliance teams to focus on genuine threats, not noise.

---

## How It Works: The AI-Powered Analysis Flow

1.  **Transaction Ingestion:** The backend receives a transaction for analysis (e.g., a large international wire transfer).
2.  **AI Risk Assessment:** The transaction data is sent to a secure prompt on **AWS Bedrock**. Claude 3 Sonnet evaluates the transaction against a sophisticated set of learned patterns and contextual red flags for financial crime.
3.  **Intelligent Response:** The model returns a structured JSON object containing:
    *   A boolean `is_suspicious` flag.
    *   A risk score from 1 to 100.
    *   A detailed `summary` explaining *why* the transaction is or isn't suspicious.
4.  **Automated SAR Generation:** If the risk score exceeds a defined threshold, the AI-generated summary is used to automatically populate a Suspicious Activity Report, which is then stored securely.

---
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
