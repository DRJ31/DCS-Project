# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class RegisterView(object):

    def __init__(self, Register):
        self.parent = Register
        self.buttonBox = QtWidgets.QDialogButtonBox(Register)
        self.formLayoutWidget = QtWidgets.QWidget(Register)
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.usernameEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.passwordEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.confirmEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.chooseButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.setupUi(Register)

    def setupUi(self, Register):
        Register.setObjectName("Register")
        Register.resize(407, 281)
        registerButton = QtWidgets.QPushButton(Register)
        registerButton.setText("Register")
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.addButton(registerButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 221))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.usernameEdit.setObjectName("usernameEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.usernameEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.passwordEdit.setObjectName("passwordEdit")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.passwordEdit)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.confirmEdit.setObjectName("confirmEdit")
        self.confirmEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.confirmEdit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.chooseButton.setObjectName("chooseButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.chooseButton)

        self.retranslateUi(Register)
        self.buttonBox.accepted.connect(Register.accept)
        self.buttonBox.rejected.connect(Register.reject)
        self.chooseButton.clicked.connect(self.choose_file)
        QtCore.QMetaObject.connectSlotsByName(Register)

    def retranslateUi(self, Register):
        _translate = QtCore.QCoreApplication.translate
        Register.setWindowTitle(_translate("Register", "Register"))
        self.label.setText(_translate("Register", "Username:"))
        self.label_2.setText(_translate("Register", "Password:"))
        self.label_3.setText(_translate("Register", "Confirm Password:"))
        self.label_4.setText(_translate("Register", "Avatar"))
        self.chooseButton.setText(_translate("Register", "Choose File"))

    def choose_file(self):
        filename, filetype = QFileDialog.getOpenFileName(QFileDialog(), 'Choose avatar', '.', 'Image Files(*.jpg *.png)')
        if filename != "":
            self.chooseButton.setText(filename)
