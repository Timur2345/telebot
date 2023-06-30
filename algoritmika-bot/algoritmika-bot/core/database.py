from os.path import join, exists
import json


class Database():
    def __init__(self, fileName: str) -> None:
        self.filePath = join('data', fileName)
        if not exists(self.filePath):
            self.write_users({})

    def load_users(self) -> dict:
        with open(self.filePath, 'r') as file:
            return json.load(file)

    def write_users(self, data: dict) -> None:
        with open(self.filePath, 'w') as file:
            json.dump(data, file)

    def user_exists(self, userId: int) -> bool:
        users = self.load_users()
        return str(userId) in users

    def create_user(self, userId: int) -> None:
        users = self.load_users()
        users[str(userId)] = {
            'state': None,
            'nineLivesPoints': 0,
            'nineLivesHealth': 0,
            'nineLivesWord': None
        }
        self.write_users(users)

    def get_user(self, userId: int) -> dict:
        users = self.load_users()
        return users.get(str(userId), {})

    def update_user(self, userId: int, **kwargs) -> None:
        users = self.load_users()
        users[str(userId)].update(kwargs)
        self.write_users(users)
