# @author: adibarra (Alec Ibarra), caleb-j-kim (Caleb Kim)
# @description: User routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
from helpers.user import User
from pydantic import UUID4, BaseModel
from services.database import Database

db = Database()
router = APIRouter(prefix="/api/v1")


class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str


class UserData(BaseModel):
    uuid: UUID4
    email: str
    username: str
    coins: int
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = "ignore"


class UpdateUserRequest(BaseModel):
    email: Optional[str] = None
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


async def authenticate(
    authorization: str = Header(...),
    uuid: UUID4 = Path(...),
) -> tuple[UUID4, str]:
    token = authorization.split(" ")[1]
    token_owner = db.get_session(token)

    # Validate the token exists
    if token_owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    # Validate the token has permission for this resource
    if token_owner != str(uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return token_owner, token


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_200_OK)
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
            detail="Bad Request",
        )

    # Attempt creating user
    user = db.create_user(data.username, data.email, User.hash_password(data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict",
        )

    return UserResponse(
        code=200,
        message="Ok",
        data=user,
    )


@router.get(
    "/users/{uuid}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def get_user(
    uuid: UUID4 = Path(...),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # Attempt fetching user
    user_data = db.get_user(str(uuid))
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    # Return user data
    return UserResponse(
        code=200,
        message="Ok",
        data=user_data,
    )


@router.patch(
    "/users/{uuid}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def patch_user(
    uuid: UUID4 = Path(...),
    data: UpdateUserRequest = Body(...),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # Attempt fetching user
    user = db.get_user(str(uuid))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
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
                detail="Invalid username",
            )
        user.username = data.username

    if data.password:
        if not User.validate_password(data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password",
            )
        user.password_hash = User.hash_password(data.password)

    # Attempt updating user
    if not db.update_user(
        str(uuid),
        {
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
        },
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict",
        )

    return UserResponse(
        code=200,
        message="Ok",
        data=user,
    )


@router.delete(
    "/users/{uuid}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def delete_user(
    uuid: UUID4 = Path(...),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # Check if the user exists
    user = db.get_user(str(uuid))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    # Attempt deleting user
    if not db.delete_user(str(uuid)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return UserResponse(code=200, message="Ok")
