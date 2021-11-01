from typing import Optional
from pydantic import BaseModel


class BackendItem(BaseModel):
    name: str
    due_date: str
    description: Optional[str]


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
