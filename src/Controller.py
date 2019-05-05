from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

from Model import Message, Contact


class ChatController:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.init_contacts()

    @staticmethod
    def get_username(text):
        return text.split('\n')[0]

    def setup_view_action(self):
        view = self.view

    def init_contacts(self):
        for contact in self.model.contacts:
            if contact.has_avatar:
                item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % contact.username), contact.username + "\n" + contact.ip_addr)
            else:
                item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), contact.username + "\n" + contact.ip_addr)
            self.view.contactList.addItem(item)
        self.view.contactList.setIconSize(QSize(25, 25))

    def get_messages(self, username):
        for message in self.model.messages[username]:
            if self.model.get_user_by_name(message.username).has_avatar:
                item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % message.username), message.content)
            else:
                item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), message.content)
            self.view.conversationList.addItem(item)
        self.view.conversationList.setIconSize(QSize(25, 25))

    def delete_contact(self):
        items = self.view.contactList.selectedItems()
        for item in items:
            username = self.get_username(item.text())
            if username != self.model.myself.username:
                result = QMessageBox.warning(QMessageBox(), 'Are you sure?',
                                             'You will permanently delete all the records with %s.' % username,
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if result == QMessageBox.Yes:
                    self.view.contactList.takeItem(self.view.contactList.row(item))
                    self.change_contact(self.view.contactList.selectedItems()[0])
                    self.model.delete_contact(username)

    def save_info(self, username, ip_addr):
        self.model.add_contact(username, ip_addr)
        item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), username + '\n' + ip_addr)
        self.view.contactList.addItem(item)

    def change_contact(self, item):
        username = self.get_username(item.text())
        self.view.sendButton.setDisabled(False)
        self.view.conversationList.clear()
        self.get_messages(username)
        self.model.change_contact(username)

    def get_avatar(self):
        myself = self.model.myself
        if myself.has_avatar:
            return QPixmap('../assets/avatar/%s.jpg' % myself.username).scaled(40, 40)
        return QPixmap('../assets/avatar/default.jpg').scaled(40, 40)

    def send_message(self):
        content = self.view.textEdit.toPlainText()
        myself = self.model.myself
        self.model.send_message(content)
        if myself.has_avatar:
            item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % myself.username), content)
        else:
            item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), content)
        self.view.conversationList.addItem(item)
        self.view.textEdit.clear()
