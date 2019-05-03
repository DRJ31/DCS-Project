from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from Model import Message, Contact


class ChatController:
    messages = {}
    contacts = [
        Contact("Nyaruko", "192.168.1.123", True),
        Contact("Ritsuka", "192.168.1.122", False),
        Contact("KizunaAI", "192.168.1.120", True)
    ]
    test_arr = [
        Message("Nyaruko", "真尋さん大好き！"),
    ]
    current_user = None
    myself = contacts[2]

    def __init__(self, ChatView):
        self.view = ChatView
        self.init_contacts()
        self.init_messages()

    def init_contacts(self):
        for contact in self.contacts:
            if contact.has_avatar:
                item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % contact.username), contact.username + "\n" + contact.ip_addr)
            else:
                item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), contact.username + "\n" + contact.ip_addr)
            self.view.contactList.addItem(item)
        self.view.contactList.setIconSize(QSize(25, 25))

    def init_messages(self):
        for contact in self.contacts:
            if contact.username == "Nyaruko":
                self.messages[contact.username] = self.test_arr
            else:
                self.messages[contact.username] = []

    def get_messages(self, contact):
        for message in self.messages[contact]:
            if self.get_user_by_name(message.username).has_avatar:
                item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % message.username), message.content)
            else:
                item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), message.content)
            self.view.conversationList.addItem(item)
        self.view.conversationList.setIconSize(QSize(25, 25))

    def get_user_by_name(self, username):
        for contact in self.contacts:
            if contact.username == username:
                return contact

    def delete_contact(self, username):
        del self.messages[username]
        for contact in self.contacts:
            if contact.username == username:
                del contact
