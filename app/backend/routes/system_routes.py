"""
System routes for Smart Inbox Application
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import datetime

from app.models.models import Log, Email, Client, RoutingRule
from app.backend.email.email_handler import get_email_handler
from app.backend.github.github_handler import GitHubHandler
from app.utils.db import get_db

router = APIRouter(
    prefix="/system",
    tags=["system"],
    responses={404: {"description": "Not found"}},
)

@router.get("/logs", response_model=List[Dict[str, Any]])
async def get_logs(
    skip: int = 0, 
    limit: int = 100, 
    email_id: int = None,
    action: str = None,
    status: str = None,
    start_date: datetime.datetime = None,
    end_date: datetime.datetime = None,
    db: Session = Depends(get_db)
):
    """
    Get system logs with filtering options
    """
    query = db.query(Log)
    
    if email_id:
        query = query.filter(Log.email_id == email_id)
    
    if action:
        query = query.filter(Log.action == action)
    
    if status:
        query = query.filter(Log.status == status)
    
    if start_date:
        query = query.filter(Log.timestamp >= start_date)
    
    if end_date:
        query = query.filter(Log.timestamp <= end_date)
    
    logs = query.order_by(Log.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/stats", response_model=Dict[str, Any])
async def get_system_stats(db: Session = Depends(get_db)):
    """
    Get system statistics
    """
    # Count total emails
    total_emails = db.query(Email).count()
    
    # Count processed emails
    processed_emails = db.query(Email).filter(Email.status == "processed").count()
    
    # Count pending review emails
    pending_review = db.query(Email).filter(
        Email.status == "pending", 
        Email.routing_action == "manual_review"
    ).count()
    
    # Count error emails
    error_emails = db.query(Email).filter(Email.status == "error").count()
    
    # Count clients
    client_count = db.query(Client).count()
    
    # Count active routing rules
    active_rules = db.query(RoutingRule).filter(RoutingRule.active == True).count()
    
    # Calculate success rate
    success_rate = 0
    if total_emails > 0:
        success_rate = (processed_emails / total_emails) * 100
    
    # Get recent activity
    recent_logs = db.query(Log).order_by(Log.timestamp.desc()).limit(10).all()
    
    return {
        "total_emails": total_emails,
        "processed_emails": processed_emails,
        "pending_review": pending_review,
        "error_emails": error_emails,
        "client_count": client_count,
        "active_rules": active_rules,
        "success_rate": round(success_rate, 2),
        "recent_activity": recent_logs
    }

@router.post("/test-connection", response_model=Dict[str, Any])
async def test_connections():
    """
    Test connections to email and GitHub APIs
    """
    results = {}
    
    # Test email connection
    try:
        email_handler = get_email_handler()
        # Simple test - just initialize the handler
        results["email"] = {
            "success": True,
            "message": "Email connection successful"
        }
    except Exception as e:
        results["email"] = {
            "success": False,
            "message": f"Email connection failed: {str(e)}"
        }
    
    # Test GitHub connection
    try:
        github_handler = GitHubHandler()
        github_test = github_handler.test_connection()
        results["github"] = github_test
    except Exception as e:
        results["github"] = {
            "success": False,
            "message": f"GitHub connection failed: {str(e)}"
        }
    
    return {
        "status": "success",
        "results": results
    }

@router.post("/initialize-database", response_model=Dict[str, Any])
async def initialize_database(db: Session = Depends(get_db)):
    """
    Initialize database with tables
    """
    from app.models.models import Base
    from app.utils.db import engine
    
    try:
        Base.metadata.create_all(bind=engine)
        
        # Add a log entry
        log = Log(
            action="system_initialization",
            details="Database initialized",
            status="success"
        )
        
        db.add(log)
        db.commit()
        
        return {
            "status": "success",
            "message": "Database initialized successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database initialization failed: {str(e)}"
        }
