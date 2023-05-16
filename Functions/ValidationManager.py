from email_validator import validate_email, EmailNotValidError
from db.QueryManager import QueryManager
import re


class ValidationManager:
    def __init__(self, data):
        self.data = data

    def password_valid(self):
        password = self.data['password']
        repeat_password = self.data['repeat-password']

        pattern = r"^(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$"
        pattern = re.compile(pattern)

        if repeat_password != password:
            return False
        if not pattern.match(password):
            return False

        return True

    def email_valid(self):
        email = self.data['email']
        manager = QueryManager()
        existing_email = manager.exists_email(email)
        if existing_email:
            return False
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    def username_valid(self):

        pattern = r"^[a-zA-Z0-9]{6,}$"
        pattern = re.compile(pattern)

        username = self.data['new-user']

        if not pattern.match(username):
            return False

        manager = QueryManager()
        existing_username = manager.exists_username(username)
        if existing_username:
            return False

        return True

    def name_valid(self):

        pattern = r"^[A-Z][a-zA-Z]*(?: [A-Z][a-zA-Z]*)?$"
        pattern = re.compile(pattern)

        name = self.data['new-name']

        if not pattern.match(name):
            return False

        return True

    def all_valid(self):
        methods = [self.name_valid, self.password_valid,
                   self.email_valid, self.username_valid]

        for method in methods:
            if not method():
                return False

        return True
