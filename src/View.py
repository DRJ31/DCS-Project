# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt

from Controller import ChatController


class MyTextEdit(QtWidgets.QTextEdit):
    returnPressed = pyqtSignal()

    def __init__(self, MainWindow, parent):
        super(MyTextEdit, self).__init__(MainWindow)
        self.parent = parent

    def keyPressEvent(self, event):
        if not self.parent.sendButton.isEnabled():
            QtWidgets.QTextEdit.keyPressEvent(self, event)

        if not event.modifiers():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                self.returnPressed.emit()
                event.accept()
            else:
                QtWidgets.QTextEdit.keyPressEvent(self, event)
        else:
            QtWidgets.QTextEdit.keyPressEvent(self, event)


class Ui_Form(object):
    def __init__(self, Form):
        self.textEdit = MyTextEdit(Form, self)
        self.conversationList = QtWidgets.QListWidget(Form)
        self.newButton = QtWidgets.QPushButton(Form)
        self.deleteButton = QtWidgets.QPushButton(Form)
        self.sendButton = QtWidgets.QPushButton(Form)
        self.contactList = QtWidgets.QListWidget(Form)
        self.avatarLabel = QtWidgets.QLabel(Form)
        self.usernameLabel = QtWidgets.QLabel(Form)
        self.controller = ChatController(self)
        self.setupUi(Form)
        if not self.controller.current_user:
            self.sendButton.setDisabled(True)

    def init_avatar(self):
        pix = self.controller.get_avatar()
        self.avatarLabel.setPixmap(pix)

    def setupUi(self, Form):
        # Setup Main Window
        Form.setObjectName("Form")
        Form.resize(875, 665)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../assets/icon/telegram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        # Setup text editor
        self.textEdit.setGeometry(QtCore.QRect(260, 460, 611, 161))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.returnPressed.connect(self.controller.send_message)
        # Setup conversation interface
        self.conversationList.setGeometry(QtCore.QRect(260, 10, 611, 441))
        self.conversationList.setObjectName("conversationList")
        self.conversationList.setWordWrap(True)
        # Setup New button
        self.newButton.setGeometry(QtCore.QRect(10, 630, 75, 23))
        self.newButton.setObjectName("newButton")
        self.newButton.clicked.connect(self.add_contact)
        # Setup Delete button
        self.deleteButton.setGeometry(QtCore.QRect(100, 630, 75, 23))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.controller.delete_contact)
        # Setup Send button
        self.sendButton.setGeometry(QtCore.QRect(790, 630, 75, 23))
        self.sendButton.setObjectName("sendButton")
        self.sendButton.clicked.connect(self.controller.send_message)
        # Setup Contact List
        self.contactList.setGeometry(QtCore.QRect(10, 70, 241, 551))
        self.contactList.setObjectName("contactList")
        self.contactList.setWordWrap(True)
        self.contactList.itemClicked.connect(self.controller.change_contact)
        # Setup avartar label
        self.avatarLabel.setGeometry(QtCore.QRect(10, 10, 61, 51))
        self.init_avatar()
        self.avatarLabel.setObjectName("avatarLabel")
        # Setup username label
        self.usernameLabel.setGeometry(QtCore.QRect(90, 10, 161, 51))
        self.usernameLabel.setText(self.controller.myself.username)
        self.usernameLabel.setStyleSheet("font-weight: bold; font-size: 20px")
        self.usernameLabel.setObjectName("usernameLabel")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Telegram"))
        self.newButton.setText(_translate("Form", "New"))
        self.deleteButton.setText(_translate("Form", "Delete"))
        self.sendButton.setText(_translate("Form", "Send"))

    def add_contact(self):
        Dialog = QDialog()
        add_ui = Ui_Dialog(Dialog, self)
        Dialog.exec()


class Ui_Dialog(object):

    def __init__(self, Dialog, parent):
        super(Ui_Dialog, self).__init__()
        self.parent = parent
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.usernameEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.ipEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.setupUi(Dialog)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(301, 208)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../assets/icon/telegram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonBox.setGeometry(QtCore.QRect(-60, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.save_info)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 30, 281, 91))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label.setStyleSheet("font-weight: bold")
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.usernameEdit.setObjectName("usernameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.usernameEdit)
        self.label_2.setStyleSheet("font-weight: bold")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.ipEdit.setObjectName("ipEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ipEdit)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Contact"))
        self.label.setText(_translate("Dialog", "Username:"))
        self.label_2.setText(_translate("Dialog", "IP Address:"))

    def save_info(self):
        if not self.usernameEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input username', QMessageBox.Ok, QMessageBox.Ok)
        elif not self.ipEdit.text():
            QMessageBox.warning(QMessageBox(), 'Warning', 'Please input IP address', QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.parent.controller.save_info(self.usernameEdit.text(), self.ipEdit.text())
