from fastapi import APIRouter, Depends
from routes.auth import get_current_user, get_current_admin


route = APIRouter()


@route.get("/account")
async def get_account(current_user=Depends(get_current_user)):
    return current_user


@route.get("/account/for/admin")
async def get_account(current_user=Depends(get_current_admin)):

    return {"admin": current_user}

