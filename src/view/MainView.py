from PyQt5 import QtWidgets, QtGui, QtCore

from .MyTextEdit import MyTextEdit


class MainView(object):
    def __init__(self, Form):
        self.textEdit = MyTextEdit(Form, self)
        self.conversationList = QtWidgets.QListWidget(Form)
        self.newButton = QtWidgets.QPushButton(Form)
        self.deleteButton = QtWidgets.QPushButton(Form)
        self.sendButton = QtWidgets.QPushButton(Form)
        self.contactList = QtWidgets.QListWidget(Form)
        self.avatarLabel = QtWidgets.QLabel(Form)
        self.usernameLabel = QtWidgets.QLabel(Form)
        self.setupUi(Form)

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
        # Setup conversation interface
        self.conversationList.setGeometry(QtCore.QRect(260, 10, 611, 441))
        self.conversationList.setObjectName("conversationList")
        self.conversationList.setWordWrap(True)
        # Setup New button
        self.newButton.setGeometry(QtCore.QRect(10, 630, 75, 23))
        self.newButton.setObjectName("newButton")
        # Setup Delete button
        self.deleteButton.setGeometry(QtCore.QRect(100, 630, 75, 23))
        self.deleteButton.setObjectName("deleteButton")
        # Setup Send button
        self.sendButton.setGeometry(QtCore.QRect(790, 630, 75, 23))
        self.sendButton.setObjectName("sendButton")
        # Setup Contact List
        self.contactList.setGeometry(QtCore.QRect(10, 70, 241, 551))
        self.contactList.setObjectName("contactList")
        self.contactList.setWordWrap(True)
        # Setup avartar label
        self.avatarLabel.setGeometry(QtCore.QRect(10, 10, 61, 51))
        self.avatarLabel.setObjectName("avatarLabel")
        # Setup username label
        self.usernameLabel.setGeometry(QtCore.QRect(90, 10, 161, 51))
        self.usernameLabel.setStyleSheet("font-weight: bold; font-size: 20px")
        self.usernameLabel.setObjectName("usernameLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DCS Chat"))
        self.newButton.setText(_translate("Form", "New"))
        self.deleteButton.setText(_translate("Form", "Delete"))
        self.sendButton.setText(_translate("Form", "Send"))



