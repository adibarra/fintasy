# @author: Caleb Kim (caleb-j-kim)
# @description: Portfolio routes for the API

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import UUID4, BaseModel
from src.helpers.portfolio import Portfolio


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


class PortfolioResponse(BaseModel):
    code: int
    message: str
    data: PortfolioData


class ErrorResponse(BaseModel):
    code: int
    message: str


app = FastAPI()
portfolio_manager = Portfolio()


@app.post("/portfolios/{tournament}", response_model=PortfolioResponse)
def add_portfolio(
    tournament: UUID4 = Path(...),
    portfolio: PortfolioInput = None,
    expand: Optional[bool] = Query(False, descriptionn=""),
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

        return PortfolioResponse(code=200, message="Ok", data=portfolio_data)
    except ValueError:
        raise HTTPException(
            status_code=400, detail={"code": 400, "message": "Bad Request"}
        )


@app.get("/portfolios/")
def list_portfolios():
    return portfolio_manager.list_portfolios()


@app.get("/portfolios")
def get_portfolio(portfolio_name: str):
    return portfolio_manager.get_portfolio()


@app.patch("/portfolios")
def add_data(
    portfolio_name: str,
    company_name: str,
    qty: int,
    unit_price: int,
    daily_PL: int,
    total_PL: int,
):
    try:
        result = portfolio_manager.add_data(
            portfolio_name, company_name, qty, unit_price, daily_PL, total_PL
        )
        if result:
            return {
                "message": f"Data added/updated successfully for portfolio {portfolio_name}."
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@app.delete("/portfolios")
def remove_portfolio(portfolio_name):
    try:
        return {"message": f"Portfolio '{portfolio_name}' was successfully deleted."}
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Portfolio '{portfolio_name}' not found."
        )
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Additional endpoints for other operations can be added here
