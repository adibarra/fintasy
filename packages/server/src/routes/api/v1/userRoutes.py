# @author: Alec Ibarra (adibarra) & Caleb Kim (caleb-j-kim)
# @description: User routes for the API

# placeholder pseudocode until the route loading is actually setup

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path
from pydantic import UUID4, BaseModel

from src.helpers.user import User
from src.services.database import Database


class UserInput(BaseModel):
    username: str
    password: str
    email: str


class UserData(BaseModel):
    uuid: UUID4
    owner: UUID4
    username: str
    email: str
    coins: 1
    created_at: datetime
    updated_at: datetime


class UserPatch(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    code: int
    message: str
    data: UserData


class ErrorResponse(BaseModel):
    code: int
    message: str


router = APIRouter(
    prefix="/users",
)
db = Database()


@router.post("/", response_model=UserResponse)
def create_user(user: UserInput = Body(...)):
    if not (
        User.validate_username(user.username)
        and User.validate_password(user.password)
        and User.validate_email(user.email)
    ):
        raise HTTPException(
            status_code=400, detail="Invalid username, password, or email"
        )

    # Attempt creating user
    if not db.create_user(user.username, user.email, User.hash_password(user.password)):
        raise HTTPException(
            status_code=409,
            detail="User already exists or Email address is already in use.",
        )

    # Retrieve new user
    user_data = db.get_user_by_email(user.email)
    if user_data is None:
        raise HTTPException(
            status_code=500, detail="User could not be retrieved after creation"
        )

    return UserResponse(
        code=200,
        message="Ok",
        data=UserData(
            uuid=user_data["uuid"],
            email=user_data["email"],
            username=user_data["username"],
            coins=user_data["coins"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"],
        ),
    )


@router.get("/{uuid}", response_model=UserResponse)
def get_user(uuid: UUID4 = Path(...)):
    try:
        user_data = db.get_user(uuid)
        if not user_data:
            raise HTTPException(
                status_code=404, detail={"code": 404, "message": "Not Found"}
            )

        return UserResponse(
            code=200,
            message="Ok",
            data=user_data,  # Assuming this directly maps to the UserData model
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "Internal Server Error"}
        )


@router.patch("/{uuid}", response_model=UserResponse)
def patch_user(
    uuid: UUID4 = Path(..., description="The UUID of the user to be updated"),
    update_data: UserInput = Body(...),
):
    # Attempt fetching user
    user = db.get_user(uuid)
    if not user:
        raise HTTPException(
            status_code=404, detail={"code": 404, "message": "Not Found"}
        )

    # Validate and update fields if present
    if update_data.username:
        if not User.validate_username(update_data.username):
            raise HTTPException(
                status_code=400, detail={"code": 400, "message": "Invalid username"}
            )
        user.username = update_data.username

    if update_data.password:
        if not User.validate_password(update_data.password):
            raise HTTPException(
                status_code=400, detail={"code": 400, "message": "Invalid password"}
            )
        user.password_hash = User.hash_password(update_data.password)

    if update_data.email:
        if not User.validate_email(update_data.email):
            raise HTTPException(
                status_code=400, detail={"code": 400, "message": "Invalid email"}
            )
        user.email = update_data.email

    # Attempt updating user
    if not db.update_user(user):
        raise HTTPException(
            status_code=409, detail={"code": 409, "message": "Conflict during update"}
        )

    return {"code": 200, "message": "Ok"}


@router.delete("/{uuid}", response_model=ErrorResponse)
def delete_user(
    uuid: UUID4 = Path(..., description="The UUID of the user to be deleted"),
):
    try:
        # Attempt fetching the user to ensure they exist before attempting deletion
        user = db.get_user(uuid)
        if not user:
            raise HTTPException(
                status_code=404, detail={"code": 404, "message": "User not found"}
            )

        # Attempt deleting the user
        deletion_success = db.delete_user(uuid)
        if not deletion_success:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": 500,
                    "message": "Internal Server Error during deletion",
                },
            )

        return {"code": 200, "message": "User successfully deleted"}
    except KeyError:
        # If the user doesn't exist, return a 404
        raise HTTPException(
            status_code=404, detail={"code": 404, "message": "User not found"}
        )
    except Exception as e:
        # For any other exceptions, return a 500
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"Internal Server Error: {str(e)}"},
        )
