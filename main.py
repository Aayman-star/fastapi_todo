from fastapi import FastAPI
from models import Todo


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
    """Get a Todo"""
    for todo in todos:
        if todo.id == todo_id:
            return {"Todo": todo}
    return {"message": "Todo not found"}

@app.post("/todos")
def create_todo(todo: Todo):
    """Create a Todo"""
    todos.append(todo)
    return {"message": "Todo created successfully"}

@app.post("/todos/{todo_id}")
def update_todo_description(todo_id: int, description:str,is_complete:bool):
    """Update Todo Description"""
    for todo in todos:
        if todo.id == todo_id:
            todo.description = description
            todo.is_complete = is_complete
            return {"message": "Todo successfully updated"}
            
    return {"message": "Todo not updated"} 

@app.post("/todos/{todo_id}")
def update_todo_status(todo_id: int,is_complete:bool):
    """Update Todo Status"""
    for todo in todos:
        if todo.id == todo_id:
            todo.is_complete = is_complete
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


