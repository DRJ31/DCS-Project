import xmlrpc.client
from utils.Exceptions import FetchDataError


class Client:
    def __init__(self, username):
        self.username = username
        self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
        self.user_id = self.register()
        if not self.user_id:
            raise FetchDataError('Username or Password is invalid!')
        self.user_list = self.server.get_online_users()

    def register(self):

        try:
            user_id = self.server.regist_new_user(self.username)

        except:
            # TODO: Add an alert
            user_id = 0
        return user_id
