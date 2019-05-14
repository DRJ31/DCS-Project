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
        self.__flag = True
        self.__running = True

    def terminate(self):
        self.__running = False

    def run(self):
        while self.__running:
            if not self.__flag:
                print("Paused")
                time.sleep(1)
                continue
            time.sleep(3)
            self.controller.update_messages(self.user_id)

    def pause(self):
        self.__flag = False

    def resume(self):
        self.__flag = True


class ChatController:

    def __init__(self, view, model, server):
        self.view = view
        self.model = model
        self.server = server
        self.msg_listener = None

    @staticmethod
    def get_username(text):
        return text.split('\n')[0]

    def init_view(self):
        self.init_contacts()
        self.view.sendButton.setDisabled(True)
        self.setup_view_action()
        # self.msg_listener = MessageListener(self, self.model.myself['user_id'])
        # self.msg_listener.start()

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
            if username != self.model.myself['username']:
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
        self.update_messages(self.model.myself['user_id'])

    def update_messages(self, user_id):
        # messages = self.stop_and_display_message(user_id)
        messages = self.server.display_message(user_id)
        # self.msg_listener.resume()
        print("Msg:", messages)
        myself = self.model.myself
        for message in messages:
            current_user = self.model.current_user
            if myself['user_id'] == message['sender']:
                user_id = message['receiver']
            else:
                user_id = message['sender']
            try:
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
        if self.model.current_user['user_id'] != myself['user_id']:
            # self.stop_and_send_message(myself['user_id'], content, self.model.current_user['user_id'])
            self.server.send_message(myself['user_id'], content, self.model.current_user['user_id'])
        self.model.send_message(content)
        item = QListWidgetItem(QIcon('../assets/avatar/%s' % myself['avatar']), content)
        self.view.conversationList.addItem(item)
        self.view.textEdit.clear()

    def add_contact(self):  # Pop out add contact window
        dialog = QDialog()
        view = AddContactView(dialog)
        controller_add = AddContactController(self, view, self.model)
        dialog.exec()

    def stop_and_display_message(self, user_id):
        self.msg_listener.pause()
        message = self.server.display_message(user_id)
        return message

    def stop_and_send_message(self, sender, content, receiver):
        self.msg_listener.pause()
        self.server.send_message(sender, content, receiver)

    def stop_and_exit(self):
        self.msg_listener.terminate()
        self.server.user_leave(self.model.myself['user_id'])

