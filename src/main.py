import sys
import View
from Model import Model
from Controller import ChatController, LoginController
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


def start_main():
    chat_controller.server = login_controller.server
    chat_controller.init_view()
    chat_controller.init_user()
    MainWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = Model()
    # Initialize Login Page
    dialog = QDialog()
    MainWindow = QMainWindow()
    login_page = View.Ui_Login(dialog)
    login_controller = LoginController(login_page, model)
    dialog.show()
    login_page.buttonBox.accepted.connect(start_main)

    # Initialize MainWindow
    main_ui = View.Ui_Main(MainWindow)
    chat_controller = ChatController(main_ui, model, None)
    sys.exit(app.exec_())