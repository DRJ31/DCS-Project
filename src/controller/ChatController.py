from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

import threading
import time

from .AddContactController import AddContactController
from view import AddContactView


class MessageListener(threading.Thread):

    def __init__(self, controller, user_id):
        super(MessageListener, self).__init__()
        self.controller = controller
        self.user_id = user_id
        self.__running = True

    def terminate(self):
        self.__running = False

    def run(self):
        while self.__running:
            # time.sleep(1)
            message_queue = self.controller.model.message_queue
            self.controller.update_messages(self.user_id)
            while not message_queue.empty():
                msg = message_queue.get()
                self.controller.server.send_message(msg['sender'], msg['content'], msg['receiver'])


class ChatController:

    def __init__(self, view, model, server):
        self.view = view
        self.model = model
        self.server = server
        self.msg_listener = None

    def init_view(self):
        self.init_contacts()
        self.view.sendButton.setDisabled(True)
        self.setup_view_action()
        self.msg_listener = MessageListener(self, self.model.myself['user_id'])
        self.msg_listener.start()

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
            username = item.text()
            user_id = self.model.get_user_id_by_name(username)
            if username != self.model.myself['username']:
                result = QMessageBox.warning(QMessageBox(), 'Are you sure?',
                                             'You will permanently delete all the records with %s.' % username,
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if result == QMessageBox.Yes:
                    self.view.contactList.takeItem(self.view.contactList.row(item))
                    self.change_contact(self.view.contactList.selectedItems()[0])
                    self.model.delete_contact(user_id)

    def change_contact(self, item):  # Action when click corresponding user
        username = item.text()
        user_id = self.model.get_user_id_by_name(username)
        self.view.sendButton.setDisabled(False)
        self.view.conversationList.clear()
        self.get_messages(user_id)
        self.model.change_contact(user_id)

    def update_messages(self, user_id):
        messages = self.server.display_message(user_id)
        myself = self.model.myself
        for message in messages:
            current_user = self.model.current_user
            if myself['user_id'] == message['sender']:
                user_id = message['receiver']
            else:
                user_id = message['sender']
            try:
                if message['sender'] != message['receiver']:
                    self.model.messages[user_id].append(message)
            except:
                if user_id == myself['user_id']:
                    return
                contact = {
                    'user_id': user_id,
                    'username': self.server.get_username_by_id(user_id),
                    'avatar': 'default.jpg'
                }
                self.model.contacts.append(contact)
                item = QListWidgetItem(QIcon('../assets/avatar/%s' % contact['avatar']), contact['username'])
                self.view.contactList.addItem(item)
                self.model.messages[user_id] = [message]

            if current_user and user_id == current_user['user_id']:
                item = QListWidgetItem(QIcon('../assets/avatar/%s' % current_user['avatar']), message['content'])
                self.view.conversationList.addItem(item)

    def get_messages(self, user_id):  # Get messages of current user
        # Init user information
        user = self.model.get_user_by_id(user_id)
        myself = self.model.myself

        message_list = self.model.messages[int(user_id)]
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
        self.model.send_message(content)
        item = QListWidgetItem(QIcon('../assets/avatar/%s' % myself['avatar']), content)
        self.view.conversationList.addItem(item)
        self.view.textEdit.clear()

    def add_contact(self):  # Pop out add contact window
        dialog = QDialog()
        view = AddContactView(dialog)
        controller_add = AddContactController(self, view, self.model)
        dialog.exec()

    def stop_and_exit(self):
        self.msg_listener.terminate()
        self.msg_listener.join()
        self.server.user_leave(self.model.myself['user_id'])

