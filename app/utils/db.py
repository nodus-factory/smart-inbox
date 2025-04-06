"""
Database utilities for Smart Inbox Application
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from app.config.settings import DATABASE

# Determine environment
env = os.getenv("ENVIRONMENT", "development")
db_config = DATABASE[env]

# Create database URL
if db_config["engine"] == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_config['name']}"
elif db_config["engine"] == "postgresql":
    password = os.getenv("DB_PASSWORD", db_config.get("password", ""))
    SQLALCHEMY_DATABASE_URL = f"postgresql://{db_config['user']}:{password}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
else:
    raise ValueError(f"Unsupported database engine: {db_config['engine']}")

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if db_config["engine"] == "sqlite" else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
