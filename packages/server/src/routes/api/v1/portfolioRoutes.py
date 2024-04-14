# @author: adibarra (Alec Ibarra), caleb-j-kim (Caleb Kim)
# @description: Portfolio routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
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


class GetPortfoliosRequest(BaseModel):
    owner: UUID4
    tournament: Optional[UUID4] = None
    name: Optional[str] = None
    offset: Optional[int] = 0
    limit: int

    class Config:
        exclude_none = True


class PortfolioResponse(BaseModel):
    code: int
    message: str
    data: PortfolioData

    class Config:
        extra = True


async def authenticateToken(
    authorization: str = Header(...),
) -> tuple[UUID4, str]:
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
    portfolio_uuid: UUID4 = Path(...),
) -> tuple[UUID4, str]:
    token_owner, token = authenticateToken(authorization)

    # Validate the token has permission for this portfolio
    portfolio = db.get_portfolio(str(portfolio_uuid))
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
    auth: tuple[UUID4, str] = Depends(authenticateToken),
):
    token_owner = auth[0]

    if not all([Portfolio.validate_portfolio_name(data.name)]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    portfolio = db.create_portfolio(
        data.tournament,
        data.name,
    )
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict",
        )

    return PortfolioResponse(
        code=200,
        message="Ok",
        data=portfolio,
    )


@router.get(
    "/portfolios", response_model=PortfolioResponse, status_code=status.HTTP_200_OK
)
def get_portfolios(
    data: GetPortfoliosRequest = Body(...),
    auth: tuple[UUID4, str] = Depends(authenticateToken),
):
    token_owner = auth[0]

    # Keep this check for now, might remove later with a more complex permission system
    # if owner != token_owner:
    # raise HTTPException(
    # status_code=status.HTTP_403_FORBIDDEN,
    # detail="Forbidden",
    # )

    # TODO: use db.get_portfolios() instead, and pass in the query parameters (resolved?)
    portfolios = db.get_portfolios(
        data.owner, data.tournament, data.name, data.offset, data.limit, auth
    )
    if portfolios is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
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
    portfolio = db.get_portfolio(portfolio_uuid)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
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
    portfolio = db.get_portfolio(portfolio_uuid)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    if data.name:
        if not Portfolio.validate_portfolio_name(data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request",
            )

    if not db.update_portfolio(portfolio_uuid, data.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict",
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
    portfolio = db.get_portfolio(portfolio_uuid)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    if not db.delete_portfolio(portfolio_uuid):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return PortfolioResponse(
        code=200,
        message="Ok",
    )