import jwt
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

secret_key = os.getenv("secret_key")
def create_token(details,expiry):
    expire =datetime.now() + expiry

    details.update
