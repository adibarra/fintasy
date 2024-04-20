# @authors: soltadd (Solomon Bedane), caleb-j-kim (Caleb Kim)
# @description: Tournaments class for handling paper trading tournaments betwen users.

from datetime import datetime
from enum import Enum

from helpers.portfolio import Portfolio


class Tournament:
    """
    Creates a new tournament with a name, duration, trading rules, and prizes.
    """

    TOURNAMENT_VALID_CHARACTERS = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#_ "
    )
    TOURNAMENT_LENGTH_MIN = 1
    TOURNAMENT_LENGTH_MAX = 20

    ERROR_TYPES = Enum(
        "ERROR_TYPES",
        [
            "PORTFOLIO_SHORT",
            "PORTFOLIO_LONG",
            "PORTFOLIO_INVALID_CHARACTERS",
            "PORTFOLIO_NAME_EXISTS",
        ],
    )

    ERROR_MESSAGES = {
        ERROR_TYPES.TOURNAMENT_SHORT: "Portfolio name must be at least 1 character long",
        ERROR_TYPES.TOURNAMENT_LONG: "Portfolio name must be less than or equal to 20 characters long",
        ERROR_TYPES.TOURNAMENT_INVALID_CHARACTERS: "Portfolio name must contain only valid characters",
        ERROR_TYPES.TOURNAMENT_NAME_EXISTS: "Portfolio name must be unique",
        ERROR_TYPES.TOURNAMENT_DATE_INVALID: "Start date must be before end date",
    }

    def validate_name(name: str) -> bool:
        if len(name) < Tournament.TOURNAMENT_LENGTH_MIN:
            raise ValueError(
                Tournament.ERROR_MESSAGES[Tournament.ERROR_TYPES.TOURNAMENT_SHORT]
            )

        if len(name) > Tournament.TOURNAMENT_LENGTH_MAX:
            raise ValueError(
                Tournament.ERROR_MESSAGES[Tournament.ERROR_TYPES.TOURNAMENT_LONG]
            )

        for char in name:
            if char not in Tournament.TOURNAMENT_VALID_CHARACTERS:
                raise ValueError(
                    Tournament.ERROR_MESSAGES[
                        Tournament.ERROR_TYPES.TOURNAMENT_INVALID_CHARACTERS
                    ]
                )
        return True

    def validate_dates(start_date: datetime, end_date: datetime) -> bool:
        if start_date > end_date:
            raise ValueError(
                Tournament.ERROR_MESSAGES[
                    Tournament.ERROR_TYPES.TOURNAMENT_DATE_INVALID
                ]
            )
        return True

    def __init__(self, name, duration, trading_rules, prizes):
        self.name = name
        self.duration = duration
        self.trading_rules = trading_rules
        self.prizes = prizes
        self.participants = []

    """
    Adds a participant to this tournament.
    """

    def add_participant(self, participant, price):
        if price > participant.portfolio.balance:
            raise ValueError(f"{participant} does not have enough money to join")
        self.participants.append(self.Participant(participant, Portfolio(), price))

    """
    Displays the leaderboard for this tournament.
    """

    def display_leaderboard(self):
        sorted_participants = sorted(
            self.participants, key=lambda x: x.portfolio.value, reverse=True
        )
        print("Leaderboard for", self.name)
        for i, participant in enumerate(sorted_participants, start=1):
            earnings = participant.portfolio.value - participant.price
            print(f"{i}. {participant.user.name}: ${earnings}")

    def set_prize_money(self, earnings: int):
        self.prizes = earnings

    def set_placements(self):
        sorted_participants = sorted(
            self.participants, key=lambda x: x.portfolio.value, reverse=True
        )
        for i, participant in enumerate(sorted_participants, start=1):
            participant.place = i

    def set_duration(self, duration: datetime):
        duration = (duration, "%m %d %Y")
        self.duration = duration

    def set_tournament_name(self, name: str):
        TOURNAMENT_VALID_CHARACTERS = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        )
        TOURNAMENT_LENGTH_MIN = 1
        TOURNAMENT_LENGTH_MAX = 20

        ERROR_TYPES = Enum(
            "ERROR_TYPES",
            [
                "PORTFOLIO_SHORT",
                "PORTFOLIO_LONG",
                "PORTFOLIO_INVALID_CHARACTERS",
                "PORTFOLIO_NAME_EXISTS",
            ],
        )

        ERROR_MESSAGES = {
            ERROR_TYPES.TOURNAMENT_SHORT: "Portfolio name must be at least 1 character long",
            ERROR_TYPES.TOURNAMENT_LONG: "Portfolio name must be less than or equal to 20 characters long",
            ERROR_TYPES.TOURNAMENT_INVALID_CHARACTERS: "Portfolio name must contain only valid characters",
            ERROR_TYPES.TOURNAMENT_NAME_EXISTS: "Portfolio name must be unique",
        }

        if len(name) < TOURNAMENT_LENGTH_MIN:
            raise ValueError(ERROR_MESSAGES[ERROR_TYPES.TOURNAMENT_SHORT])

        if len(name) > TOURNAMENT_LENGTH_MAX:
            raise ValueError(ERROR_MESSAGES[ERROR_TYPES.TOURNAMENT_LONG])

        for char in name:
            if char not in TOURNAMENT_VALID_CHARACTERS:
                raise ValueError(
                    ERROR_MESSAGES[ERROR_TYPES.TOURNAMENT_INVALID_CHARACTERS]
                )

        self.name = name

    def ticker(self):
        time_left = datetime.now() - self.duration
        if time_left > 0:
            return True
        return False

    def registration_deadline(
        self, minimum_participants: int, maximum_participants: int
    ):
        while self.ticker():
            # print("Registration is open. Please join this tournament!")
            if len(self.participants) == maximum_participants:
                print(
                    "Lobby if full. \nPlease wait for the next tournament or for someone to leave this tournament."
                )

        if len(self.participants) < minimum_participants:
            raise ValueError(
                f"Not enough participants to start the tournament.\n{self.name} will be cancelled."
            )

    def tournament_duration(self):
        while self.ticker():
            # print("Tournament is in progress. Please make your trades!")
            pass
        print("Tournament is over. Calculating winners...")

    def distribute_prizes(self, participant):
        first_place = self.prizes
        second_place = self.prizes / 2
        third_place = self.prizes / 4
        fourth_place = self.prizes / 8

        if participant.place == 1:
            participant.user.balance += first_place
        elif participant.place == 2:
            participant.user.balance += second_place
        elif participant.place == 3:
            participant.user.balance += third_place
        elif participant.place == 4:
            participant.user.balance += fourth_place

    """
    Inner class used to keep track of participants in a tournament.
    """

    class Participant:
        def __init__(self, user, portfolio):
            self.user = user
            self.portfolio = portfolio
            self.place = ""

    """
    Makes a trade betwen 2 users.
    """

    def make_trade(self, participant1, participant2):
        if participant1 not in self.participants:
            raise ValueError(f"{participant1} is not in this tournament")
        if participant2 not in self.participants:
            raise ValueError(f"{participant1} is not in this tournament")
