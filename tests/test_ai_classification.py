"""
Test script for AI classification functionality
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import json

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backend.ai.classifier import OpenAIClassifier, CustomClassifier, get_ai_classifier
from app.config.settings import AI_SETTINGS

class TestAIClassification(unittest.TestCase):
    """Test cases for AI classification functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'OPENAI_API_KEY': 'test_api_key'
        })
        self.env_patcher.start()
        
        # Sample email content
        self.technical_email = """
        Hello Support Team,
        
        I'm experiencing an issue with the API integration. When I make a POST request to the /data endpoint,
        I'm getting a 500 error. Here's the error log:
        
        Error: Internal Server Error
        Stack trace: ...
        
        Can you please help me resolve this issue?
        
        Thanks,
        John
        """
        
        self.commercial_email = """
        Hello Sales Team,
        
        I'm interested in upgrading our current subscription plan. We currently have the Basic plan,
        but we'd like to move to the Premium plan. Can you please provide pricing information and
        details about the upgrade process?
        
        Best regards,
        Sarah
        """
        
        self.administrative_email = """
        Hello Admin,
        
        I need to update our account information. Our company has recently changed its address,
        and we need to update the billing information. Also, we'd like to add a new user to our account.
        
        Thanks,
        Mike
        """
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    @patch('app.backend.ai.classifier.openai.ChatCompletion.create')
    def test_openai_classifier(self, mock_openai):
        """Test OpenAI classifier"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "technical,0.85"
        mock_openai.return_value = mock_response
        
        # Create classifier and classify email
        classifier = OpenAIClassifier()
        classification, confidence = classifier.classify_email(self.technical_email)
        
        # Verify OpenAI API call
        mock_openai.assert_called_once()
        
        # Verify results
        self.assertEqual(classification, "technical")
        self.assertEqual(confidence, 0.85)
        
        # Test with different response
        mock_response.choices[0].message.content = "commercial,0.92"
        classification, confidence = classifier.classify_email(self.commercial_email)
        self.assertEqual(classification, "commercial")
        self.assertEqual(confidence, 0.92)
    
    def test_custom_classifier(self):
        """Test custom keyword-based classifier"""
        classifier = CustomClassifier()
        
        # Test technical email
        classification, confidence = classifier.classify_email(self.technical_email)
        self.assertEqual(classification, "technical")
        self.assertGreater(confidence, 0.5)
        
        # Test commercial email
        classification, confidence = classifier.classify_email(self.commercial_email)
        self.assertEqual(classification, "commercial")
        self.assertGreater(confidence, 0.5)
        
        # Test administrative email
        classification, confidence = classifier.classify_email(self.administrative_email)
        self.assertEqual(classification, "administrative")
        self.assertGreater(confidence, 0.5)
    
    @patch('app.backend.ai.classifier.os.getenv')
    def test_get_ai_classifier(self, mock_getenv):
        """Test AI classifier factory function"""
        # Test OpenAI classifier when API key is available
        mock_getenv.return_value = "test_api_key"
        classifier = get_ai_classifier()
        self.assertIsInstance(classifier, OpenAIClassifier)
        
        # Test custom classifier when API key is not available
        mock_getenv.return_value = None
        classifier = get_ai_classifier()
        self.assertIsInstance(classifier, CustomClassifier)

if __name__ == '__main__':
    unittest.main()
