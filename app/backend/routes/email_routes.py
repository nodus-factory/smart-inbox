"""
Email routes for Smart Inbox Application
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.models.models import Email
from app.backend.email.email_handler import get_email_handler
from app.backend.routes.routing_engine import RoutingEngine
from app.utils.db import get_db

router = APIRouter(
    prefix="/emails",
    tags=["emails"],
    responses={404: {"description": "Not found"}},
)

# Initialize routing engine
routing_engine = RoutingEngine()

@router.get("/", response_model=List[Dict[str, Any]])
async def get_emails(
    skip: int = 0, 
    limit: int = 100, 
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    Get list of emails with optional filtering
    """
    query = db.query(Email)
    
    if status:
        query = query.filter(Email.status == status)
    
    emails = query.order_by(Email.received_at.desc()).offset(skip).limit(limit).all()
    return emails

@router.get("/{email_id}", response_model=Dict[str, Any])
async def get_email(email_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific email
    """
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@router.post("/receive", response_model=Dict[str, Any])
async def receive_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Webhook for receiving emails
    """
    # This endpoint will be called by external services or scheduled tasks
    # It will trigger the email reception process in the background
    background_tasks.add_task(process_incoming_emails, db)
    
    return {"status": "success", "message": "Email reception process started"}

@router.put("/{email_id}/manual-review", response_model=Dict[str, Any])
async def update_email_after_review(
    email_id: int, 
    review_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Update email after manual review
    """
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Update email with review data
    email.classification = review_data.get("classification")
    email.client_id = review_data.get("client_id")
    email.status = "processed"
    
    # Process the email based on the manual review
    client = db.query(Client).filter(Client.id == email.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Route the email based on the manual classification
    routing_result = routing_engine.route_email(
        email_data={
            "id": email.id,
            "sender": email.sender,
            "recipient": email.recipient,
            "subject": email.subject,
            "body": email.body,
            "attachments": email.attachments
        },
        client_data={
            "id": client.id,
            "name": client.name,
            "github_repository": client.github_repository,
            "technical_contact": client.technical_contact,
            "commercial_contact": client.commercial_contact,
            "administrative_contact": client.administrative_contact
        },
        classification=email.classification
    )
    
    # Update email with routing result
    email.routing_action = routing_result.get("action")
    email.action_reference = routing_result.get("reference")
    email.processed_at = datetime.datetime.utcnow()
    
    # Add log entry
    log = Log(
        email_id=email.id,
        action="manual_review",
        details=f"Manual review completed. Classification: {email.classification}",
        status="success" if routing_result.get("success") else "failure",
        error=routing_result.get("message") if not routing_result.get("success") else None
    )
    
    db.add(log)
    db.commit()
    
    return {
        "status": "success",
        "email_id": email.id,
        "routing_result": routing_result
    }

# Background task for processing incoming emails
async def process_incoming_emails(db: Session):
    """
    Process incoming emails from configured email services
    """
    email_handler = get_email_handler()
    
    try:
        # Receive emails
        emails = email_handler.receive_emails()
        
        for email_data in emails:
            # Check if email already exists
            existing_email = db.query(Email).filter(Email.message_id == email_data["message_id"]).first()
            if existing_email:
                continue
            
            # Create new email record
            email = Email(
                message_id=email_data["message_id"],
                sender=email_data["sender"],
                recipient=email_data["recipient"],
                subject=email_data["subject"],
                body=email_data["body"],
                attachments=email_data.get("attachments", []),
                received_at=datetime.datetime.utcnow(),
                status="pending"
            )
            
            db.add(email)
            db.commit()
            
            # Identify client
            client = identify_client(email_data, db)
            
            if client:
                email.client_id = client.id
                
                # Process email with routing engine
                result = routing_engine.process_email(
                    email_data={
                        "id": email.id,
                        "sender": email.sender,
                        "recipient": email.recipient,
                        "subject": email.subject,
                        "body": email.body,
                        "attachments": email.attachments
                    },
                    client_data={
                        "id": client.id,
                        "name": client.name,
                        "github_repository": client.github_repository,
                        "technical_contact": client.technical_contact,
                        "commercial_contact": client.commercial_contact,
                        "administrative_contact": client.administrative_contact
                    }
                )
                
                # Update email with processing result
                email.classification = result.get("classification")
                email.confidence_score = result.get("confidence")
                email.routing_action = result.get("action")
                email.action_reference = result.get("reference")
                
                if result.get("action") == "manual_review":
                    email.status = "pending"
                else:
                    email.status = "processed" if result.get("success") else "error"
                    email.error_message = result.get("message") if not result.get("success") else None
                    email.processed_at = datetime.datetime.utcnow()
                
                # Add log entry
                log = Log(
                    email_id=email.id,
                    action="processing",
                    details=f"Email processed. Classification: {email.classification}, Action: {email.routing_action}",
                    status="success" if result.get("success") else "failure",
                    error=result.get("message") if not result.get("success") else None
                )
                
                db.add(log)
            else:
                # No client identified, mark for manual review
                email.status = "pending"
                email.routing_action = "manual_review"
                
                # Add log entry
                log = Log(
                    email_id=email.id,
                    action="client_identification",
                    details="No client identified for this email",
                    status="failure",
                    error="Unable to identify client"
                )
                
                db.add(log)
            
            db.commit()
    
    except Exception as e:
        # Log error
        log = Log(
            action="email_reception",
            details="Error receiving emails",
            status="failure",
            error=str(e)
        )
        
        db.add(log)
        db.commit()

# Helper function to identify client
def identify_client(email_data, db):
    """
    Identify client based on email data
    """
    # Get all clients
    clients = db.query(Client).all()
    
    # Check by email domain
    sender_domain = email_data["sender"].split('@')[-1]
    for client in clients:
        # Check domains
        if client.domains and sender_domain in client.domains:
            return client
        
        # Check authorized emails
        if client.authorized_emails and email_data["sender"] in client.authorized_emails:
            return client
        
        # Check signature patterns
        if client.signature_patterns and email_data["body"]:
            for pattern in client.signature_patterns:
                if re.search(pattern, email_data["body"]):
                    return client
    
    return None
