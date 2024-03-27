# @author: Alec Ibarra (adibarra)
# @description: Test for the User class

import unittest

from src.helpers.user import User


class TestUserMethods(unittest.TestCase):
    def test_username_validation(self):
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_SHORT],
            User.validate_username,
            "",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_SHORT],
            User.validate_username,
            "12",
        )
        self.assertTrue(User.validate_username("123"))
        self.assertTrue(User.validate_username("12345678901234567890"))
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_LONG],
            User.validate_username,
            "123456789012345678901",
        )

    def test_password_validation(self):
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.PASSWORD_SHORT],
            User.validate_password,
            "",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.PASSWORD_SHORT],
            User.validate_password,
            "12345",
        )
        self.assertTrue(User.validate_password("123456"))
        self.assertTrue(User.validate_password("12345678901234567890"))

    def test_email_validation(self):
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validate_email,
            "",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validate_email,
            "test",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validate_email,
            "test@",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validate_email,
            "test@example",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validate_email,
            "test@example.",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validate_email,
            "@example.com",
        )
        self.assertTrue(User.validate_email("test@example.com"))

    def test_password_verification(self):
        test_password = "password"
        password_hash = User.hash_password(test_password)
        self.assertTrue(User.verify_password(test_password, password_hash))
        self.assertFalse(User.verify_password(test_password + "123", password_hash))


if __name__ == "__main__":
    unittest.main()
