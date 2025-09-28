from sqlalchemy.orm import Session
from models import PublicUser
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password: str, role: str) -> PublicUser:
        hashed_password = pwd_context.hash(password)
        user = PublicUser(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> PublicUser:
        return self.db.query(PublicUser).filter(PublicUser.username == username).first()

    def get_user_by_id(self, user_id: int) -> PublicUser:
        return self.db.query(PublicUser).filter(PublicUser.id == user_id).first()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> PublicUser:
        user = self.get_user_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return False
        return user