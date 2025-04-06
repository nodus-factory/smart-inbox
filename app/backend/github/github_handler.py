"""
GitHub integration module for Smart Inbox Application
"""

import logging
import os
from typing import Dict, Optional
from github import Github, GithubException

from app.config.settings import GITHUB_API

logger = logging.getLogger(__name__)

class GitHubHandler:
    """Handler for GitHub API interactions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.access_token = os.getenv("GITHUB_ACCESS_TOKEN", GITHUB_API["access_token"])
        self.default_repo = GITHUB_API["default_repo"]
        self.issue_labels = GITHUB_API["issue_labels"]
        self.github = Github(self.access_token)
    
    def create_issue(self, 
                     title: str, 
                     body: str, 
                     repository: Optional[str] = None, 
                     labels: Optional[list] = None) -> Dict:
        """
        Create a GitHub issue
        
        Args:
            title: Issue title
            body: Issue body/description
            repository: Repository in format 'owner/repo', defaults to configured default_repo
            labels: List of labels to apply, defaults to configured issue_labels
            
        Returns:
            Dict containing issue details or error information
        """
        try:
            # Use provided repository or default
            repo_name = repository or self.default_repo
            repo = self.github.get_repo(repo_name)
            
            # Use provided labels or default
            issue_labels = labels or self.issue_labels
            
            # Create issue
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=issue_labels
            )
            
            self.logger.info(f"Created GitHub issue #{issue.number} in {repo_name}")
            
            return {
                "success": True,
                "issue_number": issue.number,
                "issue_url": issue.html_url,
                "repository": repo_name
            }
        except GithubException as e:
            self.logger.error(f"GitHub API error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": e.status
            }
        except Exception as e:
            self.logger.error(f"Unexpected error creating GitHub issue: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def format_issue_from_email(self, email_data: Dict, client_name: str) -> Dict:
        """
        Format email data into GitHub issue format
        
        Args:
            email_data: Email data dictionary
            client_name: Name of the client
            
        Returns:
            Dict with formatted title and body
        """
        # Create issue title
        title = f"[{client_name}] {email_data['subject']}"
        
        # Create issue body
        body = f"## Email from {client_name}\n\n"
        body += f"**From:** {email_data['sender']}\n"
        body += f"**Date:** {email_data['date']}\n"
        body += f"**Subject:** {email_data['subject']}\n\n"
        body += "## Content\n\n"
        body += email_data['body']
        
        # Add attachments section if any
        if email_data.get('attachments'):
            body += "\n\n## Attachments\n\n"
            for attachment in email_data['attachments']:
                body += f"- {attachment}\n"
        
        return {
            "title": title,
            "body": body
        }
    
    def test_connection(self) -> Dict:
        """
        Test GitHub API connection
        
        Returns:
            Dict with connection status
        """
        try:
            # Try to get user info to test connection
            user = self.github.get_user()
            return {
                "success": True,
                "username": user.login,
                "rate_limit": self.github.get_rate_limit().core.remaining
            }
        except GithubException as e:
            self.logger.error(f"GitHub API connection error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": e.status
            }
        except Exception as e:
            self.logger.error(f"Unexpected error testing GitHub connection: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
