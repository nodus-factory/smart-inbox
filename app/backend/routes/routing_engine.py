"""
Email routing module for Smart Inbox Application
"""

import logging
from typing import Dict, Optional, Tuple

from app.backend.email.email_handler import get_email_handler
from app.backend.github.github_handler import GitHubHandler
from app.backend.ai.classifier import get_ai_classifier

logger = logging.getLogger(__name__)

class RoutingEngine:
    """Engine for routing emails based on classification and client"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_handler = get_email_handler()
        self.github_handler = GitHubHandler()
        self.ai_classifier = get_ai_classifier()
    
    def process_email(self, email_data: Dict, client_data: Dict) -> Dict:
        """
        Process email and route based on classification and client data
        
        Args:
            email_data: Email data dictionary
            client_data: Client data dictionary
            
        Returns:
            Dict with processing results
        """
        try:
            # Step 1: Classify email
            classification, confidence = self.classify_email(email_data['body'])
            
            # Step 2: Determine if manual review is needed
            needs_manual_review = confidence < self.ai_classifier.confidence_threshold
            
            # Step 3: Route email based on classification
            if needs_manual_review:
                result = {
                    "success": True,
                    "action": "manual_review",
                    "classification": classification,
                    "confidence": confidence,
                    "message": "Email flagged for manual review due to low confidence"
                }
            else:
                # Route based on classification
                routing_result = self.route_email(email_data, client_data, classification)
                result = {
                    "success": routing_result["success"],
                    "action": routing_result["action"],
                    "classification": classification,
                    "confidence": confidence,
                    "destination": routing_result.get("destination"),
                    "reference": routing_result.get("reference"),
                    "message": routing_result.get("message")
                }
            
            return result
        except Exception as e:
            self.logger.error(f"Error processing email: {str(e)}")
            return {
                "success": False,
                "action": "error",
                "message": f"Error processing email: {str(e)}"
            }
    
    def classify_email(self, email_body: str) -> Tuple[str, float]:
        """
        Classify email content
        
        Args:
            email_body: Email body content
            
        Returns:
            Tuple of (classification, confidence_score)
        """
        return self.ai_classifier.classify_email(email_body)
    
    def route_email(self, email_data: Dict, client_data: Dict, classification: str) -> Dict:
        """
        Route email based on classification and client data
        
        Args:
            email_data: Email data dictionary
            client_data: Client data dictionary
            classification: Email classification (technical, commercial, administrative)
            
        Returns:
            Dict with routing results
        """
        if classification == "technical":
            # Create GitHub issue
            repository = client_data.get("github_repository")
            if not repository:
                self.logger.warning(f"No GitHub repository configured for client {client_data['name']}")
                return {
                    "success": False,
                    "action": "error",
                    "message": f"No GitHub repository configured for client {client_data['name']}"
                }
            
            # Format issue from email
            issue_data = self.github_handler.format_issue_from_email(email_data, client_data['name'])
            
            # Create issue
            issue_result = self.github_handler.create_issue(
                title=issue_data["title"],
                body=issue_data["body"],
                repository=repository
            )
            
            if issue_result["success"]:
                return {
                    "success": True,
                    "action": "github_issue",
                    "destination": repository,
                    "reference": issue_result["issue_url"],
                    "message": f"Created GitHub issue #{issue_result['issue_number']} in {repository}"
                }
            else:
                return {
                    "success": False,
                    "action": "error",
                    "message": f"Failed to create GitHub issue: {issue_result.get('error')}"
                }
        
        elif classification == "commercial":
            # Forward to commercial contact
            contact = client_data.get("commercial_contact")
            if not contact:
                self.logger.warning(f"No commercial contact configured for client {client_data['name']}")
                return {
                    "success": False,
                    "action": "error",
                    "message": f"No commercial contact configured for client {client_data['name']}"
                }
            
            # Forward email
            forward_result = self.email_handler.forward_email(email_data, contact)
            
            if forward_result:
                return {
                    "success": True,
                    "action": "email_forward",
                    "destination": contact,
                    "message": f"Forwarded email to commercial contact: {contact}"
                }
            else:
                return {
                    "success": False,
                    "action": "error",
                    "message": f"Failed to forward email to {contact}"
                }
        
        elif classification == "administrative":
            # Forward to administrative contact
            contact = client_data.get("administrative_contact")
            if not contact:
                self.logger.warning(f"No administrative contact configured for client {client_data['name']}")
                return {
                    "success": False,
                    "action": "error",
                    "message": f"No administrative contact configured for client {client_data['name']}"
                }
            
            # Forward email
            forward_result = self.email_handler.forward_email(email_data, contact)
            
            if forward_result:
                return {
                    "success": True,
                    "action": "email_forward",
                    "destination": contact,
                    "message": f"Forwarded email to administrative contact: {contact}"
                }
            else:
                return {
                    "success": False,
                    "action": "error",
                    "message": f"Failed to forward email to {contact}"
                }
        
        else:
            # Unknown classification
            self.logger.warning(f"Unknown classification: {classification}")
            return {
                "success": False,
                "action": "error",
                "message": f"Unknown classification: {classification}"
            }
