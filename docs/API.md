# FinTrust AI API Documentation

This document describes the REST API endpoints for FinTrust AI - Secure FinTech Compliance Copilot.

## Base URL
- Local Development: `http://localhost:8000`
- Production: `https://api.fintrust-ai.com`

## Authentication

All API endpoints (except `/auth/login`) require authentication using JWT tokens.

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Using the Token
Include the token in the Authorization header:
```http
Authorization: Bearer <your-token>
```

## Risk Analysis Endpoints

### KYC Analysis
Analyze customer profiles for risk assessment.

```http
POST /analyze/kyc
Authorization: Bearer <token>
Content-Type: application/json

{
  "customer_id": "CUST001",
  "name": "John Doe",
  "date_of_birth": "1985-06-15",
  "address": "123 Main St, New York, NY 10001",
  "occupation": "Software Engineer",
  "annual_income": 75000,
  "source_of_funds": "Employment",
  "pep_status": "No",
  "sanctions_check": "Clear"
}
```

**Response:**
```json
{
  "analysis_id": "KYC-20240101-CUST001",
  "risk_level": "LOW",
  "risk_score": 25,
  "risk_factors": [
    "Low income relative to transaction patterns"
  ],
  "recommendations": [
    "Monitor for unusual transaction patterns",
    "Verify employment status"
  ],
  "compliance_notes": "Customer appears to be low risk based on provided information",
  "analysis_summary": "Standard KYC analysis completed with low risk assessment",
  "timestamp": "2024-01-01T12:00:00Z",
  "compliance_status": "compliant"
}
```

### Transaction Analysis
Analyze transactions for suspicious activity.

```http
POST /analyze/transaction
Authorization: Bearer <token>
Content-Type: application/json

{
  "transaction_id": "TXN001",
  "amount": 50000,
  "currency": "USD",
  "transaction_type": "Wire Transfer",
  "date": "2024-01-01T10:30:00Z",
  "origin": "Bank of America",
  "destination": "Wells Fargo",
  "customer_id": "CUST001",
  "purpose": "Business payment"
}
```

**Response:**
```json
{
  "analysis_id": "TXN-20240101-TXN001",
  "risk_level": "MEDIUM",
  "risk_score": 65,
  "risk_factors": [
    "Large transaction amount",
    "Cross-bank transfer"
  ],
  "recommendations": [
    "Verify business relationship",
    "Request additional documentation"
  ],
  "compliance_notes": [
    "Monitor for pattern of similar transactions",
    "Consider enhanced due diligence"
  ],
  "analysis_summary": "Transaction flagged for additional review due to amount and type",
  "timestamp": "2024-01-01T12:00:00Z",
  "compliance_status": "compliant"
}
```

### Comprehensive Analysis
Perform combined KYC and transaction analysis.

```http
POST /analyze/comprehensive
Authorization: Bearer <token>
Content-Type: application/json

{
  "kyc_request": {
    "customer_id": "CUST001",
    "name": "John Doe",
    "date_of_birth": "1985-06-15",
    "address": "123 Main St, New York, NY 10001",
    "occupation": "Software Engineer",
    "annual_income": 75000,
    "source_of_funds": "Employment",
    "pep_status": "No",
    "sanctions_check": "Clear"
  },
  "transaction_requests": [
    {
      "transaction_id": "TXN001",
      "amount": 50000,
      "currency": "USD",
      "transaction_type": "Wire Transfer",
      "date": "2024-01-01T10:30:00Z",
      "origin": "Bank of America",
      "destination": "Wells Fargo",
      "customer_id": "CUST001",
      "purpose": "Business payment"
    }
  ]
}
```

**Response:**
```json
{
  "analysis_id": "COMP-20240101-CUST001",
  "customer_id": "CUST001",
  "kyc_analysis": { ... },
  "transaction_analyses": [ ... ],
  "sar_generated": true,
  "sar_data": {
    "sar_id": "SAR-20240101-ABC12345",
    "executive_summary": "Suspicious activity detected...",
    "subject_information": { ... },
    "suspicious_activity": { ... },
    "supporting_evidence": [ ... ],
    "risk_assessment": "High risk of money laundering",
    "recommendations": [ ... ],
    "filing_instructions": "File with FinCEN within 15 days"
  },
  "compliance_status": { ... },
  "timestamp": "2024-01-01T12:00:00Z",
  "overall_risk_level": "HIGH"
}
```

## Compliance Endpoints

### Get Compliance Controls
Retrieve compliance controls from Vanta.

```http
GET /vanta/controls
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "data": [
      {
        "id": "control-001",
        "name": "Access Control",
        "description": "User access management controls",
        "status": "passed",
        "category": "Security"
      }
    ]
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Get Risk Findings
Retrieve risk findings from Vanta.

```http
GET /vanta/risks
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "data": [
      {
        "id": "risk-001",
        "title": "Unpatched System",
        "description": "Critical security patch missing",
        "severity": "High",
        "status": "Open"
      }
    ]
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Get Compliance Posture
Check overall compliance posture.

```http
GET /vanta/compliance-posture
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "compliance_score": 85,
    "status": "compliant",
    "controls": { ... },
    "risk_findings": { ... },
    "organization_status": { ... },
    "timestamp": "2024-01-01T12:00:00Z"
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Audit Endpoints

### List SARs
List all Suspicious Activity Reports.

```http
GET /audit/sars?customer_id=CUST001
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "sars": [
      {
        "sar_id": "SAR-20240101-ABC12345",
        "file_path": "sars/CUST001/SAR-20240101-ABC12345.json",
        "size": 2048,
        "last_modified": "2024-01-01T12:00:00Z",
        "customer_id": "CUST001"
      }
    ],
    "count": 1,
    "customer_id": "CUST001"
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Get SAR
Retrieve a specific SAR document.

```http
GET /audit/sars/SAR-20240101-ABC12345?customer_id=CUST001
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "sar_id": "SAR-20240101-ABC12345",
    "executive_summary": "Suspicious activity detected...",
    "subject_information": {
      "customer_id": "CUST001",
      "name": "John Doe"
    },
    "suspicious_activity": {
      "description": "Multiple large transactions...",
      "timeframe": "2024-01-01 to 2024-01-15",
      "amount": "$150,000"
    },
    "supporting_evidence": [
      "Transaction records",
      "Customer communications"
    ],
    "risk_assessment": "High risk of money laundering",
    "recommendations": [
      "File SAR with FinCEN",
      "Enhanced monitoring"
    ],
    "filing_instructions": "File with FinCEN within 15 days"
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Get Audit Dashboard
Retrieve audit dashboard data.

```http
GET /audit/dashboard
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "sars": {
      "total": 15,
      "recent": 3
    },
    "compliance": {
      "status": "compliant",
      "last_check": "2024-01-01T12:00:00Z"
    },
    "analyses": {
      "total_today": 25,
      "high_risk": 2,
      "medium_risk": 8,
      "low_risk": 15
    },
    "system": {
      "status": "operational",
      "last_backup": "2024-01-01T12:00:00Z",
      "encryption": "enabled"
    }
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Export Audit Data
Export audit data for compliance reporting.

```http
GET /audit/export?start_date=2024-01-01&end_date=2024-01-31&format=json
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "export_id": "EXPORT-20240101-120000",
    "format": "json",
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-01-31"
    },
    "records": 150,
    "status": "generated",
    "download_url": null
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Health Check Endpoints

### API Health
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "services": {
    "api": "operational",
    "bedrock": "operational",
    "vanta": "operational",
    "s3": "operational"
  }
}
```

### Service Health Checks
```http
GET /analyze/status
GET /vanta/health
GET /audit/health
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message describing what went wrong",
  "status_code": 400,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Common HTTP Status Codes
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

API endpoints are rate limited:
- General API: 10 requests per second
- Login endpoint: 5 requests per minute
- Analysis endpoints: 5 requests per minute

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1640995200
```

## Webhooks (Future)

Webhook endpoints for real-time notifications:
- `/webhooks/analysis-complete`
- `/webhooks/sar-generated`
- `/webhooks/compliance-alert`

## SDK Examples

### Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/auth/login', json={
    'username': 'admin',
    'password': 'admin123'
})
token = response.json()['access_token']

# Analyze KYC
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/analyze/kyc', 
                        json=kyc_data, headers=headers)
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { access_token } = await loginResponse.json();

// Analyze KYC
const analysisResponse = await fetch('http://localhost:8000/analyze/kyc', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify(kycData)
});
```

## Testing

Use the interactive API documentation at `/docs` for testing endpoints directly in the browser.
