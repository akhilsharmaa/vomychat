import os
from os.path import join, dirname
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

# JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = "postgresql://vomychat_owner:npg_6evZ0BSIfozH@ep-summer-poetry-a5ji43bf.us-east-2.aws.neon.tech/vomychat"
SERPER_API_KEY = os.environ.get("SERPER_API_KEY") 
BASE_API = "https://assignment-vomychat.onrender.com"

# JWT CONFIGURATION 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

MODEL_NAME = "deepseek-r1:1.5b"