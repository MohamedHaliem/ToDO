 
from fastapi import FastAPI 
 
from routes import Todoroute,Userroute,Aouthroute
 

  
app=FastAPI()
 
 
@app.get("/")
async def get():
    return "welcome to To Do Task"


app.include_router(Aouthroute.routes)
app.include_router(Userroute.routes)
app.include_router(Todoroute.routes)


