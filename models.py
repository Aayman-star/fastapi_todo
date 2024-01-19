from pydantic import BaseModel

class Todo(BaseModel):
    description: str
    is_complete:bool = False

class UsersModel(BaseModel):
    username: str
    useremail: str 
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str
