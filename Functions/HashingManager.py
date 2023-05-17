from passlib.hash import pbkdf2_sha256


class HashingManager:
    def __init__(self, password):
        self.data = {}
        hashed = pbkdf2_sha256.encrypt(password, rounds=10000, salt_size=16)

        self.data["password"] = hashed

    @staticmethod
    def is_valid_password(password, hashed):
        is_match = pbkdf2_sha256.verify(password, hashed)
        return is_match

    def get_data(self):
        return self.data
