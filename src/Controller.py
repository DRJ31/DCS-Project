from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QDialog
import xmlrpc.client

from View import Ui_Add
from Model import Message


class Client:
    def __init__(self, username):
        self.username = username
        self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
        self.user_id = self.register()
        self.user_list = self.server.get_online_users()

    def register(self):

        try:
            user_id = self.server.regist_new_user(self.username)

        except:
            # TODO: Add an alert
            user_id = 0
        return user_id


class LoginController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.server = None
        self.client = None
        self.view.buttonBox.accepted.connect(self.login)
        self.view.buttonBox.rejected.connect(self.view.parent.reject)

    def login(self):  # Action when click Login
        username = self.view.userNameEdit.text()
        self.client = Client(username)
        self.server = self.client.server
        self.model.init_self(self.client.user_list)
        self.view.parent.accept()


class AddContactController:
    def __init__(self, parent, view, model):
        self.parent = parent
        self.view = view
        self.model = model
        self.view.buttonBox.accepted.connect(self.save_info)
        self.view.buttonBox.rejected.connect(self.view.parent.reject)

    def save_info(self):
        if not self.view.userIDEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input user ID', QMessageBox.Ok, QMessageBox.Ok)
        elif not self.view.usernameEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input username', QMessageBox.Ok, QMessageBox.Ok)
        else:
            username = self.view.userIDEdit.text()
            ip_addr = self.view.usernameEdit.text()
            self.model.add_contact(username, ip_addr)
            item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), username)
            self.parent.view.contactList.addItem(item)
            self.view.parent.accept()


class ChatController:

    def __init__(self, view, model, server):
        self.view = view
        self.model = model
        self.server = server

    @staticmethod
    def get_username(text):
        return text.split('\n')[0]

    def init_view(self):
        self.init_contacts()
        self.view.sendButton.setDisabled(True)
        self.setup_view_action()

    def init_contacts(self):
        for contact in self.model.contacts:
            item = QListWidgetItem(QIcon('../assets/avatar/%s' % contact['avatar']), contact['username'])
            self.view.contactList.addItem(item)
            self.model.messages[contact['user_id']] = []
        self.view.contactList.setIconSize(QSize(25, 25))

    def setup_view_action(self):
        view = self.view
        view.textEdit.returnPressed.connect(self.send_message)
        view.deleteButton.clicked.connect(self.delete_contact)
        view.sendButton.clicked.connect(self.send_message)
        view.contactList.itemClicked.connect(self.change_contact)
        view.newButton.clicked.connect(self.add_contact)

    def init_user(self):
        self.view.usernameLabel.setText(self.model.myself['username'])
        self.init_avatar()

    def init_avatar(self):
        pix = self.get_avatar()
        self.view.avatarLabel.setPixmap(pix)

    def get_avatar(self):
        myself = self.model.myself
        return QPixmap('../assets/avatar/%s' % myself['avatar']).scaled(40, 40)

    def delete_contact(self):  # Action when delete button pressed
        items = self.view.contactList.selectedItems()
        for item in items:
            username = self.get_username(item.text())
            user_id = self.model.get_user_id_by_name(username)
            if username != self.model.myself.username:
                result = QMessageBox.warning(QMessageBox(), 'Are you sure?',
                                             'You will permanently delete all the records with %s.' % username,
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if result == QMessageBox.Yes:
                    self.view.contactList.takeItem(self.view.contactList.row(item))
                    self.change_contact(self.view.contactList.selectedItems()[0])
                    self.model.delete_contact(user_id)

    def change_contact(self, item):  # Action when click corresponding user
        username = self.get_username(item.text())
        user_id = self.model.get_user_id_by_name(username)
        self.view.sendButton.setDisabled(False)
        self.view.conversationList.clear()
        self.get_messages(user_id)
        self.model.change_contact(user_id)

    def get_messages(self, user_id):  # Get messages of current user
        # Init user information
        user = self.model.get_user_by_id(user_id)
        myself = self.model.myself

        messages = self.server.display_message(user_id)
        for message in messages:
            self.model.messages[message['sender']].append(message)
        message_list = self.model.messages[user_id]
        for message in message_list:
            if message['sender'] == myself['user_id']:
                item = QListWidgetItem(QIcon('../assets/avatar/%s' % myself['avatar']), message['content'])
            else:
                item = QListWidgetItem(QIcon('../assets/avatar/%s' % user['avatar']), message['content'])
            self.view.conversationList.addItem(item)
        self.view.conversationList.setIconSize(QSize(25, 25))

    def send_message(self):
        content = self.view.textEdit.toPlainText()
        myself = self.model.myself
        self.server.send_message(myself['user_id'], content, self.model.current_user['user_id'])
        self.model.send_message(content)
        item = QListWidgetItem(QIcon('../assets/avatar/%s' % myself['avatar']), content)
        self.view.conversationList.addItem(item)
        self.view.textEdit.clear()

    def add_contact(self):  # Pop out add contact window
        dialog = QDialog()
        view = Ui_Add(dialog)
        controller_add = AddContactController(self, view, self.model)
        dialog.exec()
