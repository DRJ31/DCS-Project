from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from Model import Message, Contact


class ChatController:
    messages = {}
    contacts = [
        Contact("Nyaruko", "192.168.1.123"),
        Contact("Ritsuka", "192.168.1.122")
    ]
    test_arr = [
        Message("Nyaruko", "Hello, master!"),
        Message("Ritsuka", "Hello, Nyaruko!")
    ]
    current_user = None

    def __init__(self, ChatView):
        self.view = ChatView
        self.init_contacts()
        self.init_messages()

    def init_contacts(self):
        for contact in self.contacts:
            item = QListWidgetItem(QIcon('../assets/icon/%s.jpg' % contact.username), contact.username)
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
            item = QListWidgetItem(QIcon('../assets/icon/%s.jpg' % message.username), message.content)
            self.view.conversationList.addItem(item)
        self.view.conversationList.setIconSize(QSize(25, 25))

    def get_user_by_name(self, username):
        for contact in self.contacts:
            if contact.username == username:
                return contact
