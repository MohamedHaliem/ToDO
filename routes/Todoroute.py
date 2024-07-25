from datetime import   datetime, time
 
from fastapi import APIRouter, Body
from models import todos
from Config import database
from models.Users import User, UserInDB
from routes.Aouthroute import get_current_active_user
from schema import TodoSchema
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
from schema import TodoSchema

routes=APIRouter()
# to get a string like this run:
# openssl rand -hex 32


 
@routes.get("/getTodo/")
async def getTodo(current_user: Annotated[User, Depends(get_current_active_user)],):
    try:
        data= TodoSchema.list_todos_Serial( database.Todo_collection.find() )
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e))
 

 
@routes.get("/getTodoById/")
async def getTodoById(current_user: Annotated[User, Depends(get_current_active_user)],id:str):
    try:
        Find_todo=   database.Todo_collection.find_one(
        {"_id": ObjectId(id)}
        ) 
        print(Find_todo)
        if Find_todo==None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="No Data Found" )
        else:
            return TodoSchema.individual_todos_serial(Find_todo)
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e))

@routes.post("/create_Task/")
async def create_todo(current_user: Annotated[User, Depends(get_current_active_user)],todo:todos.TodoInDB = Body(...)):
    try:
        
        todo.UserId=current_user.id 
        new_todo =  database.Todo_collection.insert_one(todo.__dict__)
        created_todo =   database.Todo_collection.find_one(
            {"_id": new_todo.inserted_id}
        )
        return TodoSchema.individual_todos_serial(created_todo)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e))

@routes.post("/Update_todo/")
async def Update_todo(current_user: Annotated[User, Depends(get_current_active_user)],todo:todos.Todo = Body(...)):
    try:    
        Find_todo=  TodoSchema.individual_todos_serial( database.Todo_collection.find_one(
            {"_id": ObjectId(todo.id)}
        ))
        if Find_todo==None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="No Data Found" )
        else:
            if Find_todo.UserId!=current_user.id :
               raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to change in this Task" 
        )
               
            else:            
                Find_todo.title= Find_todo.title if todo.title is None else todo.title  
                Find_todo.description=Find_todo.description if todo.description is None else todo.description 
                Find_todo.status=Find_todo.status if todo.status is None else todo.status
                Find_todo.due_date=Find_todo.due_date if todo.due_date is None else datetime.combine(todo.due_date|None, time.min) 
                Find_todo.UserId=Find_todo.UserId if todo.UserId is None else todo.UserId  
                database.Todo_collection.update_one( {"_id" :ObjectId(todo.id)},{"$set" : Find_todo.__dict__}) 
  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Error :" +str(e) ) 
    return  Find_todo 

@routes.get("/getTodoByCurrantUser/")
async def getTodo(current_user: Annotated[User, Depends(get_current_active_user)] ):
    try:  
          return TodoSchema.list_todos_Serial(database.Todo_collection.find(
        {"UserId":str(current_user.id)}
    ))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e))
      
      
@routes.get("/deleteToDo/")
async def deleteToDo(current_user: Annotated[User, Depends(get_current_active_user)], id:str ):
    try:
        Find_todo=  TodoSchema.individual_todos_serial(database.Todo_collection.find_one(
            {"_id": ObjectId(id)}
        ))
        if Find_todo==None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="No Data Found" )
        else:
            if Find_todo.UserId!=current_user.id :
               raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to change in this Task" 
        )
            database.Todo_collection.delete_one({"_id": ObjectId(id)})
            return "Record Deleted"
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                           detail="Error :" +str(e))
   