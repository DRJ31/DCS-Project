from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

import threading

from .AddContactController import AddContactController
from view import AddContactView
from utils.AvatarTool import check_avatar


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

    @staticmethod
    def check_avatar_thread(username):
        t = threading.Thread(target=check_avatar, args=(username, ))
        t.start()
        t.join()

    def init_messages(self):
        model = self.model
        myself = model.myself
        model.contacts.append({
            'user_id': 0,
            'username': 'world',
            'avatar': 'Globe.jpg'
        })
        model.messages[0] = []
        messages = self.server.get_history_messages(myself['user_id'])
        for message in messages:
            if message['sender'] == message['receiver']:
                model.messages[myself['user_id']].append(message)
            elif message['sender'] == myself['user_id']:
                if not model.get_user_by_id(message['receiver']):
                    username = self.server.get_username_by_id(message['receiver'])
                    model.contacts.append({
                        'user_id': message['receiver'],
                        'username': username,
                        'avatar': username + ".jpg"
                    })
                    model.messages[message['receiver']] = []
                model.messages[message['receiver']].append(message)
            elif message['receiver'] == myself['user_id']:
                if not model.get_user_by_id(message['sender']):
                    username = self.server.get_username_by_id(message['sender'])
                    model.contacts.append({
                        'user_id': message['sender'],
                        'username': username,
                        'avatar': username + ".jpg"
                    })
                    model.messages[message['sender']] = []
                model.messages[message['sender']].append(message)

    def start_thread(self):
        self.msg_listener = MessageListener(self, self.model.myself['user_id'])
        self.msg_listener.start()

    def init_view(self):
        self.init_messages()
        self.init_contacts()
        self.view.sendButton.setDisabled(True)
        self.setup_view_action()
        self.start_thread()

    def init_contacts(self):
        for contact in self.model.contacts:
            if contact['username'] != 'world':
                self.check_avatar_thread(contact['username'])
            item = QListWidgetItem(QIcon('../assets/avatar/%s' % contact['avatar']), contact['username'])
            self.view.contactList.addItem(item)
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
        self.check_avatar_thread(myself['username'])
        return QPixmap('../assets/avatar/%s.jpg' % myself['username']).scaled(50, 50)

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
                    self.terminate_thread()
                    self.server.delete_history_records(user_id)
                    self.start_thread()

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
            if message['receiver'] == 0:
                user_id = 0
            elif myself['user_id'] == message['sender']:
                user_id = message['receiver']
            else:
                user_id = message['sender']
            try:
                if message['sender'] != message['receiver']:
                    self.model.messages[user_id].append(message)
            except:
                if user_id == myself['user_id']:
                    return
                new_username = self.server.get_username_by_id(user_id)
                contact = {
                    'user_id': user_id,
                    'username': new_username,
                    'avatar': new_username + '.jpg'
                }
                self.model.contacts.append(contact)
                item = QListWidgetItem(QIcon('../assets/avatar/%s' % contact['avatar']), contact['username'])
                self.view.contactList.addItem(item)
                self.model.messages[user_id] = [message]

            if current_user and user_id == current_user['user_id']:
                if user_id == 0:
                    username = self.server.get_username_by_id(message['sender'])
                    item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % username), message['content'])
                else:
                    item = QListWidgetItem(QIcon('../assets/avatar/%s' % current_user['avatar']), message['content'])
                self.view.conversationList.addItem(item)

    def get_messages(self, user_id):  # Get messages of current user
        # Init user information
        user = self.model.get_user_by_id(user_id)
        myself = self.model.myself

        message_list = self.model.messages[int(user_id)]
        for message in message_list:
            if message['receiver'] == 0:
                msg_sender = self.model.get_user_by_id(message['sender'])
                if not msg_sender:
                    self.terminate_thread()
                    username = self.server.get_username_by_id(message['sender'])
                    self.model.contacts.append({
                        'user_id': message['sender'],
                        'username': username,
                        'avatar': username + ".jpg"
                    })
                    self.check_avatar_thread(username)
                    self.start_thread()
                else:
                    username = msg_sender['username']
                item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % username), message['content'])
            elif message['sender'] == myself['user_id']:
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
        controller_add = AddContactController(self, view, self.model, self.server)
        dialog.exec()

    def terminate_thread(self):
        self.msg_listener.terminate()
        self.msg_listener.join()

    def stop_and_exit(self):
        self.terminate_thread()
        self.server.user_leave(self.model.myself['user_id'])

