import os
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone # Import timezone
from typing import Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session # Import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import User, get_db, engine, Base, SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException( # Define credentials_exception
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- User CRUD Operations ---
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, password: str, email: str = None):
    hashed_password = hash_password(password)
    db_user = User(username=username, hashed_password=hashed_password, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta # Use timezone-aware datetime
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Use timezone-aware datetime
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# --- FastAPI Security Dependencies ---
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    username = verify_token(token)
    return username