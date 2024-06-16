# app/database.py
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os
load_dotenv(find_dotenv())
# Retrieve database credentials from environment variables or configuration
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
hostname = os.getenv("DB_HOSTNAME")
database_name = os.getenv("DB_NAME")

# Debugging: Print the values to ensure they are loaded correctly (remove this in production)
print(f"DB_USERNAME: {username}")
print(f"DB_PASSWORD: {password}")
print(f"DB_HOSTNAME: {hostname}")
print(f"DB_NAME: {database_name}")

# Ensure password is a string before encoding it
if not isinstance(password, str):
    password = str(password)

# Encode the password to make it safe for use in a URL
encoded_password = quote_plus(password)

# Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{encoded_password}@{hostname}/{database_name}"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
