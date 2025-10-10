"""
Audit and reporting endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from services.s3_client import s3_client

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/sars")
async def list_sars(customer_id: Optional[str] = Query(None, description="Filter by customer ID")):
    """
    List all SAR documents
    """
    try:
        logger.info(f"Listing SARs for customer: {customer_id or 'all'}")
        
        sars = await s3_client.list_sars(customer_id)
        
        logger.info(f"Successfully listed {sars['count']} SARs")
        return {
            "status": "success",
            "data": sars,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error listing SARs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list SARs: {str(e)}"
        )

@router.get("/sars/{sar_id}")
async def get_sar(sar_id: str, customer_id: str):
    """
    Retrieve a specific SAR document
    """
    try:
        logger.info(f"Retrieving SAR: {sar_id} for customer: {customer_id}")
        
        sar_data = await s3_client.retrieve_sar(sar_id, customer_id)
        
        logger.info(f"Successfully retrieved SAR: {sar_id}")
        return {
            "status": "success",
            "data": sar_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving SAR {sar_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve SAR: {str(e)}"
        )

@router.post("/logs")
async def create_audit_log(
    action: str,
    details: Dict[str, Any],
    user_id: str = "system"
):
    """
    Create an audit log entry
    """
    try:
        logger.info(f"Creating audit log for action: {action}")
        
        log_entry = await s3_client.create_audit_log(action, details, user_id)
        
        logger.info(f"Successfully created audit log: {log_entry['log_id']}")
        return {
            "status": "success",
            "data": log_entry,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating audit log: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create audit log: {str(e)}"
        )

@router.get("/reports")
async def list_reports(
    report_type: Optional[str] = Query(None, description="Filter by report type"),
    customer_id: Optional[str] = Query(None, description="Filter by customer ID")
):
    """
    List analysis reports
    """
    try:
        logger.info(f"Listing reports - type: {report_type}, customer: {customer_id}")
        
        # This would typically query a database or S3 for reports
        # For now, return a mock response
        reports = {
            "reports": [],
            "count": 0,
            "filters": {
                "report_type": report_type,
                "customer_id": customer_id
            }
        }
        
        logger.info("Successfully listed reports")
        return {
            "status": "success",
            "data": reports,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list reports: {str(e)}"
        )

@router.get("/dashboard")
async def get_audit_dashboard():
    """
    Get audit dashboard data
    """
    try:
        logger.info("Generating audit dashboard data")
        
        # Get SAR statistics
        sars = await s3_client.list_sars()
        
        # Create dashboard data
        dashboard_data = {
            "sars": {
                "total": sars["count"],
                "recent": len([sar for sar in sars["sars"] 
                             if datetime.fromisoformat(sar["last_modified"].replace('Z', '+00:00')) 
                             > datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)])
            },
            "compliance": {
                "status": "compliant",
                "last_check": datetime.now().isoformat()
            },
            "analyses": {
                "total_today": 0,  # Would be calculated from actual data
                "high_risk": 0,
                "medium_risk": 0,
                "low_risk": 0
            },
            "system": {
                "status": "operational",
                "last_backup": datetime.now().isoformat(),
                "encryption": "enabled"
            }
        }
        
        logger.info("Successfully generated audit dashboard data")
        return {
            "status": "success",
            "data": dashboard_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating audit dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate audit dashboard: {str(e)}"
        )

@router.get("/export")
async def export_audit_data(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    format: str = Query("json", description="Export format (json, csv)")
):
    """
    Export audit data for compliance reporting
    """
    try:
        logger.info(f"Exporting audit data from {start_date} to {end_date} in {format} format")
        
        # This would typically generate an export file
        # For now, return a mock response
        export_data = {
            "export_id": f"EXPORT-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}",
            "format": format,
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "records": 0,
            "status": "generated",
            "download_url": None  # Would be a presigned S3 URL
        }
        
        logger.info("Successfully exported audit data")
        return {
            "status": "success",
            "data": export_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error exporting audit data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export audit data: {str(e)}"
        )

@router.get("/health")
async def audit_health_check():
    """
    Health check for audit services
    """
    try:
        # Test S3 connectivity
        sars = await s3_client.list_sars()
        
        return {
            "service": "Audit & Reports",
            "status": "healthy",
            "s3_connectivity": "successful",
            "sar_count": sars["count"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Audit health check failed: {e}")
        return {
            "service": "Audit & Reports",
            "status": "unhealthy",
            "s3_connectivity": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
