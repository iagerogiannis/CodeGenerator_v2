from PyQt4.QtCore import Qt

from PyQt4.QtGui import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from Errors.DatabaseErrors import *

from GUI.Windows.UpdateCodeWindow.EditFieldCopyable import EditFieldCopyable

import config


class UpdateCodeWindow(QDialog):

    def __init__(self, parent, pass_id, account, username, email, old_password, new_password):
        super().__init__(parent)
        self.parent = parent
        self.pass_id = pass_id
        self.account_value = account
        self.username_value = username
        self.email_value = email
        self.old_password_value = old_password
        self.new_password_value = new_password
        self.build_UI()
        self.show()

    def build_UI(self):

        self.account = EditFieldCopyable(self, "Account", False)
        self.username = EditFieldCopyable(self, "Username", False)
        self.email = EditFieldCopyable(self, "Email Address", False)
        self.oldPassword = EditFieldCopyable(self, "Old Password")
        self.newPassword = EditFieldCopyable(self, "New Password")

        self.account.setValue(self.account_value)
        self.username.setValue(self.username_value)
        self.email.setValue(self.email_value)
        self.oldPassword.setValue(self.old_password_value)
        self.newPassword.setValue(self.new_password_value)

        self.saveButton = QPushButton(self)
        self.saveButton.clicked.connect(self.handleSave)
        self.saveButton.setText("Save")

        self.cancelButton = QPushButton(self)
        self.cancelButton.clicked.connect(self.handleCancel)
        self.cancelButton.setText("Cancel")

        self.space = QLabel(self)

        buttons = QHBoxLayout()

        buttons.addWidget(self.cancelButton, 45)
        buttons.addWidget(self.saveButton, 45)
        buttons.addWidget(self.space, 10)

        layout = QVBoxLayout()

        layout.addWidget(self.account)
        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.oldPassword)
        layout.addWidget(self.newPassword)
        layout.addLayout(buttons)

        buttons.setMargin(0)
        buttons.setSpacing(10)

        layout.setMargin(20)
        layout.setSpacing(9)

        self.setLayout(layout)

        self.setMinimumWidth(370)

    def handleSave(self):

        try:
            config.db_admin.editPassword(
                self.pass_id,
                self.account.value,
                self.username.value,
                self.email.value,
                self.newPassword.value
            )

            self.parent.tab2.editPassword(self.pass_id,
                                          self.account.value,
                                          self.username.value,
                                          self.email.value,
                                          self.newPassword.value)

            QMessageBox.information(self, "Success", "Password updated successfully!")
            self.close()
        except PassAccountLengthError:
            QMessageBox.warning(self, "Error", "Account must contain between 4 and 48 characters!")
        except PassUsernameLengthError:
            QMessageBox.warning(self, "Error", "Username must contain less than 48 characters!")
        except PassEmailLengthError:
            QMessageBox.warning(self, "Error", "Email must contain less than 48 characters!")

    def handleCancel(self):
        self.close()

    def closeEvent(self, event):
            self.parent.setEnabled(True)
            self.parent.setWindowOpacity(1.)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()