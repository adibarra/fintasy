# @author: Caleb Kim (caleb-j-kim)
# @description: Portfolio routes for the API

from datetime import datetime
from typing import Optional

from fastapi import Body, Depends, FastAPI, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel

from src.helpers.portfolio import Portfolio
from src.services.database import Database

router = FastAPI()
portfolio_manager = Portfolio(prefix="/portfolio")
db = Database()


class PortfolioData(BaseModel):
    name: str
    tournament: UUID4

    class Config:
        extra = "ignore"


class PortfolioRequest(BaseModel):
    uuid: UUID4
    owner: UUID4
    tournament: UUID4
    name: str
    balance_cents: int
    created_at: datetime
    updated_at: datetime


class UpdatePortfolioRequest(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    qty: Optional[int] = None
    unit_price: Optional[int] = None
    daily_PL: Optional[int] = None
    total_PL: Optional[int] = None

    class Config:
        extra_none = True


class PortfolioResponse(BaseModel):
    code: int
    message: str
    data: PortfolioData

    class Config:
        extra = True


async def verify_token(token: str = Header(...)) -> UUID4:
    # Implement verification logic here

    if token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    token_owner = "00000000-0000-0000-0000-000000000000"
    return token_owner


@router.post(
    "/{tournament}", response_model=PortfolioResponse, status_code=status.HTTP_200_OK
)
def create_portfolio(
    data: PortfolioRequest = Body(...),
):
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
    "/{tournament}", response_model=PortfolioResponse, status_code=status.HTTP_200_OK
)
def list_portfolios(
    uuid: UUID4 = Path(...), token_owner: UUID4 = Depends(verify_token)
):
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


@router.get("/{uuid}", response_model=PortfolioResponse, status_code=status.HTTP_200_OK)
def get_portfolio(uuid: UUID4 = Path(...), token_owner: UUID4 = Depends(verify_token)):
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
    "/{uuid}", response_model=PortfolioResponse, status_code=status.HTTP_200_OK
)
def update_portfolio(
    uuid: UUID4 = Path(...),
    data: UpdatePortfolioRequest = Body(...),
    token_owner: UUID4 = Depends(verify_token),
):
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


@router.delete("/", response_model=PortfolioResponse, status_code=status.HTTP_200_OK)
def remove_portfolio(
    uuid: UUID4 = Path(...), token_owner: UUID4 = Depends(verify_token)
):
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


# Additional endpoints for other operations can be added here
