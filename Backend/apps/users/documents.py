from typing import List, Optional
from beanie import Document
from datetime import datetime


class Backend(Document):
    item: str
    due_date: str
    description: Optional[str]