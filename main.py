import asyncio
from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []
class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    user = next((user for user in users if user.id == user_id), None)
    if user:
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post('/user/{username}/{age}')
async def post_user(user: User, username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='Valery')],
        age: int = Path(ge=18, le=120, description="Enter age", examples='55')):
    user_id = max((i.id for i in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user
@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user: User, user_id: int,
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='Valery')],
                      age: int = Path(ge=18, le=120, description="Enter age", examples='55')):
    for u in users:
        if u.id == user_id:
            u.username = username
            u.age = age
            return u
    raise HTTPException(status_code=404, detail="User was not found")
@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
     for i, u in enumerate(users):
         if u.id == user_id:
             users.pop(i)
             return {f'User {user_id} is delete'}
     raise HTTPException(404, 'User was not found')
