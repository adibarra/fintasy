# @author: adibarra (Alec Ibarra)
# @description: Transaction routes for the API

from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel
from services.database import Database

db = Database()
router = APIRouter(prefix="/api/v1")


class ACTION(Enum):
    BUY = "BUY"
    SELL = "SELL"


class CreateTransactionRequest(BaseModel):
    portfolio: UUID4
    symbol: str
    action: ACTION
    quantity: int


class GetTransactionRequest(BaseModel):
    portfolio: UUID4
    offset: int = 0
    limit: int = 10


class TransactionData(BaseModel):
    uuid: UUID4
    portfolio: UUID4
    symbol: str
    action: ACTION
    quantity: int
    price_cents: int
    created_at: datetime


class TransactionResponse(BaseModel):
    code: int
    message: str
    data: Optional[TransactionData] = None

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
    transaction_uuid: UUID4 = Path(...),
) -> tuple[str, str]:
    token_owner, token = await authenticateToken(authorization)

    # Validate the token has permission for this user's transactions
    transaction = db.get_transaction_by_uuid(str(transaction_uuid))
    portfolio = db.get_portfolio(str(transaction["portfolio"]))
    if token_owner != str(portfolio["owner"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return token_owner, token


@router.post(
    "/transactions", response_model=TransactionResponse, status_code=status.HTTP_200_OK
)
def create_transaction(
    data: CreateTransactionRequest = Body(...),
    auth: tuple[str, str] = Depends(authenticateToken),
):
    # Attempt creating transaction
    transaction = db.create_transaction(
        str(data.portfolio), str(data.symbol), data.action.value, data.quantity, 52.48
    )
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict",
        )

    return TransactionResponse(
        code=200,
        message="Ok",
        data=transaction,
    )


@router.get(
    "/transactions",
    response_model=list[TransactionResponse],
    status_code=status.HTTP_200_OK,
)
def get_transactions(
    data: GetTransactionRequest = Body(...),
    auth: tuple[str, str] = Depends(authenticateToken),
):
    token_owner = auth[0]

    # Keep the user from accessing another user's transactions
    # Fix by adding a more granular permission system later
    portfolio = db.get_portfolio(str(data.portfolio))
    if token_owner != str(portfolio["owner"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    # Attempt getting transactions
    transactions = db.get_transactions(str(data.portfolio), data.offset, data.limit)
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return TransactionResponse(
        code=200,
        message="Ok",
        data=transactions,
    )


@router.get(
    "/transactions/{transaction_uuid}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def get_transaction_by_id(
    transaction_uuid: UUID4 = Path(...),
    auth: tuple[str, str] = Depends(authenticate),
):
    # Attempt getting transaction
    transaction = db.get_transaction_by_uuid(str(transaction_uuid))
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return TransactionResponse(
        code=200,
        message="Ok",
        data=transaction,
    )
