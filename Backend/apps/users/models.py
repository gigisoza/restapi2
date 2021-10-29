from typing import Optional
from pydantic import BaseModel


class BackendItem(BaseModel):
    name: str
    due_date: str
    description: Optional[str]