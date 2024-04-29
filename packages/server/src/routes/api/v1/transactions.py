# @author: adibarra (Alec Ibarra)
# @description: Transaction routes for the API

from datetime import datetime
from typing import List, Literal, Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
from pydantic import UUID4, BaseModel
from services.alpaca import AlpacaService
from services.database import Database

db = Database()
router = APIRouter(prefix="/api/v1")


class CreateTransactionRequest(BaseModel):
    portfolio: UUID4
    symbol: str
    action: Literal["BUY", "SELL"]
    quantity: int


class TransactionData(BaseModel):
    uuid: UUID4
    portfolio: UUID4
    symbol: str
    action: Literal["BUY", "SELL"]
    quantity: int
    price_cents: int
    created_at: datetime


class TransactionResponse(BaseModel):
    code: int
    message: str
    data: Optional[TransactionData] = None

    class Config:
        exclude_none = True


class TransactionsResponse(BaseModel):
    code: int
    message: str
    data: Optional[List[TransactionData]] = None

    class Config:
        exclude_none = True


async def authenticateToken(
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


async def authenticate(
    authorization: str = Header(...),
    transaction_uuid: UUID4 = Path(...),
) -> tuple[str, str]:
    token_owner, token = await authenticateToken(authorization)

    # Validate the token has permission for this user's transactions
    transaction = db.get_transaction_by_uuid(str(transaction_uuid))
    portfolio = db.get_portfolio(str(transaction["portfolio"]))
    if token_owner != str(portfolio["owner"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return token_owner, token


@router.post(
    "/transactions", response_model=TransactionResponse, status_code=status.HTTP_200_OK
)
def create_transaction(
    data: CreateTransactionRequest = Body(...),
    auth: tuple[str, str] = Depends(authenticateToken),
):
    token_owner = auth[0]

    # check if the portfolio exists
    portfolio = db.get_portfolio(str(data.portfolio))
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    # check if the user owns the portfolio
    if portfolio["owner"] != token_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    # check if quantity is valid
    if data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    # get the stock quote
    quote = AlpacaService.get_quote(data.symbol)
    if quote is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    # check if the user can do the transaction
    if data.action == "BUY":
        # check if the user has enough funds to buy the stock
        new_balance = portfolio["balance_cents"] - (
            quote["price_cents"] * data.quantity
        )
        if new_balance < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request",
            )

        # update the portfolio balance
        if not db.update_portfolio_balance(portfolio["uuid"], new_balance):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )

    else:
        # check if the user has enough stocks to sell
        transactions = db.get_transactions(portfolio["uuid"], 0, 9999)
        if transactions is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )

        # calculate the user's stock quantity
        stock_quantity = 0
        for transaction in transactions:
            if transaction["symbol"] == data.symbol:
                if transaction["action"] == "BUY":
                    stock_quantity += transaction["quantity"]
                else:
                    stock_quantity -= transaction["quantity"]

        # check if the user has enough stocks to sell
        if stock_quantity < data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request",
            )

        # calculate the new balance
        new_balance = portfolio["balance_cents"] + (
            quote["price_cents"] * data.quantity
        )

        # update the portfolio balance
        if not db.update_portfolio_balance(portfolio["uuid"], new_balance):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )

    # attempt creating transaction
    transaction = db.create_transaction(
        uuid_portfolio=str(data.portfolio),
        symbol=data.symbol,
        action=data.action,
        quantity=data.quantity,
        price_cents=int(quote["price_cents"]) * data.quantity,
    )
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return TransactionResponse(
        code=200,
        message="Ok",
        data=transaction,
    )


@router.get(
    "/transactions",
    response_model=TransactionsResponse,
    status_code=status.HTTP_200_OK,
)
def get_transactions(
    portfolio: UUID4,
    offset: int = 0,
    limit: int = 10,
    auth: tuple[str, str] = Depends(authenticateToken),
):
    token_owner = auth[0]

    # Keep the user from accessing another user's transactions
    # Fix by adding a more granular permission system later
    portfolio_obj = db.get_portfolio(str(portfolio))
    if token_owner != str(portfolio_obj["owner"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    # Attempt getting transactions
    transactions = db.get_transactions(str(portfolio), offset, limit)
    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return TransactionsResponse(
        code=200,
        message="Ok",
        data=transactions,
    )


@router.get(
    "/transactions/{transaction_uuid}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def get_transaction_by_id(
    transaction_uuid: UUID4 = Path(...),
    auth: tuple[str, str] = Depends(authenticate),
):
    # Attempt getting transaction
    transaction = db.get_transaction_by_uuid(str(transaction_uuid))
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return TransactionResponse(
        code=200,
        message="Ok",
        data=transaction,
    )
