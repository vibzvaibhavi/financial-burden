#!/usr/bin/env python3
"""
FinTrust AI - Vanta OAuth Setup Script

This script helps you set up OAuth 2.0 authentication with Vanta.
"""

import requests
import webbrowser
import time
from urllib.parse import urlparse, parse_qs

def setup_vanta_oauth():
    print("🔐 FinTrust AI - Vanta OAuth Setup")
    print("=" * 50)
    
    # Get credentials from user
    client_id = input("Enter your Vanta Client ID: ").strip()
    client_secret = input("Enter your Vanta Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Error: Both Client ID and Client Secret are required")
        return
    
    print("\n📝 Setting up OAuth flow...")
    
    # Step 1: Generate authorization URL
    auth_url = f"https://app.vanta.com/oauth/authorize?client_id={client_id}&redirect_uri=http://localhost:8000/auth/vanta/callback&response_type=code&scope=read:controls%20read:risks%20read:evidence%20read:organization"
    
    print(f"\n🌐 Authorization URL:")
    print(auth_url)
    
    # Step 2: Open browser
    print("\n🚀 Opening browser for authorization...")
    try:
        webbrowser.open(auth_url)
        print("✅ Browser opened. Please authorize the application.")
    except:
        print("⚠️  Could not open browser automatically. Please copy the URL above and open it manually.")
    
    # Step 3: Get authorization code
    print("\n📋 After authorizing, you'll be redirected to a URL like:")
    print("http://localhost:8000/auth/vanta/callback?code=AUTHORIZATION_CODE&state=STATE")
    print("\nPlease copy the AUTHORIZATION_CODE from the URL and paste it below:")
    
    auth_code = input("\nEnter the authorization code: ").strip()
    
    if not auth_code:
        print("❌ Error: Authorization code is required")
        return
    
    # Step 4: Exchange code for token
    print("\n🔄 Exchanging authorization code for access token...")
    
    try:
        # Prepare credentials for basic auth
        import base64
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": "http://localhost:8000/auth/vanta/callback"
        }
        
        response = requests.post(
            "https://app.vanta.com/oauth/token",
            headers=headers,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            token_type = token_data.get("token_type", "Bearer")
            
            print("✅ Successfully obtained access token!")
            print(f"\n🔑 Access Token: {access_token[:20]}...")
            print(f"📝 Token Type: {token_type}")
            
            # Step 5: Create .env file
            print("\n📄 Creating .env file...")
            
            env_content = f"""# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Vanta API Configuration (OAuth 2.0)
VANTA_CLIENT_ID={client_id}
VANTA_CLIENT_SECRET={client_secret}
VANTA_API_BASE_URL=https://api.vanta.com/v1
VANTA_REDIRECT_URI=http://localhost:8000/auth/vanta/callback

# Application Configuration
APP_NAME=FinTrust AI
APP_VERSION=1.0.0
DEBUG=True

# Security Configuration
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# S3 Configuration
S3_BUCKET_NAME=fintrust-ai-reports
KMS_KEY_ID=your_kms_key_id

# CloudWatch Configuration
CLOUDWATCH_LOG_GROUP=fintrust-ai-logs

# Vanta Access Token (for testing)
VANTA_ACCESS_TOKEN={access_token}
"""
            
            with open("backend/.env", "w") as f:
                f.write(env_content)
            
            print("✅ .env file created successfully!")
            print("\n🎉 Setup complete! You can now:")
            print("1. Update your AWS credentials in backend/.env")
            print("2. Start the backend: cd backend && uvicorn main:app --reload")
            print("3. Start the frontend: cd frontend && npm run dev")
            
        else:
            print(f"❌ Error: Failed to get access token")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_vanta_oauth()
