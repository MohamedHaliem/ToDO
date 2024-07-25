from datetime import   datetime, time
 
from fastapi import APIRouter, Body
from models import todos
from Config import database
from models.Users import User, UserInDB
from routes.Aouthroute import get_current_active_user, get_current_user, get_password_hash
from schema import Userschema
from bson import ObjectId


from datetime import datetime, time, timedelta, timezone
from typing import Annotated

from bson import ObjectId
import jwt
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
 

from Config import database
from models import todos
from models.Users import Token, TokenData, User
from schema import TodoSchema,Userschema

routes=APIRouter()
  
@routes.post("/create_User/")
async def create_user( current_user: Annotated[User, Depends(get_current_active_user)],user:  UserInDB= Body(...)):
    try:  
        user.hashed_password= get_password_hash(user.hashed_password)
        new_user =   database.User_collection.insert_one(user.__dict__)
        created_user =   database.User_collection.find_one(
       {"_id": new_user.inserted_id}
        )
        return  Userschema.individual_user_serial(created_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e))
    
@routes.post("/Updateuser/")
async def Update_user(current_user: Annotated[User, Depends(get_current_active_user)],user:User = Body(...)):
    try:    
        Find_user=  Userschema.individual_user_serial( database.User_collection.find_one(
            {"_id": ObjectId(user.id)}
        ))
        if Find_user==None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="No Data Found" )
        else:                      
                user.hashed_password= get_password_hash(user.hashed_password)
                Find_user.email= Find_user.title if user.email is None else user.email  
                Find_user.full_name=Find_user.full_name if user.full_name is None else user.full_name 
                Find_user.hashed_password=Find_user.hashed_password if user.hashed_password is None else user.hashed_password
                Find_user.disabled=Find_user.disabled if user.disabled is None else user.disabled 
                
                database.Todo_collection.update_one( {"_id" :ObjectId(user.id)},{"$set" : Find_user.__dict__}) 
  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Error :" +str(e) ) 
    return  Find_user   

  
@routes.get("/getcurrentuser/")
async def getcurrentuser(  current_user: Annotated[User, Depends(get_current_user)] ):
    try:
        Find_user=  Userschema.individual_user_serial(database.User_collection.find_one(
        {"_id":ObjectId(current_user.id)}
        ))
        print(Find_user)
        return Find_user
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e))     
    
@routes.get("/GetUser/")
async def GetUser(  current_user: Annotated[User, Depends(get_current_user)],):
    try:
         return Userschema.list_user_Serial(database.User_collection.find())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e)) 
