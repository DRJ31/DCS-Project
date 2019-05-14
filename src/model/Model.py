class Model:

    def __init__(self):
        self.messages = {}  # All the message records
        self.contacts = []  # All the contacts
        self.current_user = None  # Current user you are talking with
        self.myself = None

    # Initialize functions
    def init_self(self, user_list):
        self.myself = user_list[-1]
        self.contacts = user_list

    def init_messages(self):
        for contact in self.contacts:
            self.messages[contact.user_id] = []

    # Model changes in GUI actions
    def send_message(self, content):
        if self.myself['user_id'] != self.current_user['user_id']:
            self.messages[self.current_user['user_id']].append({
                'sender': self.myself['user_id'],
                'receiver': self.current_user['user_id'],
                'content': content
            })

    def change_contact(self, user_id):
        self.current_user = self.get_user_by_id(user_id)

    def add_contact(self, user_id, username, avatar):
        self.contacts.append({
            'user_id': user_id,
            'username': username,
            'avatar': avatar
        })
        self.messages[int(user_id)] = []

    def delete_contact(self, user_id):
        del self.messages[int(user_id)]
        for contact in self.contacts:
            if contact['user_id'] == user_id:
                del contact

    # Get information from model
    def get_user_by_id(self, user_id):
        for contact in self.contacts:
            if contact['user_id'] == user_id:
                return contact

    def get_user_id_by_name(self, username):
        for contact in self.contacts:
            if contact['username'] == username:
                return contact['user_id']
