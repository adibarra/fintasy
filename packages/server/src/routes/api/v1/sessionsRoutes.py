# @author: Caleb Kim (caleb-j-kim)
# @description: Sessions routes for the API

from typing import Optional

from fastapi import Body, Depends, FastAPI, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel, EmailStr

from src.helpers.sessions import Session
from src.helpers.user import User
from src.services.database import Database


class SessionData(BaseModel):
    uuid: UUID4
    owner: UUID4
    username: str
    email: EmailStr


class SessionRequest(BaseModel):
    username: str
    password: str
    email: EmailStr


class Config:
    extra = "ignore"


class UpdateSessionRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class SessionResponse(BaseModel):
    code: int
    message: str
    data: Optional[SessionData] = None

    class Config:
        exclude_none = True


router = FastAPI(prefix="/sessions")
db = Database()


async def verify_token(token: str = Header(...)) -> UUID4:
    # Implement verification logic here

    if token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    token_owner = "00000000-0000-0000-0000-000000000000"
    return token_owner


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_200_OK)
def create_session(data: SessionRequest = Body(...)):
    if not all(
        [
            Session.validate_username(data.username)
            and Session.validate_password(data.password)
            and Session.validate_email(data.email)
        ]
    ):
        raise HTTPException(
            status_code=400,
            detail={"code": 400, "message": "Bad Request"},
        )

    session = db.create_session(
        data.username, data.password, User.hash_password(data.password)
    )
    if not session:
        raise HTTPException(
            status_code=409,
            detail={"code": 409, "message": "Conflict"},
        )
    return SessionResponse(code=200, message="Ok", data=session)


@router.get(
    "/sessions/{uuid}", response_model=SessionResponse, status_code=status.HTTP_200_OK
)
def get_session(uuid: UUID4 = Path(...), token: UUID4 = Depends(verify_token)):
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )

    session_data = db.get_session(uuid)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 409, "message": "Conflict"},
        )

    return SessionResponse(code=200, message="Ok", data=session_data)
