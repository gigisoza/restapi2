from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from Backend.apps.users.documents import Backend
from Backend.apps.users.models import User
from Backend.apps.users.services.auth import oauth2_scheme, get_current_user

router = APIRouter(prefix="")


@router.get("/get/item", response_model=List[Backend])
async def get_item():
    return await Backend.find_all().to_list()


@router.post("/add/item", status_code=201, response_model=Backend)
async def add_item(item: Backend):
    return await item.save()


@router.post("/update/item/{item_id}", status_code=200, response_model=Backend)
async def update_item(item_id: str, item: Backend):
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


@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
