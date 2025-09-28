#!/usr/bin/env python3
"""
School Management Portal - Startup Script
Handles database initialization and starts the FastAPI server
"""

import os
import sys
import subprocess
import time

# Set UTF-8 encoding for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def check_postgresql():
    """Check if PostgreSQL is accessible"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            user="postgres",
            password="tara",  # ← PUT YOUR PASSWORD HERE
            database="postgres"
        )
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] PostgreSQL connection failed: {e}")
        return False

def setup_databases():
    """Run database setup script"""
    print("Setting up databases...")
    try:
        result = subprocess.run([sys.executable, "setup_databases.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Database setup completed")
            return True
        else:
            print(f"[ERROR] Database setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error running database setup: {e}")
        return False

def install_requirements():
    """Install Python requirements"""
    print("Installing requirements...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Requirements installed successfully")
            return True
        else:
            print(f"[ERROR] Failed to install requirements: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error installing requirements: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("Starting School Management Portal...")
    print("Server will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        os.chdir("app")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"[ERROR] Error starting server: {e}")

def main():
    print("School Management Portal - Startup")
    print("=" * 50)
    
    # Step 1: Check PostgreSQL
    if not check_postgresql():
        print("\n[ERROR] Setup failed!")
        print("Please ensure PostgreSQL is installed and running")
        print("Update the password in this script and setup_databases.py")
        input("Press Enter to exit...")
        return
    
    # Step 2: Install requirements
    if not install_requirements():
        print("\n[ERROR] Setup failed!")
        input("Press Enter to exit...")
        return
    
    # Step 3: Setup databases
    if not setup_databases():
        print("\n[ERROR] Setup failed!")
        input("Press Enter to exit...")
        return
    
    print("\n[SUCCESS] All systems ready!")
    print("\nDemo Login Credentials:")
    print("Student: student1 / password123")
    print("Teacher: teacher1 / password123")
    print("Authority: admin1 / password123")
    
    # Step 4: Start server
    time.sleep(2)
    start_server()

if __name__ == "__main__":
    main()