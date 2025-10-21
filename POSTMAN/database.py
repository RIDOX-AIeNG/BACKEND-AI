from sqlalchemy import create_engine, text 
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 
from pymysql.constants import CLIENT

load_dotenv()

# db_url = dialect+driver://dbuser;dbpassword;dbhost;dbport;dbname              
db_url=f"mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}"

engine = create_engine(db_url,
                       connect_args={"client_flag": CLIENT.MULTI_STATEMENTS})

session = sessionmaker(bind=engine)

db = session()

query = text("select * from user")

users = db.execute(query).fetchall()

print(users)




create_tables = text("""
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
    );
                         
CREATE TABLE IF NOT EXISTS courses(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    level VARCHAR(100) NOT NULL
                           );


CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    courseId INT,
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (courseId) REFERENCES courses(id)
                           );

"""
)

db.execute(create_tables)

print("Table has been created successfully")