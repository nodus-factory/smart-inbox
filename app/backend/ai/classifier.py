"""
AI classification module for Smart Inbox Application
"""

import logging
import os
from typing import Dict, Tuple
import openai

from app.config.settings import AI_SETTINGS

logger = logging.getLogger(__name__)

class AIClassifier:
    """Base class for AI-based email classification"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.confidence_threshold = AI_SETTINGS["confidence_threshold"]
    
    def classify_email(self, email_content: str) -> Tuple[str, float]:
        """
        Classify email content into categories
        
        Args:
            email_content: Email body content
            
        Returns:
            Tuple of (classification, confidence_score)
        """
        raise NotImplementedError


class OpenAIClassifier(AIClassifier):
    """Email classifier using OpenAI API"""
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("OPENAI_API_KEY", AI_SETTINGS["api_key"])
        self.model = AI_SETTINGS["model"]
        openai.api_key = self.api_key
    
    def classify_email(self, email_content: str) -> Tuple[str, float]:
        """
        Classify email content using OpenAI API
        
        Args:
            email_content: Email body content
            
        Returns:
            Tuple of (classification, confidence_score)
        """
        try:
            # Prepare prompt for classification
            prompt = f"""
            Classify the following email into one of these categories:
            - technical: Technical issues, bug reports, feature requests
            - commercial: Sales inquiries, pricing questions, contract discussions
            - administrative: Account management, general inquiries, scheduling
            
            Email content:
            {email_content[:1000]}  # Limit content length
            
            Respond with only the category name and confidence score (0-1) separated by a comma.
            Example: "technical,0.85"
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an email classification assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more deterministic results
                max_tokens=20     # Short response needed
            )
            
            # Parse response
            result = response.choices[0].message.content.strip()
            parts = result.split(',')
            
            if len(parts) == 2:
                classification = parts[0].strip().lower()
                try:
                    confidence = float(parts[1].strip())
                except ValueError:
                    confidence = 0.5  # Default if parsing fails
                
                # Validate classification
                valid_categories = ["technical", "commercial", "administrative"]
                if classification not in valid_categories:
                    self.logger.warning(f"Invalid classification: {classification}, defaulting to 'administrative'")
                    classification = "administrative"
                    confidence = 0.5
                
                self.logger.info(f"Classified email as '{classification}' with confidence {confidence}")
                return classification, confidence
            else:
                self.logger.error(f"Unexpected response format: {result}")
                return "administrative", 0.5  # Default to administrative with low confidence
                
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            return "administrative", 0.5  # Default to administrative with low confidence


class CustomClassifier(AIClassifier):
    """Simple keyword-based classifier as fallback"""
    
    def __init__(self):
        super().__init__()
        # Define keywords for each category
        self.keywords = {
            "technical": [
                "bug", "error", "issue", "problem", "crash", "fix", "feature",
                "request", "update", "upgrade", "install", "configuration",
                "setup", "deploy", "code", "api", "endpoint", "server",
                "database", "query", "exception", "log", "debug"
            ],
            "commercial": [
                "price", "cost", "quote", "purchase", "buy", "order", "invoice",
                "payment", "subscription", "license", "contract", "agreement",
                "proposal", "offer", "discount", "sale", "pricing", "plan",
                "package", "trial", "demo", "sales", "billing"
            ],
            "administrative": [
                "account", "login", "password", "access", "permission", "user",
                "profile", "settings", "preference", "schedule", "meeting",
                "appointment", "call", "contact", "support", "help", "assistance",
                "information", "question", "inquiry", "feedback", "suggestion"
            ]
        }
    
    def classify_email(self, email_content: str) -> Tuple[str, float]:
        """
        Classify email content using keyword matching
        
        Args:
            email_content: Email body content
            
        Returns:
            Tuple of (classification, confidence_score)
        """
        # Convert to lowercase for case-insensitive matching
        content = email_content.lower()
        
        # Count keyword matches for each category
        counts = {category: 0 for category in self.keywords}
        
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                counts[category] += content.count(keyword)
        
        # Find category with most matches
        if sum(counts.values()) == 0:
            # No matches found
            return "administrative", 0.5
        
        # Get category with highest count
        best_category = max(counts, key=counts.get)
        
        # Calculate confidence based on proportion of matches
        total_matches = sum(counts.values())
        confidence = counts[best_category] / total_matches
        
        self.logger.info(f"Classified email as '{best_category}' with confidence {confidence}")
        return best_category, confidence


def get_ai_classifier() -> AIClassifier:
    """Factory function to get appropriate AI classifier"""
    # Check if OpenAI API key is available
    if os.getenv("OPENAI_API_KEY") or AI_SETTINGS.get("api_key"):
        return OpenAIClassifier()
    else:
        return CustomClassifier()
