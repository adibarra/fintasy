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
    token, token_owner = authenticateToken(authorization)

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

    # TODO: only need to validate portfolio name
    # but none of these functions are implemented
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
            detail="Bad Request",
        )

    # TODO: check the parameters for create_portfolio
    # the ones that are being passed in don't match the function signature
    portfolio = db.create_portfolio(
        data.uuid,
        data.owner,
        data.tournament,
        data.name,
        data.balance_cents,
        data.created_at,
        data.updated_at,
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


# TODO: extract the query parameters into a separate class like GetPortfoliosRequest or something (tournament offset, limit are all optional)
@router.get(
    "/portfolios", response_model=PortfolioResponse, status_code=status.HTTP_200_OK
)
def get_portfolios(
    owner: UUID4 = Query(...),
    tournament: UUID4 = Query(...),
    name: str = Query(...),
    offset: int = Query(...),
    limit: int = Query(...),
    auth: tuple[UUID4, str] = Depends(authenticateToken),
):
    token_owner = auth[0]

    # Keep this check for now, might remove later with a more complex permission system
    if owner != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    # TODO: use db.get_portfolios() instead, and pass in the query parameters
    portfolios = db.list_portfolios(uuid)
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

    # TODO: Portfolio.validate name doesn't exist
    if data.name:
        if not Portfolio.validate_name(data.name):
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

    # TODO: db.delete_portfolio is probably what you want to use here
    if not db.remove_portfolio(uuid):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return PortfolioResponse(
        code=200,
        message="Ok",
    )
