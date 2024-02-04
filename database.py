from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root@localhost:3306/test"
engine = create_engine(DATABASE_URL)

# Declare a base for declarative class configurations
Base = declarative_base()

# Define SessionLocal using the scoped_session pattern
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)