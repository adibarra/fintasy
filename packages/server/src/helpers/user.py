# @author: adibarra (Alec Ibarra)
# @description: User class for handling user validation and password hashing.

import re
from enum import Enum

from argon2 import PasswordHasher

ph = PasswordHasher()


class User:
    """
    Represents a user in the system.

    Attributes:
        ERROR_TYPES (enum.Enum): Enumerated type for different error types.
        ERROR_MESSAGES (dict): Dictionary mapping error types to error messages.
    """

    EMAIL_REGEX = re.compile(r"^[\w\-\.]+@(?:[\w-]+\.)+[\w-]{2,}$")
    USERNAME_VALID_CHARACTERS = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    )
    USERNAME_LENGTH_MIN = 3
    USERNAME_LENGTH_MAX = 20
    PASSWORD_LENGTH_MIN = 6

    ERROR_TYPES = Enum(
        "ERROR_TYPES",
        [
            "USERNAME_SHORT",
            "USERNAME_LONG",
            "USERNAME_INVALID_CHARACTERS",
            "EMAIL_INVALID",
            "PASSWORD_SHORT",
        ],
    )
    ERROR_MESSAGES = {
        ERROR_TYPES.EMAIL_INVALID: "Invalid email address",
        ERROR_TYPES.USERNAME_SHORT: "Username must be at least 3 characters long",
        ERROR_TYPES.USERNAME_LONG: "Username must be at most 20 characters long",
        ERROR_TYPES.USERNAME_INVALID_CHARACTERS: "Username can only contain letters, numbers, and underscores",
        ERROR_TYPES.PASSWORD_SHORT: "Password must be at least 6 characters long",
    }

    def validate_username(username: str) -> bool:
        """
        Validates the given username.

        Args:
            username (str): The username to be validated.

        Returns:
            bool: True if the username is valid, False otherwise.

        Raises:
            ValueError: If the username is too short, too long, or contains invalid characters.
        """

        if len(username) < User.USERNAME_LENGTH_MIN:
            raise ValueError(User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_SHORT])

        if len(username) > User.USERNAME_LENGTH_MAX:
            raise ValueError(User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_LONG])

        for char in username:
            if char not in User.USERNAME_VALID_CHARACTERS:
                raise ValueError(
                    User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_INVALID_CHARACTERS]
                )

        return True

    def validate_email(email: str) -> bool:
        """
        Validates if the given email address is in a valid format.

        Args:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email is in a valid format, False otherwise.

        Raises:
            ValueError: If the email address is not in a valid format.
        """

        if User.EMAIL_REGEX.match(email) is None:
            raise ValueError(User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID])

        return True

    def validate_password(password: str) -> bool:
        """
        Validates the given password.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: True if the password is valid, False otherwise.

        Raises:
            ValueError: If the password is too short.
        """

        if len(password) < User.PASSWORD_LENGTH_MIN:
            raise ValueError(User.ERROR_MESSAGES[User.ERROR_TYPES.PASSWORD_SHORT])

        return True

    def hash_password(password: str) -> str:
        """
        Hashes the given password.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """

        return ph.hash(password)

    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verifies if the given password matches the password hash.

        Args:
            password (str): The password to be verified.
            password_hash (str): The password hash to compare against.

        Returns:
            bool: True if the password matches the password hash, False otherwise.
        """

        try:
            ph.verify(password_hash, password)
            return True
        except:  # noqa: E722
            return False
