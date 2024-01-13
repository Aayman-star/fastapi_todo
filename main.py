from fastapi import FastAPI,Body,Query,Path
from models import Todo
from enum import Enum

class Status(Enum):
    complete = "complete"
    incomplete = "incomplete"

app :FastAPI = FastAPI();

"""#??As long as the api is not connected with the database"""
todos : list[Todo] = []

@app.get("/")
def get_todos():
    """Get all Todos"""
    if len(todos):
        return {"Todos": todos}
    return {"message": "No todos found"}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    """Get a single Todo by id"""
    for todo in todos:
        if todo.id == todo_id:
            return {"Todo": todo}
    return {"message": "Todo not found"}

@app.get("/todos/status_complete/{status}")
def get_completed_todos(status:Status=Path(...,description="The status of todos to filter by")):
    """Get all completed Todos"""
    completed_todos: list[Todo] = []
    for todo in todos:
        if status ==Status.complete and todo.is_complete:
            completed_todos.append(todo)
    if len(completed_todos):
        return {"Todos": completed_todos}
    return {"message": "No completed todos found"}	

@app.get("/todos/status_incomplete/{status}")
def get_incomplete_todos(status:Status=Path(...,description="The status of todos to filter by")):
    """Get all incomplete Todos"""
    incomplete_todos:list[Todo] = []
    for todo in todos:
        if status == Status.incomplete and not todo.is_complete:
            incomplete_todos.append(todo)
    if len(incomplete_todos):
        return {"Todos": incomplete_todos}
    return {"message": "No incomplete todos found"}

@app.post("/todos")
def create_todo(todo: Todo=Body(embed=True)):
    """Create a Todo"""
    todos.append(todo)
    return {"message": "Todo created successfully"}

@app.put("/todos/update")
def update_todo_description(todo_id: int, description:str):
    """Update Todo Description"""
    for todo in todos:
        if todo.id == todo_id:
            todo.description = description
            return {"message": "Todo successfully updated"}
    return {"message": "Todo not updated"} 

@app.put("/todos/check")
def update_todo_status(todo_id: int):
    """Update Todo Status"""
    for todo in todos:
        if todo.id == todo_id:
            todo.is_complete = not todo.is_complete
            return {"message": "Todo successfully updated"}
            
    return {"message": "Todo not updated"}



@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a Todo"""
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            
    return {"message": "ToDo deleted"}

@app.delete("/todos")
def delete_all_todos():
    """Delete all Todos"""
    todos.clear()
    
    return {"message": "All Todos deleted"}


if __name__ == "__main__": 
    import uvicorn
    uvicorn.run("main:app", reload=True)
