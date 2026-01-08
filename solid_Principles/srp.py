# BAD: One class doing everything​
class User:
    def save_to_db(self): ...
    def send_email(self): ...


# GOOD: Sepxarate responsibilities​
class UserRepository:
    def save(self, user): ...


class EmailService:
    def send_welcome(self, user): ...
    