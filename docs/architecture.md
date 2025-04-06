# Smart Inbox Application - Architecture Design

## Overview
The Smart Inbox Application is an AI-assisted email routing system designed to serve as a single point of contact for client communications. The system automatically identifies clients, classifies emails using AI, and routes them to appropriate destinations based on configurable rules.

## System Architecture

### High-Level Components
1. **Email Reception Service**
   - Handles incoming emails via IMAP/SMTP and Gmail API
   - Extracts email metadata and content
   - Passes emails to the processing pipeline

2. **Client Identification Service**
   - Identifies clients based on email domains, signatures, and authorized email lists
   - Maintains client mapping database

3. **AI Classification Service**
   - Analyzes email content using natural language processing
   - Classifies emails into technical, commercial, or administrative categories
   - Flags emails for manual review when confidence is low

4. **Routing Engine**
   - Applies routing rules based on client identity and email classification
   - Creates GitHub issues for technical queries
   - Forwards emails to appropriate internal addresses for commercial/administrative queries

5. **Admin Interface**
   - No-code interface for configuring routing rules
   - Management of client identification settings
   - Manual review of flagged emails

6. **Logging and Monitoring**
   - Comprehensive logging of all system actions
   - Audit trail for debugging and traceability

### Data Flow
1. Email received → Email Reception Service
2. Email metadata extracted → Client Identification Service
3. Client identified + Email content → AI Classification Service
4. Client identity + Classification → Routing Engine
5. Routing action executed (GitHub issue creation or email forwarding)
6. All actions logged by Logging and Monitoring component

## Technical Architecture

### Backend (Python)
- **Framework**: FastAPI for RESTful API endpoints
- **Email Handling**: imaplib/smtplib for IMAP/SMTP, Google API Client for Gmail API
- **GitHub Integration**: PyGithub for GitHub API interactions
- **AI Classification**: OpenAI API for natural language processing
- **Database**: SQLite for development, PostgreSQL for production
- **Authentication**: JWT-based authentication for admin interface

### Frontend
- **Framework**: React.js with nodus.social aesthetics
- **UI Components**: Material-UI or Tailwind CSS
- **State Management**: React Context API or Redux
- **API Communication**: Axios for HTTP requests

### Deployment
- **Containerization**: Docker for consistent deployment
- **Hosting**: Cloud platform (AWS, GCP, or Azure)
- **CI/CD**: GitHub Actions for automated testing and deployment

## Data Models

### Email
```
{
  "id": "unique_id",
  "sender": "sender@example.com",
  "recipient": "inbox@smartinbox.com",
  "subject": "Email subject",
  "body": "Email body content",
  "attachments": ["list", "of", "attachments"],
  "received_at": "timestamp",
  "client_id": "identified_client_id",
  "classification": "technical|commercial|administrative",
  "confidence_score": 0.95,
  "routing_action": "github_issue|email_forward|manual_review",
  "status": "processed|pending|error"
}
```

### Client
```
{
  "id": "unique_id",
  "name": "Client Name",
  "domains": ["example.com", "example.org"],
  "signature_patterns": ["regex_pattern_1", "regex_pattern_2"],
  "authorized_emails": ["contact@example.com", "support@example.com"],
  "github_repository": "owner/repo",
  "technical_contact": "tech@internal.com",
  "commercial_contact": "sales@internal.com",
  "administrative_contact": "admin@internal.com"
}
```

### RoutingRule
```
{
  "id": "unique_id",
  "client_id": "client_id",
  "classification": "technical|commercial|administrative",
  "action": "github_issue|email_forward",
  "destination": "owner/repo or email@internal.com",
  "priority": 1,
  "active": true
}
```

### Log
```
{
  "id": "unique_id",
  "timestamp": "timestamp",
  "email_id": "email_id",
  "action": "client_identification|classification|routing|manual_review",
  "details": "Action details",
  "status": "success|failure",
  "error": "Error message if any"
}
```

## API Endpoints

### Email Management
- `POST /api/emails/receive` - Webhook for receiving emails
- `GET /api/emails` - List all emails with filtering options
- `GET /api/emails/{id}` - Get details of a specific email
- `PUT /api/emails/{id}/manual-review` - Update email after manual review

### Client Management
- `GET /api/clients` - List all clients
- `POST /api/clients` - Create a new client
- `GET /api/clients/{id}` - Get details of a specific client
- `PUT /api/clients/{id}` - Update client details
- `DELETE /api/clients/{id}` - Delete a client

### Routing Rules
- `GET /api/routing-rules` - List all routing rules
- `POST /api/routing-rules` - Create a new routing rule
- `GET /api/routing-rules/{id}` - Get details of a specific routing rule
- `PUT /api/routing-rules/{id}` - Update routing rule
- `DELETE /api/routing-rules/{id}` - Delete a routing rule

### System Management
- `GET /api/logs` - Get system logs with filtering options
- `GET /api/stats` - Get system statistics
- `POST /api/test-connection` - Test connections to email and GitHub APIs

## Security Considerations
- All API endpoints secured with JWT authentication
- HTTPS for all communications
- Secure storage of API keys and credentials
- Input validation to prevent injection attacks
- Rate limiting to prevent abuse

## Scalability Considerations
- Stateless design for horizontal scaling
- Asynchronous processing of emails
- Caching for frequently accessed data
- Database indexing for performance optimization
