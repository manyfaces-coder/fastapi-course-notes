#Для обработки http запросов
from .schemas import CreateUser
from fastapi import APIRouter
from . import crud
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
# def create_user(email: EmailStr = Body()):
def create_user(user: CreateUser):
    # return {"message": "success",
    #         "email": users.email,
    #         }
    return crud.create_user(user_in=user)
