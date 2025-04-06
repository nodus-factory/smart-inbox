"""
Client routes for Smart Inbox Application
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json

from app.models.models import Client, RoutingRule
from app.utils.db import get_db

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list of clients
    """
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients

@router.post("/", response_model=Dict[str, Any])
async def create_client(client_data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Create a new client
    """
    # Convert list fields to JSON
    for field in ['domains', 'signature_patterns', 'authorized_emails']:
        if field in client_data and isinstance(client_data[field], list):
            client_data[field] = client_data[field]
    
    # Create new client
    client = Client(**client_data)
    db.add(client)
    db.commit()
    db.refresh(client)
    
    return client

@router.get("/{client_id}", response_model=Dict[str, Any])
async def get_client(client_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific client
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=Dict[str, Any])
async def update_client(client_id: int, client_data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Update client details
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Convert list fields to JSON
    for field in ['domains', 'signature_patterns', 'authorized_emails']:
        if field in client_data and isinstance(client_data[field], list):
            client_data[field] = client_data[field]
    
    # Update client attributes
    for key, value in client_data.items():
        setattr(client, key, value)
    
    db.commit()
    db.refresh(client)
    
    return client

@router.delete("/{client_id}", response_model=Dict[str, Any])
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    """
    Delete a client
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if client has routing rules
    rules = db.query(RoutingRule).filter(RoutingRule.client_id == client_id).all()
    if rules:
        # Delete associated routing rules
        for rule in rules:
            db.delete(rule)
    
    # Delete client
    db.delete(client)
    db.commit()
    
    return {"status": "success", "message": "Client deleted successfully"}

@router.get("/{client_id}/routing-rules", response_model=List[Dict[str, Any]])
async def get_client_routing_rules(client_id: int, db: Session = Depends(get_db)):
    """
    Get routing rules for a specific client
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    rules = db.query(RoutingRule).filter(RoutingRule.client_id == client_id).all()
    return rules
