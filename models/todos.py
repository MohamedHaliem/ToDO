from dataclasses import   dataclass
from typing import List, Optional
from pydantic import   EmailStr
from datetime import date, datetime 


 
    
@dataclass
class Todo():
    id:str
    title:Optional[str]  = None
    description:Optional[str]  = None
    status:Optional[str]  = None
    due_date:Optional[date]  = None
    UserId:Optional[str]  = None
    
    
@dataclass
class TodoInDB():
    title:str 
    description:str 
    status:str 
    due_date: datetime 
    UserId:Optional[str]  = None
    