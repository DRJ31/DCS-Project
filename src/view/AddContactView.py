# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class AddContactView(object):

    def __init__(self, AddContactForm):
        self.searchEdit = QtWidgets.QLineEdit(AddContactForm)
        self.searchButton = QtWidgets.QPushButton(AddContactForm)
        self.listWidget = QtWidgets.QListWidget(AddContactForm)
        self.pushButton = QtWidgets.QPushButton(AddContactForm)
        self.setupUi(AddContactForm)

    def setupUi(self, AddContactForm):
        AddContactForm.setObjectName("AddContactForm")
        AddContactForm.resize(559, 477)
        self.searchEdit.setGeometry(QtCore.QRect(10, 30, 381, 31))
        self.searchEdit.setObjectName("searchEdit")
        self.searchButton.setGeometry(QtCore.QRect(400, 30, 75, 31))
        self.searchButton.setObjectName("searchButton")
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 541, 401))
        self.listWidget.setObjectName("listWidget")
        self.pushButton.setGeometry(QtCore.QRect(480, 30, 75, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(AddContactForm)
        QtCore.QMetaObject.connectSlotsByName(AddContactForm)

    def retranslateUi(self, AddContactForm):
        _translate = QtCore.QCoreApplication.translate
        AddContactForm.setWindowTitle(_translate("AddContactForm", "Add Contact"))
        self.searchButton.setText(_translate("AddContactForm", "Search"))
        self.pushButton.setText(_translate("AddContactForm", "Add"))


