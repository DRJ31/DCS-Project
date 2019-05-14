from PyQt5.QtWidgets import QMainWindow, QMessageBox


class MainWindow(QMainWindow):
    def setController(self, controller):
        self.controller = controller

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     'Are you sure?',
                                     'You are exiting this program.',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.controller.stop_and_exit()
            # self.controller.server.user_leave(self.controller.model.myself['user_id'])
            event.accept()
        else:
            event.ignore()