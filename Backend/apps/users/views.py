from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from typing import List
from Backend.apps.users.documents import Backend
from fastapi import Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException


router = APIRouter(prefix="")


@router.get("/get/item", response_model=List[Backend])
async def register_user():
    return await Backend.find_all().to_list()


@router.post("/add/item", status_code=201, response_model=Backend)
async def register_user(item: Backend):
    return await item.save()


@router.post("/update/item/{item_id}", status_code=200, response_model=Backend)
async def register_user(item_id: str, item: Backend):
    if todo := await Backend.find_one(Backend.id == PydanticObjectId(item_id)):
        todo.item = item.item
        if item.description:
            todo.desc = item.description
        return await todo.save()
    raise HTTPException(status_code=400, detail="not found")


@router.post("/delete/item", response_model=Backend)
async def delete_item(item_id: str, item: Backend):
    if todo := await Backend.find_one(Backend.id == PydanticObjectId(item_id)):
        return await Backend.delete(todo)
    raise HTTPException(status_code=400, detail="not found")


SECRET = "secret-key"


manager = LoginManager(SECRET, tokenUrl="/auth/login", use_cookie=True)
manager.cookie_name = "some-name"


DB = {"username": {"password": "qwertyuiop"}}


@manager.user_loader
def load_user(username: str):
    user = DB.get(username)
    return user


@router.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={"sub": username}
    )
    resp = RedirectResponse(url="/private", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@router.get("/private")
def getPrivateendpoint(_=Depends(manager)):
    return "You are an authentciated user"
