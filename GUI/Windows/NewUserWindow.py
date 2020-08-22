from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import config
from Errors.DatabaseErrors import *
from GUI.Components.MyLineEdit import MyLineEdit


# noinspection PyCallByClass,PyArgumentList,PyBroadException
class NewUserWindow(QDialog):
    username: MyLineEdit
    email: MyLineEdit
    password: MyLineEdit
    confirm_password: MyLineEdit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.build_UI()

    def build_UI(self):

        # Image --------------------------------------------------------------------------------------------------------
        image = QLabel()
        pixmap = QPixmap("Files/icon.png")
        image.setPixmap(pixmap)
        image.setContentsMargins(0, 20, 0, 0)
        image.setAlignment(QtCore.Qt.AlignCenter)

        # Title --------------------------------------------------------------------------------------------------------
        title = QLabel()
        title.setText("Code Generator")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font: 25pt Cronus Round")
        title.setContentsMargins(10, 10, 10, 10)

        # Inputs -------------------------------------------------------------------------------------------------------
        self.username = MyLineEdit(self, "Username")
        self.email = MyLineEdit(self, "Email")
        self.password = MyLineEdit(self, "Password", isPassword=True)
        self.confirm_password = MyLineEdit(self, "Confirm Password", isPassword=True)

        # Buttons ------------------------------------------------------------------------------------------------------
        button_create_account = QPushButton("Create Account")
        button_create_account.clicked.connect(self.handleCreateAccount)

        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.handleCancel)

        # Buttons' Layout ----------------------------------------------------------------------------------------------
        buttons = QHBoxLayout()

        buttons.addWidget(button_create_account)
        buttons.addWidget(button_cancel)

        # Total Layout -------------------------------------------------------------------------------------------------
        layout = QVBoxLayout()

        layout.addWidget(image)
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)
        layout.addLayout(buttons)

        self.setLayout(layout)

        layout.setContentsMargins(20, 20, 20, 20)
        self.setWindowTitle("Code Generator")
        self.setWindowIcon(QIcon("Files/app.ico"))
        self.setFixedSize(270, 390)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)

        self.show()

    def handleCreateAccount(self):

        if self.password.getText() == self.confirm_password.getText():
            try:
                config.db_admin.createUser(self.username.getText(), self.email.getText(), self.password.getText())
                QMessageBox.information(self, "Success", "User created successfully!")
                self.close()
            except EmptyUsernameError:
                QMessageBox.warning(self, "Error", "Username may not be blank!")
            except InvalidCharactersInUsernameError:
                QMessageBox.warning(self, "Error", "Username may contain only letters (A-Z, a-z), "
                                                   "numbers (0-9) and underscore (_)!")
            except UsernameUsedError:
                QMessageBox.warning(self, "Error", "Username is already used!")
            except EmailUsedError:
                QMessageBox.warning(self, "Error", "Email Address is already used!")
            except UsernameLengthError:
                QMessageBox.warning(self, "Error", "Username must contain between 6 and 48 characters!")
            except EmailLengthError:
                QMessageBox.warning(self, "Error", "Email Address must contain between 6 and 48 characters!")
            except PasswordLengthError:
                QMessageBox.warning(self, "Error", "Password must contain between 6 and 48 characters!")
        else:
            QMessageBox.warning(self, "Error", "Passwords do not match!")

    def handleCancel(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        self.parent.setWindowOpacity(1.)
