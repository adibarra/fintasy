# @author: Caleb Kim (caleb-j-kim)
# @description: Portfolio routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel

from src.services.database import Database

db = Database()
router = APIRouter(
    prefix="/transactions",
)


class CreateTransactionRequest(BaseModel):
    portfolio_uuid: UUID4
    symbol: str
    qty: int
    unit_price: int
    total_price: int
    transaction_type: str
    created_at: datetime


class TransactionData(BaseModel):
    portfolio_uuid: UUID4
    symbol: str
    qty: int
    unit_price: int
    total_price: int
    transaction_type: str
    created_at: datetime

    class Config:
        extra = "ignore"


class UpdateTransactionRequest(BaseModel):
    portfolio_uuid: Optional[UUID4] = None
    symbol: Optional[str] = None
    qty: Optional[int] = None
    unit_price: Optional[int] = None
    total_price: Optional[int] = None
    transaction_type: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        extra_none = True


class TransactionResponse(BaseModel):
    code: int
    message: str
    data: Optional[TransactionData] = None

    class Config:
        extra = True


async def verify_token(token: str = Header(...)) -> UUID4:
    # Implement verification logic here

    if token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "Unauthorized"},
        )

    # uuid that owns the token
    token_owner = "00000000-0000-0000-0000-000000000000"
    return token_owner


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def create_transaction(
    data: CreateTransactionRequest = Body(...),
):
    if not all(
        [
            data.portfolio_uuid,
            data.symbol,
            data.qty,
            data.unit_price,
            data.total_price,
            data.transaction_type,
            data.created_at,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 400, "message": "Bad Request"},
        )

    transaction = db.create_transaction(
        data.portfolio_uuid,
        data.symbol,
        data.qty,
        data.unit_price,
        data.total_price,
        data.transaction_type,
        data.created_at,
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )
    return TransactionResponse(
        code=200,
        message="Ok",
        data=transaction,
    )


@router.get("/", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def list_transactions(token_owner: UUID4 = Depends(verify_token)):
    transactions = db.list_transactions()
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    return TransactionResponse(
        code=200,
        message="Ok",
        data=transactions,
    )


@router.get(
    "/{portfolio_uuid}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def get_transaction(
    portfolio_uuid: UUID4 = Path(...), token_owner: UUID4 = Depends(verify_token)
):
    transaction = db.get_transaction(portfolio_uuid)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    return TransactionResponse(
        code=200,
        message="Ok",
        data=transaction,
    )
