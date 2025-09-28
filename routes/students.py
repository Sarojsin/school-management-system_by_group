from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from database import get_student_db, get_authority_db, get_public_db
from models import SchoolNotices
from repositories.student_repository import StudentRepository
from repositories.user_repository import UserRepository
from routes.auth import require_auth

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def student_dashboard(
    request: Request,
    student_db: Session = Depends(get_student_db),
    authority_db: Session = Depends(get_authority_db),
    public_db: Session = Depends(get_public_db)
):
    user_id = require_auth(request)
    
    # Get student data
    student_repo = StudentRepository(student_db)
    student = student_repo.get_student_by_user_id(user_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Get student performance data
    marks = student_repo.get_student_marks(student.id)
    attendance = student_repo.get_student_attendance(student.id)
    assignments = student_repo.get_student_assignments(student.id)
    
    # Get notices from authority database
    notices = authority_db.query(SchoolNotices).filter(
        SchoolNotices.is_active == True,
        SchoolNotices.target_audience.in_(["all", "students"])
    ).order_by(SchoolNotices.created_at.desc()).limit(10).all()
    
    # Get user info
    user_repo = UserRepository(public_db)
    user = user_repo.get_user_by_id(user_id)
    
    return templates.TemplateResponse("student_dashboard.html", {
        "request": request,
        "student": student,
        "user": user,
        "marks": marks,
        "attendance": attendance,
        "assignments": assignments,
        "notices": notices
    })

@router.get("/profile", response_class=HTMLResponse)
async def student_profile(
    request: Request,
    student_db: Session = Depends(get_student_db),
    public_db: Session = Depends(get_public_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    student = student_repo.get_student_by_user_id(user_id)
    
    user_repo = UserRepository(public_db)
    user = user_repo.get_user_by_id(user_id)
    
    return templates.TemplateResponse("student_profile.html", {
        "request": request,
        "student": student,
        "user": user
    })

@router.post("/profile/update")
async def update_student_profile(
    request: Request,
    grade: str = Form(...),
    section: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    guardian_name: str = Form(...),
    guardian_phone: str = Form(...),
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    student = student_repo.get_student_by_user_id(user_id)
    
    if student:
        student.grade = grade
        student.section = section
        student.phone = phone
        student.address = address
        student.guardian_name = guardian_name
        student.guardian_phone = guardian_phone
        
        student_db.commit()
    
    return RedirectResponse(url="/student/profile?msg=Profile updated successfully", status_code=303)