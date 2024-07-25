from typing import Annotated
from pydantic import BeforeValidator
from pymongo import MongoClient
 
client=MongoClient("mongodb+srv://Admin:test123@todos.bwolmni.mongodb.net/?retryWrites=true&w=majority&appName=ToDos")

db = client.get_database("todos")
Todo_collection = db.get_collection("Todo")
User_collection = db.get_collection("User")
 