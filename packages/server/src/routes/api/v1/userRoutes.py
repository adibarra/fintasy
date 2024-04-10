# @author: adibarra (Alec Ibarra), caleb-j-kim (Caleb Kim)
# @description: User routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel, EmailStr

from src.helpers.user import User
from src.services.database import Database

db = Database()
router = APIRouter(
    prefix="/users",
)


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserData(BaseModel):
    uuid: UUID4
    email: EmailStr
    username: str
    coins: int
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = "ignore"


class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        exclude_none = True


class UserResponse(BaseModel):
    code: int
    message: str
    data: Optional[UserData] = None

    class Config:
        exclude_none = True


async def authenticate(token: str = Header(...), uuid: UUID4 = Path(...)) -> bool:
    token_owner = db.get_session(token)

    # Validate the token exists
    if token_owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "Unauthorized"},
        )

    # Validate the token has permission for this resource
    if token_owner != uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )
    return True


@router.post("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
def create_user(
    data: CreateUserRequest = Body(...),
):
    if not all(
        [
            User.validate_email(data.email),
            User.validate_username(data.username),
            User.validate_password(data.password),
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 400, "message": "Bad Request"},
        )

    # Attempt creating user
    user = db.create_user(data.username, data.email, User.hash_password(data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )

    return UserResponse(
        code=200,
        message="Ok",
        data=user,
    )


@router.get("/{uuid}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(
    uuid: UUID4 = Path(...),
    authenticated: bool = Depends(authenticate),
):
    # Attempt fetching user
    user_data = db.get_user(uuid)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )

    # Return user data
    return UserResponse(
        code=200,
        message="Ok",
        data=user_data,
    )


@router.patch("/{uuid}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def patch_user(
    uuid: UUID4 = Path(...),
    data: UpdateUserRequest = Body(...),
    authenticated: bool = Depends(authenticate),
):
    # Attempt fetching user
    user = db.get_user(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    # Validate and update fields if present
    if data.email:
        if not User.validate_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid email"},
            )
        user.email = data.email

    if data.username:
        if not User.validate_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid username"},
            )
        user.username = data.username

    if data.password:
        if not User.validate_password(data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid password"},
            )
        user.password_hash = User.hash_password(data.password)

    # Attempt updating user
    if not db.update_user(
        uuid,
        {
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
        },
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )

    return UserResponse(
        code=200,
        message="Ok",
        data=user,
    )


@router.delete("/{uuid}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user(
    uuid: UUID4 = Path(...),
    authenticated: bool = Depends(authenticate),
):
    # Check if the user exists
    user = db.get_user(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    # Attempt deleting user
    if not db.delete_user(uuid):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "Internal Server Error"},
        )

    return UserResponse(code=200, message="Ok")
