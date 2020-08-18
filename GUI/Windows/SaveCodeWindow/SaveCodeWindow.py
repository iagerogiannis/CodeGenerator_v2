from PyQt4.QtGui import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox

from GUI.Windows.SaveCodeWindow.EditField import EditField
import config

import pyperclip


# noinspection PyCallByClass,PyArgumentList,PyBroadException
class SaveCodeWindow(QDialog):

    def __init__(self, parent, pass_code):
        super().__init__(parent)
        self.parent = parent
        self.pass_code = pass_code
        self.build_UI()
        self.show()

    def build_UI(self):

        self.account = EditField(self, "Account")
        self.username = EditField(self, "Username")
        self.email = EditField(self, "Email Address")
        self.password = EditField(self, "Password", self.pass_code)

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

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        self.parent.setWindowOpacity(1.)

    def handleSave(self):

        config.db_admin.addPassword(
            self.account.value,
            self.username.value,
            self.email.value,
            self.password.value
        )

        pass_id = str(int(config.db_admin.getLastIndex()))

        self.parent.tab2.addPassword(pass_id, self.account.value, self.username.value,
                                     self.email.value, self.password.value)
        QMessageBox.information(self, "Success", "Password registered successfully!")
        self.close()

    def handleCopy(self):
        pyperclip.copy(self.password.value)

    def handleCancel(self):
        self.close()
