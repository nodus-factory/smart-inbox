"""
Email handling module for Smart Inbox Application
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
from typing import Dict, List, Optional, Tuple
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64

from app.config.settings import EMAIL_SETTINGS, GMAIL_API

logger = logging.getLogger(__name__)

class EmailHandler:
    """Base class for email handling"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def receive_emails(self):
        """Method to be implemented by subclasses"""
        raise NotImplementedError
    
    def forward_email(self, email_data: Dict, destination: str) -> bool:
        """Method to be implemented by subclasses"""
        raise NotImplementedError
    
    @staticmethod
    def parse_email(raw_email) -> Dict:
        """Parse raw email into structured format"""
        raise NotImplementedError


class ImapSmtpHandler(EmailHandler):
    """Email handler using IMAP for receiving and SMTP for sending"""
    
    def __init__(self):
        super().__init__()
        self.imap_server = EMAIL_SETTINGS["imap_server"]
        self.smtp_server = EMAIL_SETTINGS["smtp_server"]
        self.smtp_port = EMAIL_SETTINGS["smtp_port"]
        self.central_inbox = EMAIL_SETTINGS["central_inbox"]
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")
    
    def connect_imap(self) -> imaplib.IMAP4_SSL:
        """Connect to IMAP server"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.username, self.password)
            return mail
        except Exception as e:
            self.logger.error(f"IMAP connection error: {str(e)}")
            raise
    
    def receive_emails(self) -> List[Dict]:
        """Receive emails from IMAP server"""
        mail = self.connect_imap()
        mail.select('inbox')
        
        # Search for unread emails
        status, data = mail.search(None, 'UNSEEN')
        if status != 'OK':
            self.logger.error("Failed to search for emails")
            mail.logout()
            return []
        
        email_ids = data[0].split()
        emails = []
        
        for email_id in email_ids:
            status, data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                self.logger.error(f"Failed to fetch email {email_id}")
                continue
            
            raw_email = data[0][1]
            email_data = self.parse_email(raw_email)
            emails.append(email_data)
            
            # Mark as read
            mail.store(email_id, '+FLAGS', '\\Seen')
        
        mail.logout()
        return emails
    
    def forward_email(self, email_data: Dict, destination: str) -> bool:
        """Forward email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.central_inbox
            msg['To'] = destination
            msg['Subject'] = f"FWD: {email_data['subject']}"
            
            # Add original sender info to body
            body = f"From: {email_data['sender']}\n"
            body += f"Subject: {email_data['subject']}\n\n"
            body += email_data['body']
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email forwarded to {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to forward email: {str(e)}")
            return False
    
    @staticmethod
    def parse_email(raw_email) -> Dict:
        """Parse raw email into structured format"""
        msg = email.message_from_bytes(raw_email)
        
        # Extract basic headers
        email_data = {
            'message_id': msg.get('Message-ID', ''),
            'sender': msg.get('From', ''),
            'recipient': msg.get('To', ''),
            'subject': msg.get('Subject', ''),
            'date': msg.get('Date', ''),
            'body': '',
            'attachments': []
        }
        
        # Extract body and attachments
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                
                # Skip multipart containers
                if content_type == 'multipart/alternative':
                    continue
                
                # Handle attachments
                if 'attachment' in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        email_data['attachments'].append(filename)
                # Handle text parts
                elif content_type == 'text/plain':
                    email_data['body'] += part.get_payload(decode=True).decode()
                elif content_type == 'text/html' and not email_data['body']:
                    # Use HTML if no plain text is available
                    email_data['body'] += part.get_payload(decode=True).decode()
        else:
            # Handle non-multipart messages
            email_data['body'] = msg.get_payload(decode=True).decode()
        
        return email_data


class GmailApiHandler(EmailHandler):
    """Email handler using Gmail API"""
    
    def __init__(self):
        super().__init__()
        self.central_inbox = EMAIL_SETTINGS["central_inbox"]
        self.credentials_file = GMAIL_API["credentials_file"]
        self.token_file = GMAIL_API["token_file"]
        self.scopes = GMAIL_API["scopes"]
        self.service = self._get_gmail_service()
    
    def _get_gmail_service(self):
        """Get authenticated Gmail API service"""
        creds = None
        
        # Load credentials from token file if it exists
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_info(
                json.loads(open(self.token_file).read()),
                self.scopes
            )
        
        # If credentials don't exist or are invalid, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)
    
    def receive_emails(self) -> List[Dict]:
        """Receive emails using Gmail API"""
        try:
            # Get list of unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread'
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                email_data = self._parse_gmail_message(msg)
                emails.append(email_data)
                
                # Mark as read
                self.service.users().messages().modify(
                    userId='me',
                    id=message['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
            
            return emails
        except Exception as e:
            self.logger.error(f"Gmail API error: {str(e)}")
            return []
    
    def forward_email(self, email_data: Dict, destination: str) -> bool:
        """Forward email using Gmail API"""
        try:
            # Create message
            message = MIMEMultipart()
            message['from'] = self.central_inbox
            message['to'] = destination
            message['subject'] = f"FWD: {email_data['subject']}"
            
            # Add original sender info to body
            body = f"From: {email_data['sender']}\n"
            body += f"Subject: {email_data['subject']}\n\n"
            body += email_data['body']
            
            message.attach(MIMEText(body, 'plain'))
            
            # Encode message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            self.service.users().messages().send(
                userId='me',
                body={'raw': encoded_message}
            ).execute()
            
            self.logger.info(f"Email forwarded to {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to forward email: {str(e)}")
            return False
    
    def _parse_gmail_message(self, msg) -> Dict:
        """Parse Gmail API message into structured format"""
        headers = msg['payload']['headers']
        parts = msg['payload'].get('parts', [])
        
        # Extract headers
        email_data = {
            'message_id': msg['id'],
            'sender': '',
            'recipient': '',
            'subject': '',
            'body': '',
            'attachments': []
        }
        
        for header in headers:
            name = header['name'].lower()
            if name == 'from':
                email_data['sender'] = header['value']
            elif name == 'to':
                email_data['recipient'] = header['value']
            elif name == 'subject':
                email_data['subject'] = header['value']
        
        # Extract body and attachments
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body_data = part['body'].get('data', '')
                    if body_data:
                        email_data['body'] = base64.urlsafe_b64decode(body_data).decode()
                elif part['mimeType'] == 'text/html' and not email_data['body']:
                    body_data = part['body'].get('data', '')
                    if body_data:
                        email_data['body'] = base64.urlsafe_b64decode(body_data).decode()
                elif 'filename' in part:
                    email_data['attachments'].append(part['filename'])
        else:
            # Handle messages without parts
            body_data = msg['payload']['body'].get('data', '')
            if body_data:
                email_data['body'] = base64.urlsafe_b64decode(body_data).decode()
        
        return email_data


def get_email_handler() -> EmailHandler:
    """Factory function to get appropriate email handler"""
    # Check if Gmail API credentials exist
    if os.path.exists(GMAIL_API["credentials_file"]):
        return GmailApiHandler()
    else:
        return ImapSmtpHandler()
