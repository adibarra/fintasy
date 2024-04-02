# @author: Brenden Zacek (tenorsine), Solomon Bedane
# @description: Tournaments class for handling paper trading tournaments betwen users.

from datetime import datetime

from portfolio import Portfolio
from transactions import Transaction


class Tournament:
    """
    Creates a new tournament with a name, duration, trading rules, and prizes.
    """

    def __init__(self, name, duration, trading_rules, prizes):
        self.name = name
        self.duration = duration
        self.trading_rules = trading_rules
        self.prizes = prizes
        self.participants = []

    """
    Adds a participant to this tournament.
    """

    def add_participant(self, participant):
        self.participants.append(self.Participant(participant, Portfolio()))

    """
    Displays the leaderboard for this tournament.
    """

    def display_leaderboard(self):
        sorted_participants = sorted(
            self.participants, key=lambda x: x.portfolio.value, reverse=True
        )
        print("Leaderboard for", self.name)
        for i, participant in enumerate(sorted_participants, start=1):
            print(f"{i}. {participant.user.name}: ${participant.portfolio.value}")

    """
    Inner class used to keep track of participants in a tournament.
    """

    class Participant:
        def __init__(self, user, portfolio):
            self.user = user
            self.portfolio = portfolio

    """
    Makes a trade betwen 2 users.
    """

    def make_trade(self, participant1, participant2):
        if participant1 not in self.participants:
            raise ValueError(f"{participant1} is not in this tournament")
        if participant2 not in self.participants:
            raise ValueError(f"{participant1} is not in this tournament")
        # To be replaced later
        do_transaction()


# Example usage
if __name__ == "__main__":
    # Create a new tournament
    trading_rules = {
        "stocks": True,
        "ETFs": True,
        "short_selling": True,
        "options_trading": True,
        "margin_trading": True,
        "max_leverage": 2,
    }
    prizes = {"first_place": "Virtual Trophy", "second_place": "Honorable Mention"}
    fintasy_challenge = Tournament(
        "Fintasy Paper Trade Challenge", "3 months", 100000, trading_rules, prizes
    )

    # Add participants (these would be User objects and not strings)
    participant1 = "Alec Daniel"
    participant2 = "Solomon Bedaine"
    participant3 = "Brenden Zacek"

    fintasy_challenge.add_participant(participant1)
    fintasy_challenge.add_participant(participant2)
    fintasy_challenge.add_participant(participant3)

    # Display leaderboard
    fintasy_challenge.display_leaderboard()
