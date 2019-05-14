from PyQt5 import QtWidgets, QtGui, QtCore


class AddContactView(object):

    def __init__(self, Dialog):
        super(AddContactView, self).__init__()
        self.parent = Dialog
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.userIDEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.usernameEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.setupUi(Dialog)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(301, 208)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../assets/icon/telegram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        # Setup buttons
        addButton = QtWidgets.QPushButton(Dialog)
        addButton.setText("Save")
        self.buttonBox.setGeometry(QtCore.QRect(-60, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.addButton(addButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.setObjectName("buttonBox")
        # Setup layout
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 30, 281, 91))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label.setStyleSheet("font-weight: bold")
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.userIDEdit.setObjectName("userIDEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.userIDEdit)
        self.label_2.setStyleSheet("font-weight: bold")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.usernameEdit.setObjectName("usernameEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.usernameEdit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Contact"))
        self.label.setText(_translate("Dialog", "User ID:"))
        self.label_2.setText(_translate("Dialog", "Username:"))