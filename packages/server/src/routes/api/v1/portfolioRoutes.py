# @author: adibarra (Alec Ibarra), caleb-j-kim (Caleb Kim)
# @description: Portfolio routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, Query, status
from helpers.portfolio import Portfolio
from pydantic import UUID4, BaseModel
from services.database import Database

db = Database()
router = APIRouter(prefix="/api/v1")


class PortfolioData(BaseModel):
    uuid: UUID4
    owner: UUID4
    tournament: Optional[UUID4] = None
    name: str
    balance_cents: int
    created_at: datetime
    updated_at: datetime

    class Config:
        exclude_none = False


class CreatePortfolioRequest(BaseModel):
    tournament: Optional[UUID4] = None
    name: str

    class Config:
        exclude_none = True


class UpdatePortfolioRequest(BaseModel):
    name: Optional[str] = None

    class Config:
        exclude_none = True


class PortfolioResponse(BaseModel):
    code: int
    message: str
    data: PortfolioData

    class Config:
        extra = True


async def authenticate(
    authorization: str = Header(...), portfolio_uuid: UUID4 = Path(...)
) -> tuple[UUID4, str]:
    token = authorization.split(" ")[1]
    token_owner = db.get_session(token)
    portfolio = db.get_portfolio(str(portfolio_uuid))

    # Validate the token exists
    if token_owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    # Validate the token has permission for this portfolio
    if token_owner != str(portfolio["owner"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return token_owner, token


@router.post(
    "/portfolios", response_model=PortfolioResponse, status_code=status.HTTP_200_OK
)
def create_portfolio(
    data: CreatePortfolioRequest = Body(...),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # TODO: clean up
    if not all(
        [
            Portfolio.validate_uuid(data.uuid),
            Portfolio.validate_owner(data.owner),
            Portfolio.validate_tournament(data.tournament),
            Portfolio.validate_name(data.name),
            Portfolio.validate_balance_cents(data.balance_cents),
            Portfolio.validate_created_at(data.created_at),
            Portfolio.validate_updated_at(data.updated_at),
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 400, "message": "Bad Request"},
        )

    portfolio = db.create_portfolio(
        data.uuid,
        data.owner,
        data.tournament,
        data.name,
        data.balance_cents,
        data.created_at,
        data.updated_at,
    )
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )

    return PortfolioResponse(
        code=200,
        message="Portfolio: {name} Successfully Created",
        data=portfolio,
    )


@router.get(
    "/portfolios", response_model=PortfolioResponse, status_code=status.HTTP_200_OK
)
def get_portfolios(
    owner: Optional[UUID4] = Query(None),
    tournament: Optional[UUID4] = Query(None),
    name: Optional[str] = Query(None),
    offset: Optional[int] = Query(0),
    limit: Optional[int] = Query(10),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # TODO: clean up
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )

    portfolios = db.list_portfolios(uuid)
    if not portfolios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    return PortfolioResponse(
        code=200,
        message="Ok",
        data=portfolios,
    )


@router.get(
    "/portfolios/{portfolio_uuid}",
    response_model=PortfolioResponse,
    status_code=status.HTTP_200_OK,
)
def get_portfolio_by_uuid(
    portfolio_uuid: UUID4 = Path(...),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # TODO: clean up
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )

    portfolio = db.get_portfolio(uuid)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    return PortfolioResponse(
        code=200,
        message="Ok",
        data=portfolio,
    )


@router.patch(
    "/portfolios/{portfolio_uuid}",
    response_model=PortfolioResponse,
    status_code=status.HTTP_200_OK,
)
def update_portfolio(
    portfolio_uuid: UUID4 = Path(...),
    data: UpdatePortfolioRequest = Body(...),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # TODO: clean up
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )

    portfolio = db.get_portfolio(uuid)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    if data.name:
        if not Portfolio.validate_name(data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid Name"},
            )
        portfolio.name = data.name

    if data.company_name:
        if not Portfolio.validate_company_name(data.company_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid Company Name"},
            )
        portfolio.company_name = data.company_name

    if data.qty:
        if not Portfolio.validate_qty(data.qty):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid Quantity"},
            )
        portfolio.qty = data.qty

    if data.unit_price:
        if not Portfolio.validate_unit_price(data.unit_price):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid Unit Price"},
            )
        portfolio.unit_price = data.unit_price

    if data.daily_PL:
        if not Portfolio.validate_daily_PL(data.daily_PL):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid Daily P&L"},
            )
        portfolio.daily_PL = data.daily_PL

    if data.total_PL:
        if not Portfolio.validate_total_PL(data.total_PL):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "Invalid Total P&L"},
            )
        portfolio.total_PL = data.total_PL

    if not db.update_portfolio(
        uuid,
        {
            "name": portfolio.name,
            "company_name": portfolio.company_name,
            "qty": portfolio.qty,
            "unit_price": portfolio.unit_price,
            "daily_PL": portfolio.daily_PL,
            "total_PL": portfolio.total_PL,
        },
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "message": "Conflict"},
        )


@router.delete(
    "portfolios/{portfolio_uuid}",
    response_model=PortfolioResponse,
    status_code=status.HTTP_200_OK,
)
def remove_portfolio(
    portfolio_uuid: UUID4 = Path(...),
    auth: tuple[UUID4, str] = Depends(authenticate),
):
    # TODO: clean up
    if uuid != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "Forbidden"},
        )

    portfolio = db.get_portfolio(uuid)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "Not Found"},
        )

    if not db.remove_portfolio(uuid):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "Internal Server Error"},
        )
    return PortfolioResponse(
        code=200,
        message="Portfolio: {name} Successfully Deleted",
    )
