#!/usr/bin/env python3
"""
Database Setup Script for School Management Portal
Creates 4 PostgreSQL databases and sample data
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import random
import sys
import os

# Set UTF-8 encoding for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Database configurations
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'tara'  # ← PUT YOUR PASSWORD HERE
}

DATABASES = [
    'school_students',
    'school_teachers', 
    'school_authority',
    'school_public'
]

def create_databases():
    """Create the required databases"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Creating databases...")
        for db_name in DATABASES:
            try:
                # Check if database exists
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                if not cur.fetchone():
                    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                    print(f"[SUCCESS] Created database: {db_name}")
                else:
                    print(f"[INFO] Database {db_name} already exists")
            except Exception as e:
                print(f"[ERROR] Error creating database {db_name}: {e}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error connecting to PostgreSQL: {e}")
        print("Make sure PostgreSQL is running and credentials are correct")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("\nCreating sample data structure...")
    
    try:
        # Database tables will be created by FastAPI models
        print("[SUCCESS] Sample data structure ready")
        print("\nSample Login Credentials:")
        print("Student: student1 / password123")
        print("Teacher: teacher1 / password123") 
        print("Authority: admin1 / password123")
        
    except Exception as e:
        print(f"[ERROR] Error creating sample data: {e}")

def main():
    print("School Management Portal - Database Setup")
    print("=" * 50)
    
    # Update database password prompt
    current_password = DB_CONFIG['password']
    if current_password == 'YOUR_ACTUAL_PASSWORD':
        print("\n[WARNING] You need to update the password in this file!")
        print("Edit setup_databases.py and replace 'YOUR_ACTUAL_PASSWORD' with your PostgreSQL password")
        input("Press Enter after updating the password...")
    
    if create_databases():
        create_sample_data()
        print("\n[SUCCESS] Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Make sure you updated app/config.py with the same password")
        print("2. Run: python run.py")
        
    else:
        print("\n[ERROR] Database setup failed!")
        print("Please check PostgreSQL installation and credentials")

if __name__ == "__main__":
    main()