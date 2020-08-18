from PyQt4.QtGui import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

from GUI.Windows.UpdateCodeWindow.EditFieldCopyable import EditFieldCopyable


class UpdateCodeWindow(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.build_UI()
        self.show()

    def build_UI(self):

        self.account = EditFieldCopyable(self, "Account", False)
        self.username = EditFieldCopyable(self, "Username", False)
        self.email = EditFieldCopyable(self, "Email Address", False)
        self.oldPassword = EditFieldCopyable(self, "Old Password")
        self.newPassword = EditFieldCopyable(self, "New Password")

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save")

        self.cancelButton = QPushButton(self)
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

    def closeEvent(self, event):
            self.parent.setEnabled(True)
            self.parent.setWindowOpacity(1.)
