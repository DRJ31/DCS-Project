import sys
import View
from Model import Model
from Controller import ChatController, LoginController
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


def start_main(MainWindow, controller):
    controller.init_user()
    MainWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = QDialog()
    login_page = View.Ui_Login(dialog)
    MainWindow = QMainWindow()
    model = Model()
    login_controller = LoginController(login_page, model)
    dialog.show()
    main_ui = View.Ui_Main(MainWindow)
    controller = ChatController(main_ui, model)
    login_page.buttonBox.accepted.connect(lambda: start_main(MainWindow, controller))
    sys.exit(app.exec_())