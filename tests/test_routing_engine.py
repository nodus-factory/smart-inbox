"""
Test script for routing engine functionality
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import json

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backend.routes.routing_engine import RoutingEngine

class TestRoutingEngine(unittest.TestCase):
    """Test cases for routing engine functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Sample email data
        self.email_data = {
            'id': 1,
            'sender': 'client@acmecorp.com',
            'recipient': 'inbox@smartinbox.com',
            'subject': 'API Integration Issue',
            'body': 'We are experiencing problems with the API integration.',
            'attachments': ['error_log.txt']
        }
        
        # Sample client data
        self.client_data = {
            'id': 1,
            'name': 'Acme Corporation',
            'github_repository': 'acme/support',
            'technical_contact': 'tech@internal.com',
            'commercial_contact': 'sales@internal.com',
            'administrative_contact': 'admin@internal.com'
        }
        
        # Create patches for dependencies
        self.email_handler_patcher = patch('app.backend.routes.routing_engine.get_email_handler')
        self.github_handler_patcher = patch('app.backend.routes.routing_engine.GitHubHandler')
        self.ai_classifier_patcher = patch('app.backend.routes.routing_engine.get_ai_classifier')
        
        # Start patches
        self.mock_email_handler = self.email_handler_patcher.start()
        self.mock_github_handler = self.github_handler_patcher.start()
        self.mock_ai_classifier = self.ai_classifier_patcher.start()
        
        # Setup mock instances
        self.mock_email_handler_instance = MagicMock()
        self.mock_github_handler_instance = MagicMock()
        self.mock_ai_classifier_instance = MagicMock()
        
        self.mock_email_handler.return_value = self.mock_email_handler_instance
        self.mock_github_handler.return_value = self.mock_github_handler_instance
        self.mock_ai_classifier.return_value = self.mock_ai_classifier_instance
        
        # Set default confidence threshold
        self.mock_ai_classifier_instance.confidence_threshold = 0.7
    
    def tearDown(self):
        """Clean up after tests"""
        self.email_handler_patcher.stop()
        self.github_handler_patcher.stop()
        self.ai_classifier_patcher.stop()
    
    def test_classify_email(self):
        """Test email classification"""
        # Setup mock
        self.mock_ai_classifier_instance.classify_email.return_value = ("technical", 0.85)
        
        # Create engine and classify email
        engine = RoutingEngine()
        classification, confidence = engine.classify_email(self.email_data['body'])
        
        # Verify method calls
        self.mock_ai_classifier_instance.classify_email.assert_called_once_with(self.email_data['body'])
        
        # Verify results
        self.assertEqual(classification, "technical")
        self.assertEqual(confidence, 0.85)
    
    def test_process_email_high_confidence(self):
        """Test processing email with high confidence classification"""
        # Setup mocks
        self.mock_ai_classifier_instance.classify_email.return_value = ("technical", 0.85)
        
        # Setup GitHub issue creation mock
        self.mock_github_handler_instance.format_issue_from_email.return_value = {
            "title": "[Acme Corporation] API Integration Issue",
            "body": "Issue body"
        }
        self.mock_github_handler_instance.create_issue.return_value = {
            "success": True,
            "issue_number": 123,
            "issue_url": "https://github.com/acme/support/issues/123"
        }
        
        # Create engine and process email
        engine = RoutingEngine()
        result = engine.process_email(self.email_data, self.client_data)
        
        # Verify classification was called
        self.mock_ai_classifier_instance.classify_email.assert_called_once_with(self.email_data['body'])
        
        # Verify GitHub issue was created
        self.mock_github_handler_instance.format_issue_from_email.assert_called_once()
        self.mock_github_handler_instance.create_issue.assert_called_once()
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "github_issue")
        self.assertEqual(result["classification"], "technical")
        self.assertEqual(result["confidence"], 0.85)
        self.assertEqual(result["reference"], "https://github.com/acme/support/issues/123")
    
    def test_process_email_low_confidence(self):
        """Test processing email with low confidence classification"""
        # Setup mocks
        self.mock_ai_classifier_instance.classify_email.return_value = ("technical", 0.65)
        
        # Create engine and process email
        engine = RoutingEngine()
        result = engine.process_email(self.email_data, self.client_data)
        
        # Verify classification was called
        self.mock_ai_classifier_instance.classify_email.assert_called_once_with(self.email_data['body'])
        
        # Verify no routing was performed
        self.mock_github_handler_instance.create_issue.assert_not_called()
        self.mock_email_handler_instance.forward_email.assert_not_called()
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "manual_review")
        self.assertEqual(result["classification"], "technical")
        self.assertEqual(result["confidence"], 0.65)
        self.assertEqual(result["message"], "Email flagged for manual review due to low confidence")
    
    def test_route_email_technical(self):
        """Test routing technical email to GitHub"""
        # Setup GitHub issue creation mock
        self.mock_github_handler_instance.format_issue_from_email.return_value = {
            "title": "[Acme Corporation] API Integration Issue",
            "body": "Issue body"
        }
        self.mock_github_handler_instance.create_issue.return_value = {
            "success": True,
            "issue_number": 123,
            "issue_url": "https://github.com/acme/support/issues/123"
        }
        
        # Create engine and route email
        engine = RoutingEngine()
        result = engine.route_email(self.email_data, self.client_data, "technical")
        
        # Verify GitHub issue was created
        self.mock_github_handler_instance.format_issue_from_email.assert_called_once()
        self.mock_github_handler_instance.create_issue.assert_called_once()
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "github_issue")
        self.assertEqual(result["destination"], "acme/support")
        self.assertEqual(result["reference"], "https://github.com/acme/support/issues/123")
    
    def test_route_email_commercial(self):
        """Test routing commercial email to internal contact"""
        # Setup email forwarding mock
        self.mock_email_handler_instance.forward_email.return_value = True
        
        # Create engine and route email
        engine = RoutingEngine()
        result = engine.route_email(self.email_data, self.client_data, "commercial")
        
        # Verify email was forwarded
        self.mock_email_handler_instance.forward_email.assert_called_once_with(
            self.email_data, "sales@internal.com"
        )
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "email_forward")
        self.assertEqual(result["destination"], "sales@internal.com")
        self.assertEqual(result["message"], "Forwarded email to commercial contact: sales@internal.com")
    
    def test_route_email_administrative(self):
        """Test routing administrative email to internal contact"""
        # Setup email forwarding mock
        self.mock_email_handler_instance.forward_email.return_value = True
        
        # Create engine and route email
        engine = RoutingEngine()
        result = engine.route_email(self.email_data, self.client_data, "administrative")
        
        # Verify email was forwarded
        self.mock_email_handler_instance.forward_email.assert_called_once_with(
            self.email_data, "admin@internal.com"
        )
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "email_forward")
        self.assertEqual(result["destination"], "admin@internal.com")
        self.assertEqual(result["message"], "Forwarded email to administrative contact: admin@internal.com")

if __name__ == '__main__':
    unittest.main()
