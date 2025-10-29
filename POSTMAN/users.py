from database import db 
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
import os 
import bcrypt
from dotenv import load_dotenv
import uvicorn

from middleware import create_token, verify_token

load_dotenv()

app = FastAPI(title="Simple App", version = "1.0.0")

token_time = int(os.getenv("token_time"))

class Simple(BaseModel):
   name:str = Field(..., example= "Sam Larry")
   email:str = Field(..., example="sam@email.com")
   password:str = Field(..., example= 'sam123' )
   user_type:str = Field(..., example= 'student')

class LoginRequest(BaseModel):
    email: str = Field(..., example= "samlarry@gmail.com")
    password: str = Field(..., example= "sam123")

class courseRequest(BaseModel):
    title: str = Field(..., example="Algorithm")
    level: str = Field(..., example="200lvl")

class id(BaseModel):
    courseid: int = Field(..., example= 1)


@app.get("/")
def rooot():
    return {
        "message": "HELLO WORLD"
    }

@app.post("/signup")
def signup(input: Simple):
    try:
        duplicate_query = text("""
            SELECT * FROM users
            WHERE email = :email

        """)
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            print("email already exists")
            # raise HTTPException(status_code=400, detail="Email already exists")

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
        
        encoded_token = create_token(details={
             "id": result.id,
            "email": result.email,
            "user_type": result.user_type
           
        },expiry=token_time)

        return {
            "message": "Login Successful","token": encoded_token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e)) 
    



@app.post("/courses")
def add_courses(input: courseRequest, user_data = Depends(verify_token)):
    try:
        
        print(user_data)
        if user_data["user_type"] != "admin":
            raise HTTPException(status_code=401, detail="You are not authorized to add a course")
        

        query = text("""
            INSERT INTO courses (title, level)
            VALUES (:title, :level)
        """)

        

        db.execute(query, {"title":input.title, "level": input.level})
        db.commit()

        return {"message": f"course {input.title} created successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()




@app.post("/enroll")
def enrollcourse(input:id, user_data = Depends(verify_token)):
    try:
        print(user_data)
        if user_data["user_type"] != "student":
            raise HTTPException(status_code=401, detail="You are not authorized to enroll for a course")
        query=text("""
            INSERT INTO enrollments(userid,courseid)
                VALUES(:userid,:courseid)
                   """)
        db.execute(query, {"userid":user_data["id"], "courseid":input.courseid})
        db.commit()
        return {
        "message": "Course created sucessfully",
        "data": {
            "userid":user_data["id"],
            "courseid":input.courseid
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__=="__main__":
     uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))