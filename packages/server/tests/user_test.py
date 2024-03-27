# @author: Alec Ibarra (adibarra)
# @description: Test for the User class

import unittest

from src.classes.user import User


class TestUserMethods(unittest.TestCase):
    def test_username_validation(self):
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_SHORT],
            User.validateUsername,
            "",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_SHORT],
            User.validateUsername,
            "12",
        )
        self.assertTrue(User.validateUsername("123"))
        self.assertTrue(User.validateUsername("12345678901234567890"))
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.USERNAME_LONG],
            User.validateUsername,
            "123456789012345678901",
        )

    def test_password_validation(self):
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.PASSWORD_SHORT],
            User.validatePassword,
            "",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.PASSWORD_SHORT],
            User.validatePassword,
            "12345",
        )
        self.assertTrue(User.validatePassword("123456"))
        self.assertTrue(User.validatePassword("12345678901234567890"))

    def test_email_validation(self):
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validateEmail,
            "",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validateEmail,
            "test",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validateEmail,
            "test@",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validateEmail,
            "test@example",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validateEmail,
            "test@example.",
        )
        self.assertRaisesRegex(
            ValueError,
            User.ERROR_MESSAGES[User.ERROR_TYPES.EMAIL_INVALID],
            User.validateEmail,
            "@example.com",
        )
        self.assertTrue(User.validateEmail("test@example.com"))

    def test_password_verification(self):
        test_password = "password"
        passwordHash = User.hashPassword(test_password)
        self.assertTrue(User.verifyPassword(test_password, passwordHash))
        self.assertFalse(User.verifyPassword(test_password + "123", passwordHash))


if __name__ == "__main__":
    unittest.main()
