from fastapi import APIRouter, HTTPException

from app.modules.auth.schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.modules.auth.service import AuthService
from app.modules.auth.exceptions import UsernameTakenError, InvalidCredentialsError
from app.database.database import SessionDep
from app.database.repositories import UserRepoDep


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: RegisterRequest, session: SessionDep, user_repo: UserRepoDep):
    try:
        return await AuthService(session, user_repo).register(body.username, body.password)
    except UsernameTakenError:
        raise HTTPException(status_code=409, detail="Username already taken")


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, session: SessionDep, user_repo: UserRepoDep):
    try:
        return await AuthService(session, user_repo).login(body.username, body.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
