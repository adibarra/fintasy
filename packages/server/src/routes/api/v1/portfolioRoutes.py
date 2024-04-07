# @author: Caleb Kim (caleb-j-kim)
# @description: Portfolio routes for the API

from datetime import datetime
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import UUID4, BaseModel

from src.helpers.portfolio import Portfolio
from src.services.database import Database


class PortfolioInput(BaseModel):
    name: str
    tournament: UUID4


class PortfolioData(BaseModel):
    uuid: UUID4
    owner: UUID4
    tournament: UUID4
    name: str
    balance_cents: int
    created_at: datetime
    updated_at: datetime


class PortfolioPatch(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    qty: Optional[int] = None
    unit_price: Optional[int] = None
    daily_PL: Optional[int] = None
    total_PL: Optional[int] = None


class PortfolioResponse(BaseModel):
    code: int
    message: str
    data: PortfolioData


class ErrorResponse(BaseModel):
    code: int
    message: str


app = FastAPI()
portfolio_manager = Portfolio()
db = Database()


@app.post("/portfolios/{tournament}", response_model=PortfolioResponse)
def add_portfolio(
    tournament: UUID4 = Path(...),
    portfolio: PortfolioInput = None,
    expand: Optional[bool] = Query(False, description=""),
):
    try:
        from uuid import uuid4

        portfolio_uuid = uuid4()
        owner_uuid = uuid4()
        current_time = datetime.now()

        # Assuming the operation is successful and returns necessary data
        portfolio_data = PortfolioData(
            uuid=portfolio_uuid,
            owner=owner_uuid,
            tournament=portfolio_manager.tournament,
            name=portfolio_manager.name,
            balance_cents=50000,
            created_at=current_time,
            updated_at=current_time,
        )

        if not db.add_portfolio(portfolio):
            raise HTTPException(
                status_code=409, detail="Portfolio has already been added."
            )
        return PortfolioResponse(code=200, message="Ok", data=portfolio_data)
    except ValueError:
        raise HTTPException(
            status_code=400, detail={"code": 400, "message": "Bad Request"}
        )


@app.get("/portfolios/{tournament}", response_model=PortfolioResponse)
def list_portfolios(
    owner: Optional[UUID4] = Query(None),
    tournament: Optional[UUID4] = Path(...),
    name: Optional[str] = Query(None),
    offset: int = Query(0),
    limit: int = Query(10),
):
    try:
        from uuid import uuid4

        portfolio_uuid = uuid4()
        owner_uuid = uuid4()
        current_time = datetime.now()
        portfolios = PortfolioData(
            uuid=portfolio_uuid,
            owner=owner_uuid,
            tournament=portfolio_manager.tournament,
            name=portfolio_manager.name,
            balance_cents=50000,
            created_at=portfolio_manager.created_at,
            updated_at=current_time,
        )

        return PortfolioData(code=200, message="Ok", data=portfolios[:limit])
    except Exception:
        raise HTTPException(
            status_code=400, detail={"code": 400, "message": "Bad Request"}
        )


@app.get("/portfolios/{uuid}", response_model=PortfolioResponse)
def get_portfolio(uuid: UUID4 = Path(...)):
    try:
        from uuid import uuid4

        portfolio_uuid = uuid4()
        owner_uuid = uuid4()
        portfolio_data = PortfolioData(
            uuid=portfolio_uuid,
            owner=owner_uuid,
            tournament=portfolio_manager.tournament,
            name=portfolio_manager.name,
            balance_cents=50000,
            created_at=portfolio_manager.created_at,
            updated_at=portfolio_manager.updated_at,
        )

        return PortfolioResponse(
            code=200,
            message="Portfolio: {name} Successfully Acquired",
            data=portfolio_data,
        )
    except Exception:
        raise HTTPException(
            status_code=400, detail={"code": 400, "message": "Bad Request"}
        )


@app.patch("/portfolios", response_model=PortfolioResponse)
def update_portfolio(
    uuid: UUID4 = Path(..., description="The UUID of the portfolio to be updated"),
    patch_data: PortfolioPatch = Body(..., example={"name": "Default"}),
):
    try:
        return {"code": 200, "message": "Ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": 400, "message": str(e)})
    except KeyError as e:
        raise HTTPException(status_code=404, detail={"code": 404, "message": str(e)})
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": "An unexpected error occurred."},
        )


@app.delete("/portfolios", response_model=PortfolioResponse)
def remove_portfolio(uuid: UUID4 = Path(...)):
    try:
        return {"code": 200, "message": "Ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": 400, "message": str(e)})
    except KeyError as e:
        raise HTTPException(status_code=404, detail={"code": 404, "message": str(e)})
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": "An unexpected error occurred."},
        )


# Additional endpoints for other operations can be added here
