from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_CONFIGS

# Create engines for each database
engines = {}
SessionLocals = {}
metadata = {}

for db_name, db_url in DATABASE_CONFIGS.items():
    engines[db_name] = create_engine(db_url)
    SessionLocals[db_name] = sessionmaker(autocommit=False, autoflush=False, bind=engines[db_name])
    metadata[db_name] = MetaData()

# Base classes for each database
Base = declarative_base()

# Dependency functions for each database
def get_student_db():
    db = SessionLocals["student"]()
    try:
        yield db
    finally:
        db.close()

def get_teacher_db():
    db = SessionLocals["teacher"]()
    try:
        yield db
    finally:
        db.close()

def get_authority_db():
    db = SessionLocals["authority"]()
    try:
        yield db
    finally:
        db.close()

def get_public_db():
    db = SessionLocals["public"]()
    try:
        yield db
    finally:
        db.close()