from sqlalchemy.orm import Session
from models import Student, StudentMarks, StudentAttendance, StudentAssignments
from typing import List

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_student(self, user_id: int, student_data: dict) -> Student:
        student = Student(user_id=user_id, **student_data)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_student_by_user_id(self, user_id: int) -> Student:
        return self.db.query(Student).filter(Student.user_id == user_id).first()

    def get_student_by_id(self, student_id: int) -> Student:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_all_students(self) -> List[Student]:
        return self.db.query(Student).all()

    def get_student_marks(self, student_id: int) -> List[StudentMarks]:
        return self.db.query(StudentMarks).filter(StudentMarks.student_id == student_id).all()

    def get_student_attendance(self, student_id: int) -> List[StudentAttendance]:
        return self.db.query(StudentAttendance).filter(StudentAttendance.student_id == student_id).all()

    def get_student_assignments(self, student_id: int) -> List[StudentAssignments]:
        return self.db.query(StudentAssignments).filter(StudentAssignments.student_id == student_id).all()

    def create_marks(self, marks_data: dict, teacher_user_id: int) -> StudentMarks:
        marks = StudentMarks(**marks_data, uploaded_by=teacher_user_id)
        self.db.add(marks)
        self.db.commit()
        self.db.refresh(marks)
        return marks

    def create_attendance(self, attendance_data: dict, teacher_user_id: int) -> StudentAttendance:
        attendance = StudentAttendance(**attendance_data, uploaded_by=teacher_user_id)
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def create_assignment(self, assignment_data: dict, teacher_user_id: int) -> StudentAssignments:
        assignment = StudentAssignments(**assignment_data, uploaded_by=teacher_user_id)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment