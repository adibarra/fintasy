# @author: adibarra (Alec Ibarra)
# @description: Example test

import unittest


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("test".upper(), "TEST")


if __name__ == "__main__":
    unittest.main()
