import sys
import View
from Model import Model
from Controller import ChatController
from PyQt5.QtWidgets import QApplication, QMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = View.Ui_Main(MainWindow)
    model = Model()
    controller = ChatController(ui, model)
    MainWindow.show()
    sys.exit(app.exec_())