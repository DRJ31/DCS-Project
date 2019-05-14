from PyQt5.QtWidgets import QMessageBox

from .Client import Client


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
        if not username:
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input your username!', QMessageBox.Ok, QMessageBox.Ok)
            return
        self.client = Client(username)
        self.server = self.client.server
        self.model.init_self(self.client.user_list)
        self.view.parent.accept()