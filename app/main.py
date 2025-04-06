"""
Main application entry point for the Smart Inbox Application
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.settings import API, DATABASE, LOGGING

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING["level"]),
    format=LOGGING["format"],
    filename=LOGGING["file"]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Inbox API",
    description="API for Smart Inbox Application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def get_db_url():
    """Get database URL based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    db_config = DATABASE[env]
    
    if db_config["engine"] == "sqlite":
        return f"sqlite:///{db_config['name']}"
    elif db_config["engine"] == "postgresql":
        password = os.getenv("DB_PASSWORD", db_config.get("password", ""))
        return f"postgresql://{db_config['user']}:{password}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
    else:
        raise ValueError(f"Unsupported database engine: {db_config['engine']}")

# Create database engine and session
engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import and include routers
# These imports are placed here to avoid circular imports
from app.backend.routes import email_routes, client_routes, routing_rules_routes, system_routes

app.include_router(email_routes.router, prefix=API["prefix"])
app.include_router(client_routes.router, prefix=API["prefix"])
app.include_router(routing_rules_routes.router, prefix=API["prefix"])
app.include_router(system_routes.router, prefix=API["prefix"])

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"status": "ok", "message": "Smart Inbox API is running"}

def start():
    """Start the application server"""
    import uvicorn
    logger.info(f"Starting Smart Inbox API on {API['host']}:{API['port']}")
    uvicorn.run(app, host=API["host"], port=API["port"])

if __name__ == "__main__":
    start()
