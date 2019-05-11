import socket


class Message:
    def __init__(self, username, content):
        self.username = username
        self.content = content


class Contact:
    def __init__(self, username, ip_addr, has_avatar):
        self.username = username
        self.ip_addr = ip_addr
        self.has_avatar = has_avatar

    @staticmethod
    def get_ip_addr():
        myname = socket.getfqdn(socket.gethostname())
        return socket.gethostbyname(myname)


class Model:
    test_arr = [  # Just for test
        Message("Nyaruko", "君の名前は？")
    ]

    def __init__(self):
        self.messages = {}  # All the message records
        self.contacts = [  # All the contacts
            Contact("Nyaruko", "192.168.1.123", True),
            Contact("Ritsuka", "192.168.1.122", False),
            Contact("KizunaAI", "192.168.1.120", True)
        ]
        self.current_user = None  # Current user you are talking with
        self.myself = self.contacts[2]  # Modify this as your account
        self.init_messages()

    def init_messages(self):
        for contact in self.contacts:
            if contact.username == "Nyaruko":
                self.messages[contact.username] = self.test_arr
            else:
                self.messages[contact.username] = []

    def send_message(self, content):
        self.messages[self.current_user.username].append(Message(self.myself.username, content))

    def change_contact(self, username):
        self.current_user = self.get_user_by_name(username)

    def get_user_by_name(self, username):
        for contact in self.contacts:
            if contact.username == username:
                return contact

    def add_contact(self, username, ip_addr):
        self.contacts.append(Contact(username, ip_addr, False))
        self.messages[username] = []

    def delete_contact(self, username):
        del self.messages[username]
        for contact in self.contacts:
            if contact.username == username:
                del contact
