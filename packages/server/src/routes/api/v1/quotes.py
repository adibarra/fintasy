# @author: adibarra (Alec Ibarra), caleb-j-kim (Caleb Kim)
# @description: Quote routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Path, status
from pydantic import BaseModel
from services.alpaca import AlpacaService
from services.database import Database

db = Database()
router = APIRouter(
    prefix="/api/v1",
)


class QuoteData(BaseModel):
    symbol: str
    price: int
    timestamp: datetime


class QuoteResponse(BaseModel):
    code: int
    message: str
    data: Optional[QuoteData] = None

    class Config:
        exclude_none = True


class QuoteHistoricalResponse(BaseModel):
    code: int
    message: str
    data: Optional[list[QuoteData]] = None

    class Config:
        exclude_none = True


async def authenticate(
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


@router.get(
    "/quote/{symbol}", response_model=QuoteResponse, status_code=status.HTTP_200_OK
)
def get_quote(
    symbol: str = Path(...),
    auth: tuple[str, str] = Depends(authenticate),
):
    symbol = symbol.upper()[:4]
    quote = AlpacaService.get_quote(symbol)
    if quote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return QuoteResponse(
        code=200,
        message="Ok",
        data=quote,
    )


@router.get(
    "/quote/historical/{symbol}",
    response_model=QuoteHistoricalResponse,
    status_code=status.HTTP_200_OK,
)
def get_historical_quote(
    symbol: str = Path(...),
    start_date: datetime = None,
    end_date: datetime = None,
    interval: str = None,
    limit: int = 10,
    offset: int = 0,
    auth: tuple[str, str] = Depends(authenticate),
):
    # TODO: implement get_quote_historical in quotes helper class
    # it should access the external api to get the quote historical data
    quote_data = {}
    if quote_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return QuoteResponse(
        code=200,
        message="Ok",
        data=quote_data,
    )
