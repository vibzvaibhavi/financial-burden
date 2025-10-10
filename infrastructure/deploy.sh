#!/bin/bash

# FinTrust AI Deployment Script
# This script deploys the FinTrust AI infrastructure using AWS CloudFormation

set -e

# Configuration
STACK_NAME="fintrust-ai"
ENVIRONMENT="dev"
REGION="us-east-1"
VANTA_API_KEY=""
KMS_KEY_ALIAS="fintrust-ai-key"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if AWS CLI is installed and configured
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi

    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS CLI is not configured. Please run 'aws configure' first."
        exit 1
    fi

    print_status "AWS CLI is configured correctly"
}

# Function to check if required parameters are provided
check_parameters() {
    if [ -z "$VANTA_API_KEY" ]; then
        print_error "VANTA_API_KEY is required. Please set it as an environment variable or modify the script."
        exit 1
    fi
}

# Function to create S3 bucket for deployment artifacts
create_deployment_bucket() {
    BUCKET_NAME="fintrust-ai-deployment-${ENVIRONMENT}-$(date +%s)"
    
    print_status "Creating deployment bucket: $BUCKET_NAME"
    
    if aws s3 mb s3://$BUCKET_NAME --region $REGION; then
        print_status "Deployment bucket created successfully"
        echo $BUCKET_NAME
    else
        print_error "Failed to create deployment bucket"
        exit 1
    fi
}

# Function to package and deploy CloudFormation stack
deploy_stack() {
    print_status "Starting CloudFormation deployment..."
    
    # Package the template
    TEMPLATE_FILE="cloudformation-template.yaml"
    PACKAGED_TEMPLATE="packaged-template.yaml"
    
    if [ ! -f "$TEMPLATE_FILE" ]; then
        print_error "CloudFormation template not found: $TEMPLATE_FILE"
        exit 1
    fi
    
    print_status "Packaging CloudFormation template..."
    aws cloudformation package \
        --template-file $TEMPLATE_FILE \
        --s3-bucket $DEPLOYMENT_BUCKET \
        --output-template-file $PACKAGED_TEMPLATE \
        --region $REGION
    
    # Deploy the stack
    print_status "Deploying CloudFormation stack: $STACK_NAME-$ENVIRONMENT"
    
    aws cloudformation deploy \
        --template-file $PACKAGED_TEMPLATE \
        --stack-name $STACK_NAME-$ENVIRONMENT \
        --parameter-overrides \
            Environment=$ENVIRONMENT \
            VantaApiKey=$VANTA_API_KEY \
            KMSKeyAlias=$KMS_KEY_ALIAS \
        --capabilities CAPABILITY_NAMED_IAM \
        --region $REGION
    
    if [ $? -eq 0 ]; then
        print_status "CloudFormation stack deployed successfully"
    else
        print_error "CloudFormation deployment failed"
        exit 1
    fi
}

# Function to get stack outputs
get_stack_outputs() {
    print_status "Retrieving stack outputs..."
    
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME-$ENVIRONMENT \
        --region $REGION \
        --query 'Stacks[0].Outputs' \
        --output table
}

# Function to setup local development environment
setup_local_dev() {
    print_status "Setting up local development environment..."
    
    # Create .env file for backend
    cat > ../backend/.env << EOF
# AWS Configuration
AWS_REGION=$REGION
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)

# Vanta API Configuration
VANTA_API_KEY=$VANTA_API_KEY
VANTA_API_BASE_URL=https://api.vanta.com/v1

# Application Configuration
APP_NAME=FinTrust AI
APP_VERSION=1.0.0
DEBUG=True

# Security Configuration
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# S3 Configuration
S3_BUCKET_NAME=fintrust-ai-reports-$ENVIRONMENT-$(aws sts get-caller-identity --query Account --output text)
KMS_KEY_ID=alias/$KMS_KEY_ALIAS-$ENVIRONMENT

# CloudWatch Configuration
CLOUDWATCH_LOG_GROUP=fintrust-ai-logs
EOF

    print_status "Local development environment configured"
    print_warning "Please review and update the .env file as needed"
}

# Function to run tests
run_tests() {
    print_status "Running deployment tests..."
    
    # Test S3 bucket access
    BUCKET_NAME=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME-$ENVIRONMENT \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
        --output text)
    
    if aws s3 ls s3://$BUCKET_NAME --region $REGION &> /dev/null; then
        print_status "S3 bucket access test passed"
    else
        print_error "S3 bucket access test failed"
        exit 1
    fi
    
    # Test Lambda function
    FUNCTION_NAME=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME-$ENVIRONMENT \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionName`].OutputValue' \
        --output text)
    
    if aws lambda invoke \
        --function-name $FUNCTION_NAME \
        --region $REGION \
        --payload '{}' \
        /tmp/lambda-response.json &> /dev/null; then
        print_status "Lambda function test passed"
    else
        print_error "Lambda function test failed"
        exit 1
    fi
    
    print_status "All deployment tests passed"
}

# Function to cleanup deployment artifacts
cleanup() {
    print_status "Cleaning up deployment artifacts..."
    
    if [ -f "packaged-template.yaml" ]; then
        rm packaged-template.yaml
    fi
    
    if [ -f "/tmp/lambda-response.json" ]; then
        rm /tmp/lambda-response.json
    fi
    
    print_status "Cleanup completed"
}

# Main deployment function
main() {
    print_status "Starting FinTrust AI deployment..."
    print_status "Environment: $ENVIRONMENT"
    print_status "Region: $REGION"
    print_status "Stack Name: $STACK_NAME-$ENVIRONMENT"
    
    # Pre-deployment checks
    check_aws_cli
    check_parameters
    
    # Create deployment bucket
    DEPLOYMENT_BUCKET=$(create_deployment_bucket)
    
    # Deploy the stack
    deploy_stack
    
    # Get stack outputs
    get_stack_outputs
    
    # Setup local development
    setup_local_dev
    
    # Run tests
    run_tests
    
    # Cleanup
    cleanup
    
    print_status "FinTrust AI deployment completed successfully!"
    print_status "Next steps:"
    print_status "1. Review the stack outputs above"
    print_status "2. Update your local .env file if needed"
    print_status "3. Start the backend: cd backend && uvicorn main:app --reload"
    print_status "4. Start the frontend: cd frontend && npm run dev"
}

# Handle command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --environment|-e)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --region|-r)
            REGION="$2"
            shift 2
            ;;
        --vanta-api-key|-k)
            VANTA_API_KEY="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -e, --environment    Environment name (dev, staging, prod)"
            echo "  -r, --region         AWS region"
            echo "  -k, --vanta-api-key  Vanta API key"
            echo "  -h, --help          Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main
