# @author: Caleb Kim (caleb-j-kim)
# @description: Portfolio routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel

from src.helpers.tournament import Tournament
from src.services.database import Database

db = Database()
router = APIRouter(
    prefix="/tournament",
)


class TournamentRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = "ignore"


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


class TournamentResponse(BaseModel):
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


@router.post(
    "/",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def create_tournament(
    data: TournamentRequest = Body(...),
):
    if not all(
        [
            Tournament.validate_name(data.name),
            Tournament.validate_date(data.start_date),
            Tournament.validate_end(data.end_date),
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 400, "message": "Bad Request"},
        )

    tournaments = db.create_tournament(data)
    return TournamentResponse(
        code=200,
        message="Ok",
        data=tournaments,
    )


@router.get(
    "/",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def list_tournaments():
    tournaments = db.list_tournaments()
    if not tournaments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )
    return TournamentResponse(
        code=200,
        message="Ok",
        data=tournaments,
    )


@router.get(
    "/{uuid}",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def get_tournament(uuid: UUID4 = Path(...), token_owner: UUID4 = Depends(verify_token)):
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )
    tournaments = db.get_tournament(uuid)
    if not tournaments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )
    return TournamentResponse(
        code=200,
        message="Ok",
        data=tournaments,
    )


@router.patch(
    "/{uuid}",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def update_tournament(
    uuid: UUID4 = Path(...),
    data: UpdateTransactionRequest = Body(...),
    token_owner: UUID4 = Depends(verify_token),
):
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )
    tournaments = db.update_tournament(uuid, data)
    if not tournaments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    if data.portfolio_uuid:
        if not Tournament.validate_portfolio_uuid(data.portfolio_uuid):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid name"},
            )
        tournaments.portfolio_uuid = data.portfolio_uuid

    if data.symbol:
        if not Tournament.validate_symbol(data.symbol):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid symbol"},
            )
        tournaments.symbol = data.symbol

    if data.qty:
        if not Tournament.validate_qty(data.qty):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid quantity"},
            )
        tournaments.qty = data.qty

    if data.unit_price:
        if not Tournament.validate_unit_price(data.unit_price):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid unit price"},
            )
        tournaments.unit_price = data.unit_price

    if data.total_price:
        if not Tournament.validate_total_price(data.total_price):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid total price"},
            )
        tournaments.total_price = data.total_price

    if data.transaction_type:
        if not Tournament.validate_transaction_type(data.transaction_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid transaction type"},
            )
        tournaments.transaction_type = data.transaction_type

    if data.created_at:
        if not Tournament.validate_created_at(data.created_at):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid time"},
            )
        tournaments.created_at = data.created_at

    if not db.update_tournament(
        uuid,
        {
            "portfolio_uuid": tournaments.portfolio_uuid,
            "symbol": tournaments.symbol,
            "qty": tournaments.qty,
            "unit_price": tournaments.unit_price,
            "total_price": tournaments.total_price,
            "transaction_type": tournaments.transaction_type,
            "created_at": tournaments.created_at,
        },
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )

    return TournamentResponse(
        code=200,
        message="Ok",
        data=tournaments,
    )


@router.delete(
    "/{uuid}",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def remove_tournament(
    uuid: UUID4 = Path(...), token_owner: UUID4 = Depends(verify_token)
):
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )
    tournaments = db.get_tournament(uuid)
    if not tournaments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    if not db.remove_tournament(uuid):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )

    return TournamentResponse(
        code=200,
        message="Tournament {uuid} has been deleted",
        data=tournaments,
    )
