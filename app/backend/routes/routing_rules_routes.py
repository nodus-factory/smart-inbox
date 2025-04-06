"""
Routing rules routes for Smart Inbox Application
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.models.models import RoutingRule, Client
from app.utils.db import get_db

router = APIRouter(
    prefix="/routing-rules",
    tags=["routing-rules"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_routing_rules(
    skip: int = 0, 
    limit: int = 100, 
    client_id: int = None,
    active: bool = None,
    db: Session = Depends(get_db)
):
    """
    Get list of routing rules with optional filtering
    """
    query = db.query(RoutingRule)
    
    if client_id:
        query = query.filter(RoutingRule.client_id == client_id)
    
    if active is not None:
        query = query.filter(RoutingRule.active == active)
    
    rules = query.order_by(RoutingRule.priority.desc()).offset(skip).limit(limit).all()
    return rules

@router.post("/", response_model=Dict[str, Any])
async def create_routing_rule(rule_data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Create a new routing rule
    """
    # Verify client exists
    client = db.query(Client).filter(Client.id == rule_data["client_id"]).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Create new rule
    rule = RoutingRule(**rule_data)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    return rule

@router.get("/{rule_id}", response_model=Dict[str, Any])
async def get_routing_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific routing rule
    """
    rule = db.query(RoutingRule).filter(RoutingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Routing rule not found")
    return rule

@router.put("/{rule_id}", response_model=Dict[str, Any])
async def update_routing_rule(rule_id: int, rule_data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Update routing rule
    """
    rule = db.query(RoutingRule).filter(RoutingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Routing rule not found")
    
    # If client_id is being updated, verify new client exists
    if "client_id" in rule_data and rule_data["client_id"] != rule.client_id:
        client = db.query(Client).filter(Client.id == rule_data["client_id"]).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
    
    # Update rule attributes
    for key, value in rule_data.items():
        setattr(rule, key, value)
    
    db.commit()
    db.refresh(rule)
    
    return rule

@router.delete("/{rule_id}", response_model=Dict[str, Any])
async def delete_routing_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Delete a routing rule
    """
    rule = db.query(RoutingRule).filter(RoutingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Routing rule not found")
    
    db.delete(rule)
    db.commit()
    
    return {"status": "success", "message": "Routing rule deleted successfully"}

@router.put("/{rule_id}/toggle-active", response_model=Dict[str, Any])
async def toggle_rule_active_status(rule_id: int, db: Session = Depends(get_db)):
    """
    Toggle active status of a routing rule
    """
    rule = db.query(RoutingRule).filter(RoutingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Routing rule not found")
    
    # Toggle active status
    rule.active = not rule.active
    db.commit()
    db.refresh(rule)
    
    return {
        "status": "success", 
        "rule_id": rule.id, 
        "active": rule.active,
        "message": f"Rule is now {'active' if rule.active else 'inactive'}"
    }
