# @authors: omer8 (Omer Siddiqui)
# @description: SessionController class for user authentication and session management

import secrets
import string
from collections import defaultdict

seshTokenToUUID = defaultdict(str)


class SessionController:
    """Session Controller:
    Receives username and email from the user and returns session token
    """

    def generate_session_token(length=32):
        """Generate a random session token."""
        characters = string.ascii_letters + string.digits
        session_token = "".join(secrets.choice(characters) for _ in range(length))
        return session_token

    def authenticate_user(email, password):
        """Authenticate user and return session token and UUID if valid."""
        # Implement logic that validates a user, by retrieving
        # uuid with username and password. Update validCredentials
        validCredentials = True  # Placeholder value

        if validCredentials:
            # Authentication successful, generate session token
            session_token = SessionController.generate_session_token()
            uuid = "d383865a-df45-4c4c-bc47-b06253b126a6"  # Placeholder value
            return session_token, uuid
        else:
            # Authentication failed
            print("Authentication failed. Please check your credentials.")
            return None, None

    def login(email, password):
        """Login user and return session token if authenticated."""
        # Authenticate user
        token, uuid = SessionController.authenticate_user(email, password)
        if token:
            # Add sessionToken to sessionTokenToUUID Map
            seshTokenToUUID[session_token] = uuid
            return token
        else:
            print("Login Failed. Please try again.")
            return None
