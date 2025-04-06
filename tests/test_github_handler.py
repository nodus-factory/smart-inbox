"""
Test script for GitHub integration functionality
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import json

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backend.github.github_handler import GitHubHandler
from app.config.settings import GITHUB_API

class TestGitHubHandler(unittest.TestCase):
    """Test cases for GitHub integration functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'GITHUB_ACCESS_TOKEN': 'test_github_token'
        })
        self.env_patcher.start()
        
        # Sample email data
        self.email_data = {
            'sender': 'client@acmecorp.com',
            'date': '2025-04-06T07:30:00Z',
            'subject': 'API Integration Issue',
            'body': 'We are experiencing problems with the API integration.',
            'attachments': ['error_log.txt']
        }
        
        # Sample client name
        self.client_name = 'Acme Corporation'
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    @patch('app.backend.github.github_handler.Github')
    def test_github_handler_initialization(self, mock_github):
        """Test GitHubHandler initialization"""
        handler = GitHubHandler()
        
        self.assertEqual(handler.access_token, 'test_github_token')
        self.assertEqual(handler.default_repo, GITHUB_API["default_repo"])
        self.assertEqual(handler.issue_labels, GITHUB_API["issue_labels"])
        mock_github.assert_called_once_with('test_github_token')
    
    @patch('app.backend.github.github_handler.Github')
    def test_create_issue(self, mock_github):
        """Test creating GitHub issue"""
        # Setup mock
        mock_github_instance = MagicMock()
        mock_github.return_value = mock_github_instance
        
        mock_repo = MagicMock()
        mock_github_instance.get_repo.return_value = mock_repo
        
        mock_issue = MagicMock()
        mock_issue.number = 123
        mock_issue.html_url = 'https://github.com/owner/repo/issues/123'
        mock_repo.create_issue.return_value = mock_issue
        
        # Create handler and issue
        handler = GitHubHandler()
        result = handler.create_issue(
            title='Test Issue',
            body='Test issue description',
            repository='owner/repo',
            labels=['bug', 'priority']
        )
        
        # Verify method calls
        mock_github_instance.get_repo.assert_called_once_with('owner/repo')
        mock_repo.create_issue.assert_called_once_with(
            title='Test Issue',
            body='Test issue description',
            labels=['bug', 'priority']
        )
        
        # Verify result
        self.assertTrue(result['success'])
        self.assertEqual(result['issue_number'], 123)
        self.assertEqual(result['issue_url'], 'https://github.com/owner/repo/issues/123')
        self.assertEqual(result['repository'], 'owner/repo')
    
    @patch('app.backend.github.github_handler.Github')
    def test_create_issue_with_error(self, mock_github):
        """Test creating GitHub issue with error"""
        # Setup mock with error
        mock_github_instance = MagicMock()
        mock_github.return_value = mock_github_instance
        
        from github import GithubException
        mock_github_instance.get_repo.side_effect = GithubException(404, {'message': 'Not Found'})
        
        # Create handler and issue
        handler = GitHubHandler()
        result = handler.create_issue(
            title='Test Issue',
            body='Test issue description'
        )
        
        # Verify result
        self.assertFalse(result['success'])
        self.assertEqual(result['status_code'], 404)
        self.assertIn('Not Found', result['error'])
    
    def test_format_issue_from_email(self):
        """Test formatting email data into GitHub issue format"""
        handler = GitHubHandler()
        issue_data = handler.format_issue_from_email(self.email_data, self.client_name)
        
        # Verify issue title
        self.assertEqual(issue_data['title'], '[Acme Corporation] API Integration Issue')
        
        # Verify issue body contains email data
        self.assertIn('## Email from Acme Corporation', issue_data['body'])
        self.assertIn('**From:** client@acmecorp.com', issue_data['body'])
        self.assertIn('**Subject:** API Integration Issue', issue_data['body'])
        self.assertIn('We are experiencing problems with the API integration.', issue_data['body'])
        self.assertIn('## Attachments', issue_data['body'])
        self.assertIn('- error_log.txt', issue_data['body'])
    
    @patch('app.backend.github.github_handler.Github')
    def test_test_connection(self, mock_github):
        """Test GitHub connection test"""
        # Setup mock
        mock_github_instance = MagicMock()
        mock_github.return_value = mock_github_instance
        
        mock_user = MagicMock()
        mock_user.login = 'test_user'
        mock_github_instance.get_user.return_value = mock_user
        
        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_github_instance.get_rate_limit.return_value = mock_rate_limit
        
        # Create handler and test connection
        handler = GitHubHandler()
        result = handler.test_connection()
        
        # Verify method calls
        mock_github_instance.get_user.assert_called_once()
        mock_github_instance.get_rate_limit.assert_called_once()
        
        # Verify result
        self.assertTrue(result['success'])
        self.assertEqual(result['username'], 'test_user')
        self.assertEqual(result['rate_limit'], 5000)

if __name__ == '__main__':
    unittest.main()
