from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

from Model import Message, Contact


class ChatController:
    messages = {}  # All the message records
    contacts = [  # All the contacts
        Contact("Nyaruko", "192.168.1.123", True),
        Contact("Ritsuka", "192.168.1.122", False),
        Contact("KizunaAI", "192.168.1.120", True)
    ]
    current_user = None  # Current user you are talking with
    myself = contacts[2]  # Modify this as your account

    test_arr = [  # Just for test
        Message("Nyaruko", "君の名前は？")
    ]

    def __init__(self, ChatView):
        self.view = ChatView
        self.init_contacts()
        self.init_messages()

    @staticmethod
    def get_username(text):
        return text.split('\n')[0]

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

    def get_messages(self, username):
        for message in self.messages[username]:
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

    def delete_contact(self):
        items = self.view.contactList.selectedItems()
        for item in items:
            username = self.get_username(item.text())
            if username != self.myself.username:
                result = QMessageBox.warning(QMessageBox(), 'Are you sure?',
                                             'You will permanently delete all the records with %s.' % username,
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if result == QMessageBox.Yes:
                    self.view.contactList.takeItem(self.view.contactList.row(item))
                    self.change_contact(self.view.contactList.selectedItems()[0])
                    del self.messages[username]
                    for contact in self.contacts:
                        if contact.username == username:
                            del contact

    def save_info(self, username, ip_addr):
        contact = Contact(username, ip_addr, False)
        self.contacts.append(contact)
        self.messages[contact.username] = []
        item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), contact.username + '\n' + contact.ip_addr)
        self.view.contactList.addItem(item)

    def change_contact(self, item):
        username = self.get_username(item.text())
        self.view.sendButton.setDisabled(False)
        self.view.conversationList.clear()
        self.get_messages(username)
        self.current_user = self.get_user_by_name(username)

    def get_avatar(self):
        myself = self.myself
        if myself.has_avatar:
            return QPixmap('../assets/avatar/%s.jpg' % myself.username).scaled(40, 40)
        return QPixmap('../assets/avatar/default.jpg').scaled(40, 40)

    def send_message(self):
        content = self.view.textEdit.toPlainText()
        myself = self.myself
        self.messages[self.current_user.username].append(Message(myself.username, content))
        if self.myself.has_avatar:
            item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % myself.username), content)
        else:
            item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), content)
        self.view.conversationList.addItem(item)
        self.view.textEdit.clear()
