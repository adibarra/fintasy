# @author: Caleb Kim (caleb-j-kim)
# @description: Quote routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel

from src.services.database import Database

db = Database()
router = APIRouter(
    prefix="/quotes",
)


class CreateQuoteRequest(BaseModel):
    symbol: str
    price: int
    timestamp: datetime


class QuoteData(BaseModel):
    symbol: str
    price: int
    timestamp: datetime

    class Config:
        extra = "ignore"


class UpdateQuoteRequest(BaseModel):
    symbol: Optional[str] = None
    price: Optional[int] = None
    timestamp: Optional[datetime] = None

    class Config:
        extra_none = True


class QuoteResponse(BaseModel):
    code: int
    message: str
    data: Optional[QuoteData] = None

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


@router.get("/{symbol}", response_model=QuoteResponse, status_code=status.HTTP_200_OK)
def get_quote(symbol: str = Path(...), token_owner: UUID4 = Depends(verify_token)):
    quote_data = db.get_quote(symbol)
    if not quote_data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 404, "message": "Conflict"},
        )

    return QuoteResponse(
        code=200,
        message="Ok",
        data=quote_data,
    )


@router.get(
    "/historical/{symbol}", response_model=QuoteResponse, status_code=status.HTTP_200_OK
)
def get_historical_quote(
    symbol: str = Path(...), token_owner: UUID4 = Depends(verify_token)
):
    quote_data = db.get_historical_quote(symbol)
    if not quote_data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 404, "message": "Conflict"},
        )

    return QuoteResponse(
        code=200,
        message="Ok",
        data=quote_data,
    )
