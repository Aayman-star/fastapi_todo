import requests
BASE_URL = "http://127.0.0.1:8000"
# data = {
#   "todo": {
#     "description": "Buy groceries",
#     "is_complete": False
#   }
# }
# response =  requests.post(f"{BASE_URL}/create-todo", json=data)
# print(response.status_code)
# print(response.json())
todo_id = 9
text ="text has been altered"

# response =  requests.put(f"{BASE_URL}/update-text?todo_id={todo_id}&text={text}")
# print(response.status_code)
# print(response.json())

response =  requests.put(f"{BASE_URL}/update-status?todo_id={todo_id}")
print(response.status_code)
print(response.json())
# response = requests.get(f"{BASE_URL}/incomplete-todos")
# print(response.status_code)
# print(response.json())
