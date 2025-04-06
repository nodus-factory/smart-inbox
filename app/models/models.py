"""
Database models for the Smart Inbox Application
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Client(Base):
    """Client model for storing client information"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    domains = Column(JSON, nullable=True)  # List of domains associated with client
    signature_patterns = Column(JSON, nullable=True)  # List of regex patterns for signature identification
    authorized_emails = Column(JSON, nullable=True)  # List of authorized email addresses
    github_repository = Column(String(255), nullable=True)  # GitHub repository for technical issues
    technical_contact = Column(String(255), nullable=True)  # Email for technical issues
    commercial_contact = Column(String(255), nullable=True)  # Email for commercial issues
    administrative_contact = Column(String(255), nullable=True)  # Email for administrative issues
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    routing_rules = relationship("RoutingRule", back_populates="client", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="client")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}')>"


class Email(Base):
    """Email model for storing processed emails"""
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    message_id = Column(String(255), unique=True, nullable=False)  # Original email message ID
    sender = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(512), nullable=True)
    body = Column(Text, nullable=True)
    attachments = Column(JSON, nullable=True)  # List of attachment filenames or references
    received_at = Column(DateTime, default=datetime.datetime.utcnow)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True)
    classification = Column(String(50), nullable=True)  # technical, commercial, administrative
    confidence_score = Column(Float, nullable=True)
    routing_action = Column(String(50), nullable=True)  # github_issue, email_forward, manual_review
    action_reference = Column(String(255), nullable=True)  # GitHub issue URL or forwarded email ID
    status = Column(String(50), default='pending')  # pending, processed, error
    error_message = Column(Text, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    client = relationship("Client", back_populates="emails")
    logs = relationship("Log", back_populates="email", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Email(id={self.id}, subject='{self.subject}', classification='{self.classification}')>"


class RoutingRule(Base):
    """Routing rule model for configuring email routing"""
    __tablename__ = 'routing_rules'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    classification = Column(String(50), nullable=False)  # technical, commercial, administrative
    action = Column(String(50), nullable=False)  # github_issue, email_forward
    destination = Column(String(255), nullable=False)  # GitHub repo or email address
    priority = Column(Integer, default=1)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="routing_rules")
    
    def __repr__(self):
        return f"<RoutingRule(id={self.id}, client_id={self.client_id}, classification='{self.classification}')>"


class Log(Base):
    """Log model for storing system actions"""
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=True)
    action = Column(String(50), nullable=False)  # client_identification, classification, routing, manual_review
    details = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)  # success, failure
    error = Column(Text, nullable=True)
    
    # Relationships
    email = relationship("Email", back_populates="logs")
    
    def __repr__(self):
        return f"<Log(id={self.id}, action='{self.action}', status='{self.status}')>"


class User(Base):
    """User model for admin interface authentication"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
