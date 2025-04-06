# Smart Inbox Application

Smart Inbox is an AI-assisted email routing system designed to serve as a single point of contact for client communications. The system automatically identifies clients, classifies emails using AI, and routes them to appropriate destinations based on configurable rules.

## Features

- **Email Reception**: Receive emails via IMAP/SMTP or Gmail API
- **Client Identification**: Identify clients by email domain, signature patterns, and authorized emails
- **AI Classification**: Classify emails into technical, commercial, or administrative categories
- **Automated Routing**:
  - Create GitHub issues for technical queries
  - Forward emails to appropriate internal contacts
- **No-Code Interface**: Configure routing rules without coding
- **Manual Review**: Review and route emails when AI confidence is low
- **Comprehensive Logging**: Track all system actions for debugging and auditing

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React.js with nodus.social aesthetics
- **Database**: PostgreSQL (production) / SQLite (development)
- **AI**: OpenAI API with fallback to custom classifier
- **Integrations**: Gmail API, GitHub API

## Installation

### Prerequisites

- Python 3.10+
- Node.js 14+
- Docker and Docker Compose (for production deployment)

### Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/quirze62/Nodus.git
   cd Nodus
   ```

2. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env file with your credentials
   ```

4. Initialize the database:
   ```
   python -m app.main
   ```

5. Start the development server:
   ```
   uvicorn app.main:app --reload
   ```

### Production Deployment

1. Clone the repository on your Hetzner server:
   ```
   git clone https://github.com/quirze62/Nodus.git
   cd Nodus
   ```

2. Create a `.env` file with your production credentials:
   ```
   ENVIRONMENT=production
   EMAIL_USERNAME=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   GITHUB_ACCESS_TOKEN=your_github_token
   OPENAI_API_KEY=your_openai_api_key
   DB_PASSWORD=your_database_password
   ```

3. Start the application with Docker Compose:
   ```
   docker-compose up -d
   ```

4. Access the application at `http://your-server-ip:8000`

## Configuration

### Email Settings

Configure email settings in `app/config/settings.py`:
- IMAP/SMTP server details
- Gmail API credentials
- Central inbox address

### GitHub Integration

Configure GitHub settings in `app/config/settings.py`:
- Default repository
- Issue labels

### AI Classification

Configure AI settings in `app/config/settings.py`:
- OpenAI API model
- Confidence threshold for manual review

## Usage

### Admin Interface

Access the admin interface at `/admin` to:
- Manage clients
- Configure routing rules
- Review emails flagged for manual review
- View system logs

### API Endpoints

- `/api/emails`: Manage emails
- `/api/clients`: Manage clients
- `/api/routing-rules`: Configure routing rules
- `/api/system`: System management and logs

## License

This project is proprietary and confidential.

## Support

For support, please contact the development team.
