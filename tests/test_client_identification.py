"""
Test script for client identification functionality
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import json

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backend.routes.email_routes import identify_client
from app.models.models import Client

class TestClientIdentification(unittest.TestCase):
    """Test cases for client identification functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Sample email data
        self.email_data = {
            'message_id': '<test123@example.com>',
            'sender': 'client@acmecorp.com',
            'recipient': 'inbox@smartinbox.com',
            'subject': 'Test Subject',
            'body': 'This is a test email body with signature from Acme Corp.',
            'attachments': ['test.pdf']
        }
        
        # Sample clients
        self.clients = [
            MagicMock(
                id=1,
                name='Acme Corporation',
                domains=['acmecorp.com', 'acme-inc.org'],
                signature_patterns=['Acme Corp'],
                authorized_emails=['ceo@acmecorp.com'],
                github_repository='acme/support',
                technical_contact='tech@internal.com',
                commercial_contact='sales@internal.com',
                administrative_contact='admin@internal.com'
            ),
            MagicMock(
                id=2,
                name='Globex Industries',
                domains=['globex.com'],
                signature_patterns=['Globex'],
                authorized_emails=['contact@globex.com'],
                github_repository='globex/helpdesk',
                technical_contact='tech@internal.com',
                commercial_contact='sales@internal.com',
                administrative_contact='admin@internal.com'
            )
        ]
        
        # Mock database session
        self.db = MagicMock()
        self.db.query.return_value.all.return_value = self.clients
    
    def test_identify_client_by_domain(self):
        """Test client identification by email domain"""
        # Test with matching domain
        client = identify_client(self.email_data, self.db)
        self.assertEqual(client.id, 1)
        self.assertEqual(client.name, 'Acme Corporation')
        
        # Test with non-matching domain
        self.email_data['sender'] = 'client@unknown.com'
        client = identify_client(self.email_data, self.db)
        self.assertIsNone(client)
    
    def test_identify_client_by_authorized_email(self):
        """Test client identification by authorized email"""
        # Test with authorized email
        self.email_data['sender'] = 'ceo@acmecorp.com'
        client = identify_client(self.email_data, self.db)
        self.assertEqual(client.id, 1)
        self.assertEqual(client.name, 'Acme Corporation')
    
    def test_identify_client_by_signature(self):
        """Test client identification by signature pattern"""
        # Test with matching signature pattern
        self.email_data['sender'] = 'client@unknown.com'
        client = identify_client(self.email_data, self.db)
        self.assertEqual(client.id, 1)
        self.assertEqual(client.name, 'Acme Corporation')
        
        # Test with different signature pattern
        self.email_data['body'] = 'This is a test email body with signature from Globex.'
        client = identify_client(self.email_data, self.db)
        self.assertEqual(client.id, 2)
        self.assertEqual(client.name, 'Globex Industries')
        
        # Test with no matching signature
        self.email_data['body'] = 'This is a test email body with no recognizable signature.'
        client = identify_client(self.email_data, self.db)
        self.assertIsNone(client)
    
    def test_no_client_match(self):
        """Test when no client matches"""
        # Test with non-matching data
        self.email_data['sender'] = 'client@unknown.com'
        self.email_data['body'] = 'This is a test email body with no recognizable signature.'
        client = identify_client(self.email_data, self.db)
        self.assertIsNone(client)

if __name__ == '__main__':
    unittest.main()
