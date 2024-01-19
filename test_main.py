from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from typing import List
from main import app,get_db
from models import Todo
from database import SessionLocal,engine,Todo as Td


client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    # create a test database
    Td.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    # drop the test database
    Td.metadata.drop_all(bind=engine)

"""This file contains tests for all api routes"""


def test_read_todos(db):
    db.add(Td(description="Buy groceries", is_complete=False))
    db.add(Td(description="Do laundry", is_complete=True))
    db.commit()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "description": "Buy groceries", "is_complete": False},
        {"id": 2, "description": "Do laundry", "is_complete": True}
    ]
    # delete the test data
    db.query(Td)
    db.commit()
    # response = client.get("/")
    # assert response.status_code == 200
    # assert response.json() == List[Td]


# def test_get_todo():
#     response = client.get("/todos/1")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Todo not found"}

# def test_get_completed_todos():
#     response = client.get("/todos/completed")
#     assert response.status_code == 200
#     assert response.json() == []

# def test_get_incomplete_todos():
#     response = client.get("/todos/incomplete")
#     assert response.status_code == 200
#     assert response.json() == []

# def test_create_todo(): 
#     response = client.post("/todos", json={"title": "Test Todo", "description": "This is a test todo", "completed": False})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "title": "Test Todo", "description": "This is a test todo", "completed": False}

# def test_update_todo_status():
#     response = client.put("/todos/1", json={"completed": True})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "title": "Test Todo", "description": "This is a test todo", "completed": True}

# def test_update_todo_description():
#     response = client.put("/todos/1", json={"description": "This is the updated test todo"})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "title": "Test Todo", "description": "This is the updated test todo", "completed": True}

# def test_delete_todo(): 
#     response = client.delete("/todos/1")
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "title": "Test Todo", "description": "This is the updated test todo", "completed": True}
