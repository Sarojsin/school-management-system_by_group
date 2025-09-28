from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from database import get_authority_db, get_student_db, get_teacher_db, get_public_db
from models import Authority, SchoolNotices, FeeStructure, Student, Teacher
from repositories.user_repository import UserRepository
from routes.auth import require_auth

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def authority_dashboard(
    request: Request,
    authority_db: Session = Depends(get_authority_db),
    student_db: Session = Depends(get_student_db),
    teacher_db: Session = Depends(get_teacher_db),
    public_db: Session = Depends(get_public_db)
):
    user_id = require_auth(request)
    
    # Get authority data
    authority = authority_db.query(Authority).filter(Authority.user_id == user_id).first()
    if not authority:
        raise HTTPException(status_code=404, detail="Authority profile not found")
    
    # Get statistics
    total_students = student_db.query(Student).count()
    total_teachers = teacher_db.query(Teacher).count()
    active_notices = authority_db.query(SchoolNotices).filter(SchoolNotices.is_active == True).count()
    
    # Get recent notices
    recent_notices = authority_db.query(SchoolNotices).filter(
        SchoolNotices.created_by == user_id
    ).order_by(SchoolNotices.created_at.desc()).limit(5).all()
    
    # Get user info
    user_repo = UserRepository(public_db)
    user = user_repo.get_user_by_id(user_id)
    
    return templates.TemplateResponse("authority_dashboard.html", {
        "request": request,
        "authority": authority,
        "user": user,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "active_notices": active_notices,
        "recent_notices": recent_notices
    })

@router.get("/notices", response_class=HTMLResponse)
async def manage_notices(
    request: Request,
    authority_db: Session = Depends(get_authority_db)
):
    user_id = require_auth(request)
    
    notices = authority_db.query(SchoolNotices).order_by(SchoolNotices.created_at.desc()).all()
    
    return templates.TemplateResponse("authority_notices.html", {
        "request": request,
        "notices": notices
    })

@router.get("/add-notice", response_class=HTMLResponse)
async def add_notice_form(request: Request):
    user_id = require_auth(request)
    
    return templates.TemplateResponse("authority_add_notice.html", {
        "request": request
    })

@router.post("/add-notice")
async def add_notice(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    priority: str = Form(...),
    target_audience: str = Form(...),
    expires_at: Optional[str] = Form(None),
    authority_db: Session = Depends(get_authority_db)
):
    user_id = require_auth(request)
    
    expires_datetime = None
    if expires_at:
        expires_datetime = datetime.strptime(expires_at, "%Y-%m-%d")
    
    notice = SchoolNotices(
        title=title,
        content=content,
        priority=priority,
        target_audience=target_audience,
        expires_at=expires_datetime,
        created_by=user_id
    )
    
    authority_db.add(notice)
    authority_db.commit()
    
    return RedirectResponse(url="/authority/notices?msg=Notice added successfully", status_code=303)

@router.post("/toggle-notice/{notice_id}")
async def toggle_notice(
    notice_id: int,
    request: Request,
    authority_db: Session = Depends(get_authority_db)
):
    user_id = require_auth(request)
    
    notice = authority_db.query(SchoolNotices).filter(SchoolNotices.id == notice_id).first()
    if notice:
        notice.is_active = not notice.is_active
        authority_db.commit()
    
    return RedirectResponse(url="/authority/notices", status_code=303)

@router.get("/fee-structure", response_class=HTMLResponse)
async def manage_fee_structure(
    request: Request,
    authority_db: Session = Depends(get_authority_db)
):
    user_id = require_auth(request)
    
    fees = authority_db.query(FeeStructure).filter(FeeStructure.is_active == True).all()
    
    return templates.TemplateResponse("authority_fee_structure.html", {
        "request": request,
        "fees": fees
    })

@router.get("/add-fee", response_class=HTMLResponse)
async def add_fee_form(request: Request):
    user_id = require_auth(request)
    
    return templates.TemplateResponse("authority_add_fee.html", {
        "request": request
    })

@router.post("/add-fee")
async def add_fee(
    request: Request,
    grade: str = Form(...),
    fee_type: str = Form(...),
    amount: float = Form(...),
    academic_year: str = Form(...),
    authority_db: Session = Depends(get_authority_db)
):
    user_id = require_auth(request)
    
    fee = FeeStructure(
        grade=grade,
        fee_type=fee_type,
        amount=amount,
        academic_year=academic_year,
        created_by=user_id
    )
    
    authority_db.add(fee)
    authority_db.commit()
    
    return RedirectResponse(url="/authority/fee-structure?msg=Fee structure added successfully", status_code=303)

@router.get("/students", response_class=HTMLResponse)
async def view_all_students(
    request: Request,
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    students = student_db.query(Student).all()
    
    return templates.TemplateResponse("authority_students.html", {
        "request": request,
        "students": students
    })

@router.get("/teachers", response_class=HTMLResponse)
async def view_all_teachers(
    request: Request,
    teacher_db: Session = Depends(get_teacher_db)
):
    user_id = require_auth(request)
    
    teachers = teacher_db.query(Teacher).all()
    
    return templates.TemplateResponse("authority_teachers.html", {
        "request": request,
        "teachers": teachers
    })