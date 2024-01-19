from typing import Annotated
from fastapi import FastAPI,HTTPException,Body,Query,Path,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Todo
from database import SessionLocal,engine,Todo as Td
from enum import Enum
import auth
from auth import get_current_user
from starlette import status

# class Status(Enum):
#     complete = "complete"
#     incomplete = "incomplete"

app :FastAPI = FastAPI();
#Inclding the router from the auth file
app.include_router(auth.router)

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""#??As long as the api is not connected with the database"""
todos : list[Todo] = []

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/user",status_code = status.HTTP_200_OK)
async def get_user(user:user_dependency,db:Session = Depends(get_db)):
    """This is to get the current user"""
    if user is None:
        raise HTTPException(status_code=404, detail="No user found")
    return {"User":user}
@app.get("/")
async def read_todos(db: Session = Depends(get_db)):
    """Get all Todos"""
    todos_query = db.query(Td).order_by(Td.id)
    if todos_query.first() is None:
        raise HTTPException(status_code=404, detail="No todos found")
    return todos_query.all()
   

@app.get("/todo/{todo_id}")
def get_todo(todo_id: int,db:Session=Depends(get_db)):
    """Get a single Todo by id"""
    todo = db.query(Td).filter(Td.id==todo_id).first()
    return todo


@app.get("/complete-todos")
def get_completed_todos(db:Session=Depends(get_db)):
    """Get all completed Todos"""
    todos_query = db.query(Td).order_by(Td.id)
    done_todos_query = todos_query.filter(Td.is_complete==True)
    if done_todos_query.first() is None:
        raise HTTPException(status_code=404, detail="No completed todos found")
    return done_todos_query.all()
 	

@app.get("/incomplete-todos")
def get_incomplete_todos(db:Session=Depends(get_db)):
    """Get all incomplete Todos"""
    todos_query = db.query(Td).order_by(Td.id)
    undone_todos_query = todos_query.filter(Td.is_complete==False)
    if undone_todos_query.first() is None:
        raise HTTPException(status_code=404, detail="No incomplete todos found")
    return undone_todos_query.all()
 

@app.post("/create-todo")
async def create_todo(todo: Todo=Body(embed=True),db: Session = Depends(get_db)):
    """Create a Todo"""
    todo = Td(description=todo.description,is_complete=todo.is_complete)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put("/update-text")
def update_todo_description(todo_id: int, text:str,db:Session=Depends(get_db)):
    """Update Todo Description"""
    todo = db.query(Td).filter(Td.id==todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.description = text
    db.commit()
    db.refresh(todo)
    return todo
 

@app.put("/update-status")
def update_todo_status(todo_id: int,db:Session=Depends(get_db)):
    """Update Todo Status"""
    todo = db.query(Td).filter(Td.id==todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.is_complete = not todo.is_complete
    db.commit()
    db.refresh(todo)
    return todo




@app.delete("/delete/{todo_id}")
async def delete_todo(todo_id: int,db: Session = Depends(get_db)):
    """Delete a Todo"""
    db_todo = db.query(Td).filter(Td.id==todo_id).first() # Todo object
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"todo deleted": db_todo.description}
  
            
    

# @app.delete("/delete-all")
# def delete_all_todos(db:Session=Depends(get_db)):
#     """Delete all Todos"""
      #db.query(Td).delete()
#     todos = db.query(Td)
#     db.delete(todos.all())
#     db.commit()
    
#     return {"message": "All Todos deleted"}


if __name__ == "__main__": 
    import uvicorn
    uvicorn.run("main:app", reload=True)
