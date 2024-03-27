# @author: Alec Ibarra (adibarra)
# @description: User class for handling users

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

    def createUser(username: str, email: str, password: str) -> str:
        """
        Create a new user with the given username, email, and password and store it in the database.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            str: The UUID of the newly created user.
        """

        User.validateUsername(username)
        User.validateEmail(email)
        User.validatePassword(password)
        passwordHash = User.hashPassword(password)  # noqa: F841

        # database query to create user with username, email, passwordHash
        # database should automatically populate uuid, coins, createdAt, updatedAt

        uuid = "123"  # from database after creation

        return uuid

    def validateUsername(username: str) -> bool:
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

    def validateEmail(email: str) -> bool:
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

    def validatePassword(password: str) -> bool:
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

    def hashPassword(password: str) -> str:
        """
        Hashes the given password.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """

        return ph.hash(password)

    def verifyPassword(password: str, passwordHash: str) -> bool:
        """
        Verifies if the given password matches the password hash.

        Args:
            password (str): The password to be verified.
            passwordHash (str): The password hash to compare against.

        Returns:
            bool: True if the password matches the password hash, False otherwise.
        """

        try:
            ph.verify(passwordHash, password)
            return True
        except:  # noqa: E722
            return False
