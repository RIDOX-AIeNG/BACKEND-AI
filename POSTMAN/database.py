from sqlalchemy import create_engine, text 
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 

load_dotenv()

# db_url = dialect+driver://dbuser;dbpassword;dbhost;dbport;dbname              
db_url=f"mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}"

engine = create_engine(db_url)

session = sessionmaker(bind=engine)

db = session()

query = text("select * from user")

users = db.execute(query).fetchall()

print(users)