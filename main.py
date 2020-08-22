import sys

from PyQt5.QtWidgets import QApplication, QDialog

import config
from GUI.Windows.LoginWindow import LoginWindow
from GUI.Windows.MainWindow.MainWindow import MainWindow
from Database.DatabaseAdministrator import DatabaseAdministrator


def run():
    app = QApplication(sys.argv)
    while True:
        config.db_admin = DatabaseAdministrator()
        loginWindow = LoginWindow()
        if loginWindow.exec_() == QDialog.Accepted:
            win = MainWindow()
            app.exec_()


run()
