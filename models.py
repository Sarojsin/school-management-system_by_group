from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# PUBLIC DATABASE MODELS
class PublicUser(Base):
    __tablename__ = "public_users"
    __table_args__ = {'schema': 'public'}
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # student, teacher, authority
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# STUDENT DATABASE MODELS
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)  # Reference to PublicUser
    student_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    grade = Column(String)
    section = Column(String)
    phone = Column(String)
    address = Column(Text)
    guardian_name = Column(String)
    guardian_phone = Column(String)
    created_at = Column(DateTime, default=datetime.timezone.utcnow)

class StudentMarks(Base):
    __tablename__ = "student_marks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    exam_type = Column(String)  # midterm, final, quiz
    marks_obtained = Column(Float)
    total_marks = Column(Float)
    grade = Column(String)
    exam_date = Column(DateTime)
    uploaded_by = Column(Integer)  # Teacher user_id
    created_at = Column(DateTime, default=datetime.timezone.utcnow)

class StudentAttendance(Base):
    __tablename__ = "student_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime)
    status = Column(String)  # present, absent, late
    subject = Column(String)
    uploaded_by = Column(Integer)  # Teacher user_id
    created_at = Column(DateTime, default=datetime.timezone.utcnow)

class StudentAssignments(Base):
    __tablename__ = "student_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    assignment_title = Column(String)
    subject = Column(String)
    assignment_date = Column(DateTime)
    due_date = Column(DateTime)
    status = Column(String)  # submitted, pending, overdue
    marks = Column(Float, nullable=True)
    uploaded_by = Column(Integer)  # Teacher user_id
    created_at = Column(DateTime, default=datetime.timezone.utcnow)

# TEACHER DATABASE MODELS
class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)  # Reference to PublicUser
    teacher_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    subjects = Column(String)  # JSON string of subjects
    phone = Column(String)
    qualification = Column(String)
    experience_years = Column(Integer)
    created_at = Column(DateTime, default=datetime.timezone.utcnow)

class TeacherSubjects(Base):
    __tablename__ = "teacher_subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject_name = Column(String)
    grade = Column(String)
    section = Column(String)

# AUTHORITY DATABASE MODELS
class Authority(Base):
    __tablename__ = "authorities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)  # Reference to PublicUser
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)  # Principal, Vice Principal, Admin
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.timezone.utcnow)

class SchoolNotices(Base):
    __tablename__ = "school_notices"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    priority = Column(String)  # high, medium, low
    target_audience = Column(String)  # all, students, teachers
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer)  # Authority user_id
    created_at = Column(DateTime, default=datetime.timezone.utcnow)
    expires_at = Column(DateTime, nullable=True)

class FeeStructure(Base):
    __tablename__ = "fee_structure"
    
    id = Column(Integer, primary_key=True, index=True)
    grade = Column(String)
    fee_type = Column(String)  # tuition, transport, activity, etc
    amount = Column(Float)
    academic_year = Column(String)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer)  # Authority user_id
    created_at = Column(DateTime, default=datetime.timezone.utcnow)