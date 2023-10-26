from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth")
async def create_user(req: CreateUserRequest):
    user_model = Users(
        email = req.email,
        username = req.username,
        first_name = req.first_name,
        last_name = req.last_name,
        hashed_password = bcrypt_context.hash(req.password),
        role = req.role,
        is_active = True,
    )

    return user_model
