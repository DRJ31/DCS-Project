from PyQt5 import QtWidgets, QtCore


class LoginView(object):

    def __init__(self, Dialog):
        self.parent = Dialog
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.userNameEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.passwordEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.passwordLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.usernameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.setupUi(Dialog)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        # Setup buttonBox
        loginButton = QtWidgets.QPushButton(Dialog)
        loginButton.setText("Login")
        self.buttonBox.setGeometry(QtCore.QRect(30, 230, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.addButton(loginButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.setObjectName("buttonBox")
        # Setup layout
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.userNameEdit.setObjectName("userNameEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.userNameEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.passwordEdit.setObjectName("passwordEdit")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.passwordEdit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.usernameLabel.setObjectName("usernameLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.usernameLabel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.passwordLabel.setText(_translate("Dialog", "Password"))
        self.usernameLabel.setText(_translate("Dialog", "Username"))
