import csv

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class UserManager:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open(self.credentials_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    users.append(User(row['username'], row['password'], row['role']))
        except FileNotFoundError:
            print(f"Credentials file '{self.credentials_file}' not found.")
        return users

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None
