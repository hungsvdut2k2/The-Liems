from pyrebase.pyrebase import Database


class UserDatabase:
    def __init__(self, database: Database) -> None:
        self.users = [user for user in database.child('users').get().each()]

    def get_all_emails(self):
        return [email for email in self.users['email']]
