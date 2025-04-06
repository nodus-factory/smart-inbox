"""
Utility functions for Smart Inbox Application
"""

import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def extract_domain_from_email(email: str) -> Optional[str]:
    """
    Extract domain from email address
    
    Args:
        email: Email address
        
    Returns:
        Domain or None if invalid email
    """
    try:
        return email.split('@')[-1]
    except:
        return None

def match_pattern_in_text(pattern: str, text: str) -> bool:
    """
    Check if pattern matches in text
    
    Args:
        pattern: Regex pattern
        text: Text to search in
        
    Returns:
        True if pattern matches, False otherwise
    """
    try:
        return bool(re.search(pattern, text))
    except:
        logger.error(f"Invalid regex pattern: {pattern}")
        return False

def format_github_issue_body(email_data: Dict, client_name: str) -> str:
    """
    Format email data into GitHub issue body
    
    Args:
        email_data: Email data dictionary
        client_name: Name of the client
        
    Returns:
        Formatted issue body
    """
    body = f"## Email from {client_name}\n\n"
    body += f"**From:** {email_data.get('sender', 'Unknown')}\n"
    body += f"**Date:** {email_data.get('date', 'Unknown')}\n"
    body += f"**Subject:** {email_data.get('subject', 'No subject')}\n\n"
    body += "## Content\n\n"
    body += email_data.get('body', 'No content')
    
    # Add attachments section if any
    if email_data.get('attachments'):
        body += "\n\n## Attachments\n\n"
        for attachment in email_data['attachments']:
            body += f"- {attachment}\n"
    
    return body

def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text
    """
    # Remove potentially dangerous characters
    return re.sub(r'[<>&;]', '', text)

def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_github_repo(repo: str) -> bool:
    """
    Validate GitHub repository format (owner/repo)
    
    Args:
        repo: Repository string
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$'
    return bool(re.match(pattern, repo))
