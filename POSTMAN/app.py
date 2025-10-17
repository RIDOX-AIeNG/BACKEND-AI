from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

app = FastAPI(title="Simple FastAPI App", version = "1.0.0")
data = [{"name": "sam larry","age": 20, "track": "AI Developer"},
        {"name": "Bahubali","age":21, "track": "Backend Developer"},
        {"name": "John Doe","age":22, "track": "Frontend Developer"}]
class Item(BaseModel):
    name:str = Field(..., example= "Perpetual")
    age:int = Field(..., example=25)
    track:str = Field(..., example= 'Fullstack Developer' )


@app.get("/", description="This is a good day")
def root():
    return {"Message": "Welcome to my FastAPI Application"}

@app.get("/get_data")
def get_data():
    return data

@app.post("/create_data")
def create_data(req: Item):
    data.append(req.dict())
    return{"Message": "Data Received", "Data": data}

@app.put("/update_data/{id}")
def update_data(id: int, req: Item):
    data[id] = req.dict()
    print(data)
    return{"Message": "Data Updated", "Data": data}

@app.patch("/updated_data/{id}")
def updated_data(id: int, req: Item):
    data[id].update(req.model_dump())
    print(data)
    return{"Message": "Updated_data", "Data":data}

@app.delete("/deleted/")
def deleted(req: Item):
    data.clear()
    return{"message": "Data deleted", "Data": []}

# def test(sam: str)

if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))