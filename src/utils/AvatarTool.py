import xmlrpc.client
from os import path


def check_avatar(username):
    status = path.exists('../assets/avatar/%s.jpg' % username)
    if not status:
        server = xmlrpc.client.ServerProxy('http://120.77.38.66:8015')
        with open('../assets/avatar/%s.jpg' % username, 'wb') as f:
            f.write(server.get_avatar(username).data)
            f.close()