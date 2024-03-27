# @author: Alec Ibarra
# @description: Database class for handling database interactions


class Database(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def create_user(self, username: str, email: str, password_hash: str) -> bool:
        # check if user with email already exists
        # else create user
        pass
