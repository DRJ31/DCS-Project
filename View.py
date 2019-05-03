# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Controller import ChatController


class Ui_Form(object):

    def fuck(self):
        print(self.contactList.itemClicked)

    def __init__(self, Form):
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.conversationList = QtWidgets.QListWidget(Form)
        self.newButton = QtWidgets.QPushButton(Form)
        self.deleteButton = QtWidgets.QPushButton(Form)
        self.sendButton = QtWidgets.QPushButton(Form)
        self.contactList = QtWidgets.QListWidget(Form)
        self.setupUi(Form)
        self.controller = ChatController(self)
        self.contactList.itemClicked.connect(self.fuck)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(875, 665)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/telegram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.textEdit.setGeometry(QtCore.QRect(260, 460, 611, 161))
        self.textEdit.setObjectName("textEdit")
        self.conversationList.setGeometry(QtCore.QRect(260, 10, 611, 441))
        self.conversationList.setObjectName("conversationList")
        self.newButton.setGeometry(QtCore.QRect(10, 630, 75, 23))
        self.newButton.setObjectName("newButton")
        self.deleteButton.setGeometry(QtCore.QRect(100, 630, 75, 23))
        self.deleteButton.setObjectName("deleteButton")
        self.sendButton.setGeometry(QtCore.QRect(790, 630, 75, 23))
        self.sendButton.setObjectName("sendButton")
        self.contactList.setGeometry(QtCore.QRect(10, 10, 241, 611))
        self.contactList.setObjectName("contactList")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Telegram"))
        self.newButton.setText(_translate("Form", "New"))
        self.deleteButton.setText(_translate("Form", "Delete"))
        self.sendButton.setText(_translate("Form", "Send"))


