import sys
import View
from PyQt5.QtWidgets import QApplication, QMainWindow




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = View.Ui_Form(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())