import os
from dotenv import load_dotenv,find_dotenv
from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal,UserList
from models import UsersModel,Token
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm   
from jose import JWTError, jwt



load_dotenv(find_dotenv())
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
#print(JWT_SECRET_KEY)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]	
)
ALGORITHM = os.environ["ALGORITHM"]

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer =  OAuth2PasswordBearer(tokenUrl="auth/token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_model: UsersModel):
    """Create a new user"""
    user_model = UserList(username=user_model.username,useremail=user_model.useremail, hashed_password=password_context.hash(user_model.password))
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm , Depends()], db: db_dependency):
    """ this is where we send the acquired user data to be authenticated"""
    auth_user = authenticate_user(form_data.username,form_data.password, db)    
    print(auth_user)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
           )
    token = create_access_token(auth_user.username, auth_user.id,timedelta(minutes=20))
    if token:
        return{"access_token":token,"token_type":"bearer"}
    else:
        return "something is wrong"


def authenticate_user(username: str, password: str, db):
    user = db.query(UserList).filter(UserList.username == username).first()
    print(user)
    if not user:
        return False
    if not password_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """This is where the jwt token in being created"""
    encode = {"sub": username, "id": user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """This is where we access the information about the current user"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="could not validate the user")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="could not validate the user")
