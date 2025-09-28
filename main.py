from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine

from config import SECRET_KEY, DATABASE_CONFIGS
from database import Base, engines
from routes import auth, students, teacher, authority

# Initialize FastAPI app
app = FastAPI(title="School Management Portal", version="1.0.0")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Create database tables
def create_tables():
    for db_name, engine in engines.items():
        Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(students.router, prefix="/student", tags=["students"])
app.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
app.include_router(authority.router, prefix="/authority", tags=["authority"])


@app.on_event("startup")
#@app.lifespan("startup")
async def startup_event():
    create_tables()
    print("✅ Database tables created successfully")
    print("🚀 School Management Portal is running!")
    print("📚 Access the portal at: http://localhost:8000")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware

# from config import SECRET_KEY, DATABASE_CONFIGS
# from database import Base, engines
# from routes import auth, students, teacher, authority

# # Initialize FastAPI app
# app = FastAPI(title="School Management Portal", version="1.0.0")

# # Add middlewares
# app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Create database tables
# def create_tables():
#     for db_name, engine in engines.items():
#         Base.metadata.create_all(bind=engine)
#     print("✅ Database tables created successfully")

# # Include routers
# app.include_router(auth.router, tags=["auth"])
# app.include_router(students.router, prefix="/student", tags=["students"])
# app.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
# app.include_router(authority.router, prefix="/authority", tags=["authority"])

# # Startup
# create_tables()
# print("🚀 School Management Portal is running!")

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
