from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Token():
    access_token: str
    token_type: str

@dataclass
class TokenData():
    username: str | None = None

@dataclass
class User():
    id:str | None = None
    username: str| None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str| None = None

@dataclass
class UserInDB(): 
    username: str| None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str| None = None