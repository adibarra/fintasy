# @authors: omer8 (Omer Siddiqui)
# @description: Testcases for the SessionController class

import unittest

from src.helpers.sessions import SessionController


class TestSessionController(unittest.TestCase):
    def test_generate_session_token(self):
        """Test generating a session token"""

        generated_token = SessionController.generate_session_token()
        self.assertIsNotNone(generated_token)

    def test_authenticate_valid_user(self):
        """Test authenticating a valid user"""

        email = "valid@example.com"
        password = "valid123"
        token, uuid = SessionController.authenticate_user(email, password)
        self.assertIsNotNone(token)
        self.assertIsNotNone(uuid)

    def test_authenticate_invalid_user(self):
        """Test authentication for invalid user"""

        email = "invalid@example.com"
        password = "invalid123"
        token, uuid = SessionController.authenticate_user(email, password)
        self.assertIsNone(token)
        self.assertIsNone(uuid)

    def test_valid_login(self):
        """Test logging in a user with valid credentials"""

        email = "valid@example.com"
        password = "valid123"
        session_token = SessionController.login(email, password)
        self.assertIsNotNone(session_token)

    ""

    def test_invalid_login(self):
        """Test logging in a user with invalid credentials"""

        email = "invalid@example.com"
        password = "abc12345678"
        session_token = SessionController.login(email, password)
        self.assertIsNone(session_token)


if __name__ == "__main__":
    unittest.main()
