from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from PyQt5.QtGui import QIcon


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
            user_id = self.view.userIDEdit.text()
            username = self.view.usernameEdit.text()
            self.model.add_contact(int(user_id), username, 'default.jpg')
            item = QListWidgetItem(QIcon('../assets/avatar/default.jpg'), username)
            self.parent.view.contactList.addItem(item)
            self.view.parent.accept()
