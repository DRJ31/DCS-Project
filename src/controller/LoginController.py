from PyQt5.QtWidgets import QDialog, QMessageBox

from view import RegisterView
from .RegisterController import RegisterController
from .Client import Client
from utils.Exceptions import FetchDataError


class LoginController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.server = None
        self.client = None
        self.view.buttonBox.accepted.connect(self.login)
        self.view.buttonBox.rejected.connect(self.register)

    def login(self):  # Action when click Login
        username = self.view.userNameEdit.text()
        password = self.view.passwordEdit.text()
        if not username:
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input username', QMessageBox.Ok, QMessageBox.Ok)
            return
        elif not password:
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input password', QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            self.client = Client(username)
        except FetchDataError:
            QMessageBox.warning(QMessageBox(), 'Warning', 'Username or Password is invalid!', QMessageBox.Ok, QMessageBox.Ok)
            return
        self.server = self.client.server
        self.model.init_self(self.client.user_list)
        self.view.parent.accept()

    def register(self):
        dialog = QDialog()
        view = RegisterView(dialog)
        register_controller = RegisterController(view)
        dialog.exec()
