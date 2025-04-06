"""
Smart Inbox Application - Main Configuration File
"""

# Application settings
APP_NAME = "Smart Inbox"
DEBUG = True
SECRET_KEY = "development_secret_key"  # Change in production

# Email settings
EMAIL_SETTINGS = {
    "imap_server": "imap.gmail.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "central_inbox": "inbox@example.com",  # Replace with actual inbox
    "check_interval": 60,  # seconds
}

# Gmail API settings
GMAIL_API = {
    "credentials_file": "credentials.json",
    "token_file": "token.json",
    "scopes": [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send",
    ],
}

# GitHub API settings
GITHUB_API = {
    "access_token": "",  # To be set via environment variable
    "default_repo": "owner/repository",  # Default repository for issues
    "issue_labels": ["client-email", "auto-generated"],
}

# AI Classification settings
AI_SETTINGS = {
    "provider": "openai",
    "api_key": "",  # To be set via environment variable
    "model": "gpt-3.5-turbo",
    "confidence_threshold": 0.7,  # Minimum confidence score to avoid manual review
}

# Database settings
DATABASE = {
    "development": {
        "engine": "sqlite",
        "name": "smart_inbox.db",
    },
    "production": {
        "engine": "postgresql",
        "host": "localhost",
        "port": 5432,
        "name": "smart_inbox",
        "user": "postgres",
        "password": "",  # To be set via environment variable
    },
}

# Logging settings
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "smart_inbox.log",
}

# Frontend settings
FRONTEND = {
    "host": "localhost",
    "port": 3000,
    "api_url": "http://localhost:8000/api",
}

# Backend API settings
API = {
    "host": "0.0.0.0",
    "port": 8000,
    "prefix": "/api",
}
