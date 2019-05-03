class Message:
    def __init__(self, username, content):
        self.username = username
        self.content = content


class Contact:
    def __init__(self, username, ip_addr, has_avatar):
        self.username = username
        self.ip_addr = ip_addr
        self.has_avatar = has_avatar

