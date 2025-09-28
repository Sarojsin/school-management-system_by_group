from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from starlette.middleware.sessions import SessionMiddleware

from database import get_public_db, get_student_db, get_teacher_db, get_authority_db
from models import Teacher, Student, Authority
from repositories.user_repository import UserRepository
from tables import UserCreate, UserLogin, Token
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(request: Request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return user_id

def require_auth(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user_id

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user_id = get_current_user(request)
    return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    public_db: Session = Depends(get_public_db),
    student_db: Session = Depends(get_student_db),
    teacher_db: Session = Depends(get_teacher_db),
    authority_db: Session = Depends(get_authority_db)
):
    user_repo = UserRepository(public_db)
    
    # Check if user exists
    if user_repo.get_user_by_username(username):
        return templates.TemplateResponse("signup.html", {
            "request": request, 
            "error": "Username already exists"
        })
    
    # Create user in public database
    user = user_repo.create_user(username, email, password, role)
    
    # Create role-specific entry
    if role == "student":
        student = Student(
            user_id=user.id,
            student_id=f"STU{user.id:04d}",
            first_name=first_name,
            last_name=last_name,
            grade="",  # To be filled later
            section="",
            phone=phone,
            address="",
            guardian_name="",
            guardian_phone=""
        )
        student_db.add(student)
        student_db.commit()
    elif role == "teacher":
        teacher = Teacher(
            user_id=user.id,
            teacher_id=f"TCH{user.id:04d}",
            first_name=first_name,
            last_name=last_name,
            subjects="",
            phone=phone,
            qualification="",
            experience_years=0
        )
        teacher_db.add(teacher)
        teacher_db.commit()
    elif role == "authority":
        authority = Authority(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            position="Staff",
            phone=phone
        )
        authority_db.add(authority)
        authority_db.commit()
    
    return RedirectResponse(url="/login?msg=Registration successful", status_code=303)

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    public_db: Session = Depends(get_public_db)
):
    user_repo = UserRepository(public_db)
    user = user_repo.authenticate_user(username, password)
    
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid credentials"
        })
    
    # Set session
    request.session['user_id'] = user.id
    request.session['username'] = user.username
    request.session['role'] = user.role
    
    # Redirect based on role
    if user.role == "student":
        return RedirectResponse(url="/student/dashboard", status_code=303)
    elif user.role == "teacher":
        return RedirectResponse(url="/teacher/dashboard", status_code=303)
    elif user.role == "authority":
        return RedirectResponse(url="/authority/dashboard", status_code=303)
    else:
        return RedirectResponse(url="/", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)