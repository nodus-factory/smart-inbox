# Detailed Deployment Guide for Smart Inbox Application

This guide provides step-by-step instructions for deploying the Smart Inbox Application to your Hetzner server.

## 1. GitHub Repository Setup

### Creating a GitHub Organization
1. Go to GitHub and sign in to your account
2. Click on your profile picture in the top-right corner
3. Select "Your organizations"
4. Click "New organization"
5. Choose the free plan
6. Enter "nodus-factory" as the organization name
7. Complete the organization setup process

### Creating the Repository
1. Navigate to your new organization page (github.com/nodus-factory)
2. Click the "New" button to create a new repository
3. Name it "smart-inbox"
4. Choose visibility (public or private)
5. Click "Create repository"

### Pushing Code to GitHub
1. Extract the downloaded ZIP file to your local machine
2. Open a terminal and navigate to the extracted directory
3. Initialize Git and push to GitHub:
   ```bash
   cd smart_inbox
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/nodus-factory/smart-inbox.git
   git push -u origin main
   ```

## 2. Hetzner Server Deployment

### Prerequisites
- SSH access to your Hetzner server
- Docker and Docker Compose installed on the server
- Git installed on the server

### Deployment Steps

1. SSH into your Hetzner server:
   ```bash
   ssh username@your-server-ip
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/nodus-factory/smart-inbox.git
   cd smart-inbox
   ```

3. Create the environment file:
   ```bash
   cp .env.example .env
   nano .env
   ```

4. Edit the .env file with your actual credentials:
   ```
   ENVIRONMENT=production
   EMAIL_USERNAME=your_email@example.com
   EMAIL_PASSWORD=your_secure_password
   GITHUB_ACCESS_TOKEN=your_github_token
   OPENAI_API_KEY=your_openai_api_key
   DB_PASSWORD=your_secure_database_password
   ```
   Save and exit (Ctrl+X, then Y, then Enter)

5. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

6. Verify the application is running:
   ```bash
   docker-compose ps
   ```

7. Check the logs if needed:
   ```bash
   docker-compose logs -f
   ```

8. Access the application at `http://your-server-ip:8000`

## 3. Configuration and Maintenance

### Updating the Application
When you make changes to the code:

1. Push changes to GitHub
2. On your Hetzner server:
   ```bash
   cd smart-inbox
   git pull
   docker-compose down
   docker-compose up -d --build
   ```

### Database Backup
To backup the PostgreSQL database:

```bash
docker-compose exec db pg_dump -U postgres smart_inbox > backup.sql
```

### Troubleshooting

#### Application Not Starting
Check the logs:
```bash
docker-compose logs app
```

#### Database Connection Issues
Verify the database is running:
```bash
docker-compose ps db
```

Check database logs:
```bash
docker-compose logs db
```

#### Email Reception Issues
Verify your email credentials in the .env file and check the logs:
```bash
docker-compose logs app
```

## 4. Security Considerations

- The .env file contains sensitive information. Ensure it has restricted permissions:
  ```bash
  chmod 600 .env
  ```

- Consider setting up HTTPS with a reverse proxy like Nginx and Let's Encrypt

- Regularly update the application and dependencies:
  ```bash
  git pull
  docker-compose build --no-cache
  docker-compose down
  docker-compose up -d
  ```

## 5. Support

If you encounter any issues during deployment or operation, please refer to the documentation or contact the development team for assistance.
