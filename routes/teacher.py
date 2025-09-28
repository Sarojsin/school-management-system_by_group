from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import get_student_db, get_teacher_db, get_public_db
from models import Teacher, Student, StudentMarks, StudentAttendance, StudentAssignments
from repositories.student_repository import StudentRepository
from repositories.user_repository import UserRepository
from routes.auth import require_auth

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def teacher_dashboard(
    request: Request,
    teacher_db: Session = Depends(get_teacher_db),
    student_db: Session = Depends(get_student_db),
    public_db: Session = Depends(get_public_db)
):
    user_id = require_auth(request)
    
    # Get teacher data
    teacher = teacher_db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get all students
    student_repo = StudentRepository(student_db)
    students = student_repo.get_all_students()
    
    # Get recent uploads by this teacher
    recent_marks = student_db.query(StudentMarks).filter(
        StudentMarks.uploaded_by == user_id
    ).order_by(StudentMarks.created_at.desc()).limit(10).all()
    
    recent_attendance = student_db.query(StudentAttendance).filter(
        StudentAttendance.uploaded_by == user_id
    ).order_by(StudentAttendance.created_at.desc()).limit(10).all()
    
    # Get user info
    user_repo = UserRepository(public_db)
    user = user_repo.get_user_by_id(user_id)
    
    return templates.TemplateResponse("teacher_dashboard.html", {
        "request": request,
        "teacher": teacher,
        "user": user,
        "students": students,
        "recent_marks": recent_marks,
        "recent_attendance": recent_attendance
    })

@router.get("/students", response_class=HTMLResponse)
async def view_students(
    request: Request,
    teacher_db: Session = Depends(get_teacher_db),
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    students = student_repo.get_all_students()
    
    return templates.TemplateResponse("teacher_students.html", {
        "request": request,
        "students": students
    })

@router.get("/add-marks", response_class=HTMLResponse)
async def add_marks_form(
    request: Request,
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    students = student_repo.get_all_students()
    
    return templates.TemplateResponse("teacher_add_marks.html", {
        "request": request,
        "students": students
    })

@router.post("/add-marks")
async def add_marks(
    request: Request,
    student_id: int = Form(...),
    subject: str = Form(...),
    exam_type: str = Form(...),
    marks_obtained: float = Form(...),
    total_marks: float = Form(...),
    grade: str = Form(...),
    exam_date: str = Form(...),
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    marks_data = {
        "student_id": student_id,
        "subject": subject,
        "exam_type": exam_type,
        "marks_obtained": marks_obtained,
        "total_marks": total_marks,
        "grade": grade,
        "exam_date": datetime.strptime(exam_date, "%Y-%m-%d")
    }
    
    student_repo.create_marks(marks_data, user_id)
    
    return RedirectResponse(url="/teacher/dashboard?msg=Marks added successfully", status_code=303)

@router.get("/add-attendance", response_class=HTMLResponse)
async def add_attendance_form(
    request: Request,
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    students = student_repo.get_all_students()
    
    return templates.TemplateResponse("teacher_add_attendance.html", {
        "request": request,
        "students": students
    })

@router.post("/add-attendance")
async def add_attendance(
    request: Request,
    student_id: int = Form(...),
    date: str = Form(...),
    status: str = Form(...),
    subject: str = Form(...),
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    attendance_data = {
        "student_id": student_id,
        "date": datetime.strptime(date, "%Y-%m-%d"),
        "status": status,
        "subject": subject
    }
    
    student_repo.create_attendance(attendance_data, user_id)
    
    return RedirectResponse(url="/teacher/dashboard?msg=Attendance added successfully", status_code=303)

@router.get("/add-assignment", response_class=HTMLResponse)
async def add_assignment_form(
    request: Request,
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    students = student_repo.get_all_students()
    
    return templates.TemplateResponse("teacher_add_assignment.html", {
        "request": request,
        "students": students
    })

@router.post("/add-assignment")
async def add_assignment(
    request: Request,
    student_id: int = Form(...),
    assignment_title: str = Form(...),
    subject: str = Form(...),
    assignment_date: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...),
    student_db: Session = Depends(get_student_db)
):
    user_id = require_auth(request)
    
    student_repo = StudentRepository(student_db)
    assignment_data = {
        "student_id": student_id,
        "assignment_title": assignment_title,
        "subject": subject,
        "assignment_date": datetime.strptime(assignment_date, "%Y-%m-%d"),
        "due_date": datetime.strptime(due_date, "%Y-%m-%d"),
        "status": status
    }
    
    student_repo.create_assignment(assignment_data, user_id)
    
    return RedirectResponse(url="/teacher/dashboard?msg=Assignment added successfully", status_code=303)