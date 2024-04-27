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


class UserResponse(BaseModel):
    code: int
    message: str
    data: Optional[UserData] = None

    class Config:
        exclude_none = True


async def authenticateToken(
    authorization: str = Header(...),
) -> tuple[str, str]:
    if not len(authorization.split(" ")) == 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    token = authorization.split(" ")[1]
    token_owner = db.get_session(token)

    # Validate the token exists
    if token_owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return token_owner, token


async def authenticate(
    authorization: str = Header(...),
    uuid: str = Path(...),
) -> tuple[str, str]:
    token_owner, token = await authenticateToken(authorization)

    # Validate the token has permission for this resource
    if str(token_owner) != str(uuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return token_owner, token


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_200_OK)
def create_user(
    data: CreateUserRequest = Body(...),
):
    try:
        User.validate_email(data.email)
        User.validate_username(data.username)
        User.validate_password(data.password)
    except ValueError:
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
    auth: tuple[str, str] = Depends(authenticate),
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
    auth: tuple[str, str] = Depends(authenticate),
):
    # Attempt fetching user
    user = db.get_user(str(uuid))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    # Validate and update fields if present
    try:
        if data.email is not None:
            User.validate_email(data.email)
        if data.username is not None:
            User.validate_username(data.username)
        if data.password is not None:
            User.validate_password(data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    # Attempt updating user
    if not db.update_user(
        str(uuid),
        data.email,
        data.username,
        User.hash_password(data.password) if data.password else None,
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
    auth: tuple[str, str] = Depends(authenticate),
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
