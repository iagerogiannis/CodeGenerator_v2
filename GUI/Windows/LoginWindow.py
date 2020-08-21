import sys

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QLabel, QPixmap, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QIcon

import config
from GUI.Components.MyLineEdit import MyLineEdit
from GUI.Windows.NewUserWindow import NewUserWindow


# noinspection PyCallByClass,PyArgumentList
class LoginWindow(QDialog):

    username: MyLineEdit
    password: MyLineEdit

    def __init__(self):
        super().__init__()
        self.build_UI()

    def build_UI(self):

        # Image --------------------------------------------------------------------------------------------------------
        image = QLabel()
        pixmap = QPixmap("Files/icon.png")
        image.setPixmap(pixmap)
        image.setContentsMargins(0, 20, 0, 0)
        image.setAlignment(Qt.AlignCenter)

        # Title --------------------------------------------------------------------------------------------------------
        title = QLabel()
        title.setText("Code Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font: 25pt Cronus Round")
        title.setMargin(10)

        # Inputs -------------------------------------------------------------------------------------------------------
        self.username = MyLineEdit(self, "Username")
        self.password = MyLineEdit(self, "Password", isPassword=True)

        # Buttons ------------------------------------------------------------------------------------------------------
        button_login = QPushButton("Log In")
        button_login.clicked.connect(self.handleLogin)

        button_new_user = QPushButton("New User")
        button_new_user.clicked.connect(self.handleNewUser)

        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.handleCancel)

        # Buttons' Layout ----------------------------------------------------------------------------------------------
        buttons = QHBoxLayout()

        buttons.addWidget(button_login)
        buttons.addWidget(button_new_user)
        buttons.addWidget(button_cancel)

        # Total Layout -------------------------------------------------------------------------------------------------
        layout = QVBoxLayout()

        layout.addWidget(image)
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addLayout(buttons)

        self.setLayout(layout)

        layout.setMargin(20)
        self.setWindowTitle("Code Generator")
        self.setWindowIcon(QIcon("Files/app.ico"))
        self.setFixedSize(270, 350)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setWindowFlags(Qt.WindowSystemMenuHint)

        self.show()

    def handleLogin(self):
        if config.db_admin.attemptLogin(self.username.getText(), self.password.getText()):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Wrong username or password!")

    def handleNewUser(self):
        win = NewUserWindow(self)
        self.setWindowOpacity(0.)

    def handleCancel(self):
        self.close()

    def closeEvent(self, event):
        exit()
