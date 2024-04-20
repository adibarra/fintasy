# @author: adibarra (Alec Ibarra), caleb-j-kim (Caleb Kim)
# @description: Portfolio routes for the API

from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, status
from helpers.tournament import Tournament
from pydantic import UUID4, BaseModel
from services.database import Database

db = Database()
router = APIRouter(prefix="/api/v1")


class TournamentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    ONGOING = "ONGOING"
    FINISHED = "FINISHED"


class TournamentData(BaseModel):
    uuid: UUID4
    owner: UUID4
    name: str
    status: TournamentStatus
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime


class CreateTournamentRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime


class UpdateTournamentRequest(BaseModel):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        exclude_none = True


class TournamentResponse(BaseModel):
    code: int
    message: str
    data: Optional[TournamentData] = None

    class Config:
        exclude_none = True


class TournamentsResponse(BaseModel):
    code: int
    message: str
    data: Optional[List[TournamentData]] = None

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
    tournament_uuid: UUID4 = Path(...),
) -> tuple[str, str]:
    token_owner, token = await authenticateToken(authorization)

    tournament = db.get_tournament(str(tournament_uuid))
    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    # Validate the token has permission for this resource
    if str(token_owner) != str(tournament["owner"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return token_owner, token


@router.post(
    "/tournaments",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def create_tournament(
    data: CreateTournamentRequest = Body(...),
    auth: tuple[str, str] = Depends(authenticateToken),
):
    try:
        Tournament.validate_name(data.name)
        Tournament.validate_dates(data.start_date, data.end_date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    tournaments = db.create_tournament(
        auth[0], data.name, data.start_date, data.end_date
    )
    return TournamentResponse(
        code=200,
        message="Ok",
        data=tournaments,
    )


@router.get(
    "/tournaments",
    response_model=TournamentsResponse,
    status_code=status.HTTP_200_OK,
)
def get_tournaments(
    name: str = None,
    owner: UUID4 = None,
    status: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    offset: int = 0,
    limit: int = 10,
    auth: tuple[str, str] = Depends(authenticateToken),
):
    tournaments = db.get_tournaments(
        owner=str(owner) if owner else None,
        name=name,
        status=status,
        start_date=start_date,
        end_date=end_date,
        offset=offset,
        limit=limit,
    )
    return TournamentsResponse(
        code=200,
        message="Ok",
        data=tournaments,
    )


@router.get(
    "/tournaments/{tournament_uuid}",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def get_tournament(
    tournament_uuid: UUID4 = Path(...),
    auth: tuple[str, str] = Depends(authenticateToken),
):
    tournament = db.get_tournament(str(tournament_uuid))
    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )
    return TournamentResponse(
        code=200,
        message="Ok",
        data=tournament,
    )


@router.patch(
    "/tournaments/{tournament_uuid}",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def update_tournament(
    tournament_uuid: UUID4 = Path(...),
    data: UpdateTournamentRequest = Body(...),
    auth: tuple[str, str] = Depends(authenticate),
):
    try:
        Tournament.validate_name(data.name)
        Tournament.validate_dates(data.start_date, data.end_date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    tournament = db.get_tournament(str(tournament_uuid))
    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    if not db.update_tournament(
        str(tournament_uuid), data.name, data.start_date, data.end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return TournamentResponse(
        code=200,
        message="Ok",
    )


@router.delete(
    "/tournaments/{tournament_uuid}",
    response_model=TournamentResponse,
    status_code=status.HTTP_200_OK,
)
def delete_tournament(
    tournament_uuid: UUID4 = Path(...),
    auth: tuple[str, str] = Depends(authenticate),
):
    tournaments = db.get_tournament(str(tournament_uuid))
    if tournaments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    if not db.delete_tournament(str(tournament_uuid)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return TournamentResponse(
        code=200,
        message="Ok",
    )
