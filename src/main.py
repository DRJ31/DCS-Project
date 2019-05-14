from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import sys

from model import Model
from controller import ChatController, LoginController
from view import LoginView, MainView


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
    login_page = LoginView(dialog)
    login_controller = LoginController(login_page, model)
    dialog.show()
    login_page.buttonBox.accepted.connect(start_main)

    # Initialize MainWindow
    main_ui = MainView(MainWindow)
    chat_controller = ChatController(main_ui, model, None)
    sys.exit(app.exec_())