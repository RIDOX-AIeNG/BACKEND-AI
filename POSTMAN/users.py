from database import db 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os 
import bcrypt
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="Simple App", version = "1.0.0")

class Simple(BaseModel):
   name:str = Field(..., example= "Sam Larry")
   email:str = Field(..., example="sam@email.com")
   password:str = Field(..., example= 'sam123' )
   user_type:str = Field(..., example= 'student')

@app.post("/signup")
def signup(input: Simple):
    try:
        duplicate_query = text("""
            SELECT * FROM users
            WHERE email = :email

        """)
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        query = text("""
                INSERT INTO users (name, email, password, user_type)
                VALUES (:name, :email, :password, :user_type)
        """)

        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'),salt)
        print(hashedPassword)
        
        db.execute(query, {"name": input.name, "email": input.email, "password":hashedPassword, "user_type": input.user_type})
        db.commit()

        return {"message": "User created successfully",
                "data": {"name":input.name, "email":input.email, "user_type": input.user_type}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    
class LoginRequest(BaseModel):
    email: str = Field(..., examples= "samlarry@gmail.com")
    password: str = Field(..., examples= "sam123")
@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
         SELECT * FROM users WHERE email = :email
""")
        result = db.execute(query, {"email": input.email}).fetchone()

        if not result:
            raise HTTPException(status_code=400, detail = "invalid email or password")
        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))

        if not verified_password: 
            raise HTTPException(status_code = 404, detail = ' invalid email or pasword')
        return {
            "message": "Login Successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e)) 

if __name__=="__main__":
     uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))