import os
from os.path import join, dirname
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

# JWT CONFIGURATION 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

MODEL_NAME = "deepseek-r1:1.5b"