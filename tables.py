from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Auth schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Student schemas
class StudentCreate(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    grade: str
    section: str
    phone: str
    address: str
    guardian_name: str
    guardian_phone: str

class StudentMarksCreate(BaseModel):
    student_id: int
    subject: str
    exam_type: str
    marks_obtained: float
    total_marks: float
    grade: str
    exam_date: datetime

class StudentAttendanceCreate(BaseModel):
    student_id: int
    date: datetime
    status: str
    subject: str

class StudentAssignmentCreate(BaseModel):
    student_id: int
    assignment_title: str
    subject: str
    assignment_date: datetime
    due_date: datetime
    status: str
    marks: Optional[float] = None

# Teacher schemas
class TeacherCreate(BaseModel):
    teacher_id: str
    first_name: str
    last_name: str
    subjects: str
    phone: str
    qualification: str
    experience_years: int

class TeacherSubjectCreate(BaseModel):
    teacher_id: int
    subject_name: str
    grade: str
    section: str

# Authority schemas
class AuthorityCreate(BaseModel):
    first_name: str
    last_name: str
    position: str
    phone: str

class NoticeCreate(BaseModel):
    title: str
    content: str
    priority: str
    target_audience: str
    expires_at: Optional[datetime] = None

class FeeStructureCreate(BaseModel):
    grade: str
    fee_type: str
    amount: float
    academic_year: str

# Response schemas
class StudentResponse(BaseModel):
    id: int
    student_id: str
    first_name: str
    last_name: str
    grade: str
    section: str

    class Config:
        from_attributes = True

class TeacherResponse(BaseModel):
    id: int
    teacher_id: str
    first_name: str
    last_name: str
    subjects: str

    class Config:
        from_attributes = True

class NoticeResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True