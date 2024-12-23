import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from starlette import status

from db import fake_users_db
from werkzeug.security import check_password_hash
from tools import create_token, decode_token
from settings import settings_app

route = APIRouter()

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

db = {}


@route.post("/auth/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Username or Password incorrect")

    if not check_password_hash(user["hashed_password"], form_data.password):
        raise HTTPException(status_code=400, detail="Username or Password incorrect")

    return {"access_token": create_token(data={"name": user}), "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_admin(current_user=Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="only for admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings_app.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")
