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


# Reusing the authenticate dependency from your user routes for consistency
async def authenticate(
    authorization: str = Header(...), transaction_uuid: UUID4 = Path(...)
) -> tuple[UUID4, str]:
    token = authorization.split(" ")[1]
    token_owner = db.get_session(token)
    transaction = db.get_transaction_by_uuid(str(transaction_uuid))
    portfolio = db.get_portfolio(str(transaction["portfolio"]))

    # Validate the token exists
    if token_owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    # Validate the token has permission for this user's transactions
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
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # Attempt creating transaction
    transaction = db.create_transaction(
        data.portfolio, data.symbol, data.action, data.quantity
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
    auth: tuple[UUID4, str] = Depends(authenticate),
):
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
    auth: tuple[UUID4, str] = Depends(authenticate),
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
