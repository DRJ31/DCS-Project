class Contact:
    def __init__(self, user_id, username, avatar):
        self.user_id = user_id
        self.username = username
        self.avatar = avatar

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'avatar': self.avatar
        }
