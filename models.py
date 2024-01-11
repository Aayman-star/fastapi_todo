from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    description: str
    is_complete:bool = False
