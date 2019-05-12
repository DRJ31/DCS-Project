from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QDialog, QMainWindow
import socket

from View import Ui_Add
from Model import Contact


class LoginController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.buttonBox.accepted.connect(self.login)
        self.view.buttonBox.rejected.connect(self.view.parent.reject)

    def login(self):
        ip_addr = socket.gethostbyname(socket.gethostname())
        username = self.view.usernameEdit.text()
        myself = Contact(username, ip_addr, False)
        self.model.contacts.append(myself)
        self.model.myself = myself
        self.view.parent.accept()


class AddContactController:
    def __init__(self, parent, view, model):
        self.parent = parent
        self.view = view
        self.model = model
        self.view.buttonBox.accepted.connect(self.save_info)
        self.view.buttonBox.rejected.connect(self.view.parent.reject)

    def save_info(self):
        if not self.view.usernameEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input username', QMessageBox.Ok, QMessageBox.Ok)
        elif not self.view.ipEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input IP address', QMessageBox.Ok, QMessageBox.Ok)
        else:
            username = self.view.usernameEdit.text()
            ip_addr = self.view.ipEdit.text()
            self.model.add_contact(username, ip_addr)
            item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), username + '\n' + ip_addr)
            self.parent.view.contactList.addItem(item)
            self.view.parent.accept()


class ChatController:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.init_view()

    @staticmethod
    def get_username(text):
        return text.split('\n')[0]

    def init_user(self):
        self.view.usernameLabel.setText(self.model.myself.username)
        self.init_avatar()

    def init_view(self):
        self.init_contacts()
        self.view.sendButton.setDisabled(True)
        self.setup_view_action()

    def init_avatar(self):
        pix = self.get_avatar()
        self.view.avatarLabel.setPixmap(pix)

    def setup_view_action(self):
        view = self.view
        view.textEdit.returnPressed.connect(self.send_message)
        view.deleteButton.clicked.connect(self.delete_contact)
        view.sendButton.clicked.connect(self.send_message)
        view.contactList.itemClicked.connect(self.change_contact)
        view.newButton.clicked.connect(self.add_contact)

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

    def change_contact(self, item):
        username = self.get_username(item.text())
        print(username)
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

    def add_contact(self):
        print("Shit")
        dialog = QDialog()
        view = Ui_Add(dialog)
        controller_add = AddContactController(self, view, self.model)
        dialog.exec()
