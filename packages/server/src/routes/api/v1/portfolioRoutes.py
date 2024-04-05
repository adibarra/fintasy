from fastapi import FastAPI, HTTPException
from helpers.portfolio import Portfolio

app = FastAPI()
portfolio_manager = Portfolio()


@app.post("/portfolios/")
def add_portfolio(portfolio_name: str):
    try:
        is_valid = portfolio_manager.validate_portfolio_name(portfolio_name)
        if is_valid:
            return {"message": f"Portfolio {portfolio_name} added successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
