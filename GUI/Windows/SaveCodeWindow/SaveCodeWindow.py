from PyQt4.QtCore import Qt

from PyQt4.QtGui import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from Errors.DatabaseErrors import *

from GUI.Windows.SaveCodeWindow.EditField import EditField
import config

import pyperclip


# noinspection PyCallByClass,PyArgumentList,PyBroadException
class SaveCodeWindow(QDialog):

    def __init__(self, parent, password_value, pass_id=0, account_value="", username_value="", email_value="", edit=False):
        super().__init__(parent)
        self.parent = parent
        self.pass_id = pass_id
        self.account_value = account_value
        self.username_value = username_value
        self.email_value = email_value
        self.password_value = password_value
        self.edit = edit
        self.build_UI()
        self.show()

    def build_UI(self):

        self.account = EditField(self, "Account", self.account_value)
        self.username = EditField(self, "Username", self.username_value)
        self.email = EditField(self, "Email Address", self.email_value)
        self.password = EditField(self, "Password", self.password_value)

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.pressed.connect(self.handleSave)

        self.copyButton = QPushButton(self)
        self.copyButton.setText("Copy")
        self.copyButton.pressed.connect(self.handleCopy)

        self.cancelButton = QPushButton(self)
        self.cancelButton.setText("Cancel")
        self.cancelButton.pressed.connect(self.handleCancel)

        buttons = QHBoxLayout()

        buttons.addWidget(self.saveButton)
        buttons.addWidget(self.copyButton)
        buttons.addWidget(self.cancelButton)

        layout = QVBoxLayout()

        layout.addWidget(self.account)
        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addLayout(buttons)

        buttons.setMargin(0)
        buttons.setSpacing(5)
        layout.setMargin(20)
        layout.setSpacing(9)

        self.setLayout(layout)

        self.setMinimumWidth(300)

    def handleSave(self):

        if not self.edit:
            self.saveNewPassword()
        else:
            self.saveEditedPassword()

    def saveNewPassword(self):

        try:
            config.db_admin.addPassword(
                self.account.value,
                self.username.value,
                self.email.value,
                self.password.value
            )

            self.pass_id = str(int(config.db_admin.getLastIndex()))

            self.parent.tab2.addPassword(self.pass_id, self.account.value, self.username.value,
                                         self.email.value, self.password.value)
            QMessageBox.information(self, "Success", "Password registered successfully!")
            self.close()
        except PassAccountLengthError:
            QMessageBox.warning(self, "Error", "Account must contain between 4 and 48 characters!")
        except PassUsernameLengthError:
            QMessageBox.warning(self, "Error", "Username must contain less than 48 characters!")
        except PassEmailLengthError:
            QMessageBox.warning(self, "Error", "Email must contain less than 48 characters!")

    def saveEditedPassword(self):

        try:
            config.db_admin.editPassword(
                self.pass_id,
                self.account.value,
                self.username.value,
                self.email.value,
                self.password.value
            )

            self.parent.tab2.editPassword(self.pass_id,
                                          self.account.value,
                                          self.username.value,
                                          self.email.value,
                                          self.password.value)

            QMessageBox.information(self, "Success", "Password updated successfully!")
            self.close()
        except PassAccountLengthError:
            QMessageBox.warning(self, "Error", "Account must contain between 4 and 48 characters!")
        except PassUsernameLengthError:
            QMessageBox.warning(self, "Error", "Username must contain less than 48 characters!")
        except PassEmailLengthError:
            QMessageBox.warning(self, "Error", "Email must contain less than 48 characters!")

    def handleCopy(self):
        pyperclip.copy(self.password.value)

    def handleCancel(self):
        self.close()

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        self.parent.setWindowOpacity(1.)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()