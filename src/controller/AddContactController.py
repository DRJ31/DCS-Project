from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from PyQt5.QtGui import QIcon

import threading

from utils.AvatarTool import check_avatar


class AddContactController:
    def __init__(self, parent, view, model, server):
        self.parent = parent
        self.view = view
        self.model = model
        self.server = server
        self.view.searchButton.clicked.connect(self.search_user)
        self.view.pushButton.clicked.connect(self.add_user)
        self.results = None

    @staticmethod
    def get_id_and_user(string):
        id = string.split(" ")[0]
        username = " ".join(string.split(" ")[1:])
        return id, username

    def search_thread(self, keyword):
        self.results = self.server.search_users(keyword)

    def search_user(self):
        view = self.view
        view.listWidget.clear()
        # Threading handling
        self.parent.terminate_thread()
        t = threading.Thread(target=self.search_thread, args=(view.searchEdit.text(), ))
        t.start()
        t.join()
        self.parent.start_thread()
        for result in self.results:
            status = False
            if not self.parent.model.get_user_by_id(result['user_id']):
                item = QListWidgetItem(str(result['user_id']) + " " + result['username'])
                view.listWidget.addItem(item)
                status = True
            if not status:
                item = QListWidgetItem("No result found or you have added all the users you search for.")
                view.listWidget.addItem(item)

    def add_user(self):
        view = self.view
        if not view.listWidget.selectedItems():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please select a user to add!', QMessageBox.Ok, QMessageBox.Ok)
            return
        else:
            user_id, username = self.get_id_and_user(view.listWidget.selectedItems()[0].text())
            check_avatar(username)
            self.model.add_contact(int(user_id), username, username + '.jpg')
            item = QListWidgetItem(QIcon('../assets/avatar/%s.jpg' % username), username)
            self.parent.view.contactList.addItem(item)
            self.view.parent.accept()
