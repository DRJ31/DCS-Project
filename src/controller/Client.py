import xmlrpc.client
from utils.Exceptions import FetchDataError


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
        self.user_id = self.register()
        if self.user_id == -1:
            raise FetchDataError('Username or Password is invalid!')
        self.user_list = self.server.get_online_users()

    def register(self):

        try:
            user_id = self.server.regist_new_user(self.username, self.password)
            if not user_id:
                user_id = -1
        except:
            user_id = -1
        return user_id
