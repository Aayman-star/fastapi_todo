from pydantic import BaseModel

class Todo(BaseModel):
    description: str
    is_complete:bool = False
