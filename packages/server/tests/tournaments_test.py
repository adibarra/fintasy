import unittest


# Function to simulate user joining tournament
def join_tournament(user_finbucks, tournament_cost):
    if user_finbucks >= tournament_cost:
        return "User joins tournament"
    else:
        raise ValueError("Insufficient FinBucks")


class TestJoinTournament(unittest.TestCase):
    def test_valid_more_than(self):
        # Arrange
        user_finbucks = 700
        tournament_cost = 50

        # Act
        outcome = join_tournament(user_finbucks, tournament_cost)

        # Assert
        self.assertEqual(outcome, "User joins tournament")

    def test_valid_exact(self):
        # Arrange
        user_finbucks = 50
        tournament_cost = 50

        # Act
        outcome = join_tournament(user_finbucks, tournament_cost)

        # Assert
        self.assertEqual(outcome, "User joins tournament")

    def test_invalid_less_than(self):
        # Arrange
        user_finbucks = 49
        tournament_cost = 50

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            join_tournament(user_finbucks, tournament_cost)
        self.assertEqual(str(context.exception), "Insufficient FinBucks")


if __name__ == "__main__":
    unittest.main()
