from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Encode the password to handle special characters properly
password = "Janaki@1"
encoded_password = quote_plus(password)

# Construct the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost/pii_analyzer"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()