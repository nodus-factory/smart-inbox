"""
Test script for email handling functionality
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import json

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backend.email.email_handler import ImapSmtpHandler, GmailApiHandler, get_email_handler
from app.config.settings import EMAIL_SETTINGS, GMAIL_API

class TestEmailHandler(unittest.TestCase):
    """Test cases for email handling functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'EMAIL_USERNAME': 'test@example.com',
            'EMAIL_PASSWORD': 'test_password',
            'OPENAI_API_KEY': 'test_api_key'
        })
        self.env_patcher.start()
        
        # Sample email data
        self.sample_email = {
            'message_id': '<test123@example.com>',
            'sender': 'client@acmecorp.com',
            'recipient': 'inbox@smartinbox.com',
            'subject': 'Test Subject',
            'body': 'This is a test email body.',
            'attachments': ['test.pdf']
        }
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    @patch('app.backend.email.email_handler.imaplib.IMAP4_SSL')
    @patch('app.backend.email.email_handler.smtplib.SMTP')
    def test_imap_smtp_handler_initialization(self, mock_smtp, mock_imap):
        """Test ImapSmtpHandler initialization"""
        handler = ImapSmtpHandler()
        
        self.assertEqual(handler.imap_server, EMAIL_SETTINGS["imap_server"])
        self.assertEqual(handler.smtp_server, EMAIL_SETTINGS["smtp_server"])
        self.assertEqual(handler.smtp_port, EMAIL_SETTINGS["smtp_port"])
        self.assertEqual(handler.central_inbox, EMAIL_SETTINGS["central_inbox"])
        self.assertEqual(handler.username, 'test@example.com')
        self.assertEqual(handler.password, 'test_password')
    
    @patch('app.backend.email.email_handler.imaplib.IMAP4_SSL')
    def test_imap_connection(self, mock_imap):
        """Test IMAP connection"""
        # Setup mock
        mock_imap_instance = MagicMock()
        mock_imap.return_value = mock_imap_instance
        
        # Create handler and connect
        handler = ImapSmtpHandler()
        handler.connect_imap()
        
        # Verify connection
        mock_imap.assert_called_once_with(EMAIL_SETTINGS["imap_server"])
        mock_imap_instance.login.assert_called_once_with('test@example.com', 'test_password')
    
    @patch('app.backend.email.email_handler.imaplib.IMAP4_SSL')
    def test_receive_emails(self, mock_imap):
        """Test receiving emails via IMAP"""
        # Setup mock
        mock_imap_instance = MagicMock()
        mock_imap.return_value = mock_imap_instance
        
        # Mock search results
        mock_imap_instance.search.return_value = ('OK', [b'1 2 3'])
        
        # Mock fetch results for a single email
        mock_email_data = b'From: client@acmecorp.com\r\nTo: inbox@smartinbox.com\r\nSubject: Test Subject\r\n\r\nThis is a test email body.'
        mock_imap_instance.fetch.return_value = ('OK', [(b'1', (b'RFC822', mock_email_data))])
        
        # Create handler and receive emails
        handler = ImapSmtpHandler()
        
        # Mock parse_email method
        handler.parse_email = MagicMock(return_value=self.sample_email)
        
        emails = handler.receive_emails()
        
        # Verify method calls
        mock_imap_instance.select.assert_called_once_with('inbox')
        mock_imap_instance.search.assert_called_once_with(None, 'UNSEEN')
        mock_imap_instance.fetch.assert_called_once_with(b'1', '(RFC822)')
        mock_imap_instance.store.assert_called_once_with(b'1', '+FLAGS', '\\Seen')
        
        # Verify results
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0], self.sample_email)
    
    @patch('app.backend.email.email_handler.smtplib.SMTP')
    def test_forward_email(self, mock_smtp):
        """Test forwarding email via SMTP"""
        # Setup mock
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        
        # Create handler and forward email
        handler = ImapSmtpHandler()
        result = handler.forward_email(self.sample_email, 'tech@internal.com')
        
        # Verify method calls
        mock_smtp.assert_called_once_with(EMAIL_SETTINGS["smtp_server"], EMAIL_SETTINGS["smtp_port"])
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('test@example.com', 'test_password')
        mock_smtp_instance.send_message.assert_called_once()
        
        # Verify result
        self.assertTrue(result)
    
    @patch('app.backend.email.email_handler.os.path.exists')
    def test_get_email_handler(self, mock_exists):
        """Test email handler factory function"""
        # Test Gmail API handler when credentials exist
        mock_exists.return_value = True
        handler = get_email_handler()
        self.assertIsInstance(handler, GmailApiHandler)
        
        # Test IMAP/SMTP handler when credentials don't exist
        mock_exists.return_value = False
        handler = get_email_handler()
        self.assertIsInstance(handler, ImapSmtpHandler)

if __name__ == '__main__':
    unittest.main()
