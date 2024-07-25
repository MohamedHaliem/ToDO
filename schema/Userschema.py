from models.Users import User

 
def individual_user_serial(user) -> User:
  ousr=User(str(user["_id"]),
            str(user["username"]),
            str(user["email"]),
            str(user["full_name"]),
            bool(user["disabled"]),
            str(user["hashed_password"]))
  return ousr 
  
def list_user_Serial(users)->list[User]:
  return [individual_user_serial(user) for user in users]
 
 