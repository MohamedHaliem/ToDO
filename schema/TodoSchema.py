from models.todos import Todo 


def individual_todos_serial(todo) -> Todo:
  otodo=Todo(
  str(todo["_id"]),
  str(todo["title"]),
  str(todo["description"]),
  str(todo["status"]),
  todo["due_date"] ,
 todo["UserId"] )
 
  return  otodo
  
def list_todos_Serial(todos)->list[Todo]:
  return list(individual_todos_serial(todo) for todo in todos)
 
 