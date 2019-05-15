class Message:
    def __init__(self, sender, receiver, content):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def serialize(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'content': self.content
        }
