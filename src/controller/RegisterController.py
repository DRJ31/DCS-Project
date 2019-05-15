from PyQt5.QtWidgets import QMessageBox

import xmlrpc.client


class RegisterController:

    def __init__(self, view):
        self.view = view
        self.view.buttonBox.accepted.connect(self.register)

    def register(self):
        view = self.view
        if view.chooseButton.text() == "Choose File":
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please choose your avatar', QMessageBox.Ok, QMessageBox.Ok)
            return
        elif not view.usernameEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input your username!', QMessageBox.Ok, QMessageBox.Ok)
            return
        elif not view.passwordEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input your password!', QMessageBox.Ok, QMessageBox.Ok)
            return
        elif not view.confirmEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please confirm your password!', QMessageBox.Ok, QMessageBox.Ok)
            return
        elif view.passwordEdit.text() != view.confirmEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'The two passwords are not the same.', QMessageBox.Ok, QMessageBox.Ok)
            return
        with open(view.chooseButton.text(), 'rb') as f:
            img = xmlrpc.client.Binary(f.read())
        server = xmlrpc.client.ServerProxy('http://localhost:8000')
        result = server.user_register(view.usernameEdit.text(), view.passwordEdit.text(), img)
        if not result:
            QMessageBox.warning(QMessageBox(), 'Warning', 'The username has registered.', QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.information(QMessageBox(), 'Success', 'You have successfully registered.', QMessageBox.Ok, QMessageBox.Ok)
        view.parent.accept()
