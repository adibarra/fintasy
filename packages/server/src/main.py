# @author: adibarra (Alec Ibarra)
# @description: The main entry point for the server.

import uvicorn
from config import API_CORS_ORIGINS, API_HOST, API_PORT
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from routes.api.v1.portfolios import router as portfolios_router
from routes.api.v1.quotes import router as quotes_router
from routes.api.v1.sessions import router as sessions_router
from routes.api.v1.tournaments import router as tournaments_router
from routes.api.v1.transactions import router as transactions_router
from routes.api.v1.users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail},
    )


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": 400, "message": "Bad Request"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail},
    )


app.include_router(sessions_router)
app.include_router(users_router)
app.include_router(quotes_router)
app.include_router(portfolios_router)
app.include_router(transactions_router)
app.include_router(tournaments_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
    )
