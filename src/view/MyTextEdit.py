from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal


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