from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

import config


class ConfirmWindow(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.build_UI()
        self.show()

    def build_UI(self):

        self.labelText = QLabel()
        self.labelText.setText("Enter Password to Confirm Changes:")

        self.passLineEdit = QLineEdit()
        self.passLineEdit.setEchoMode(QLineEdit.Password)

        self.button = QPushButton()
        self.button.setText("Confirm")
        self.button.clicked.connect(self.handleConfirm)

        layout = QVBoxLayout()

        layout.addWidget(self.labelText)
        layout.addWidget(self.passLineEdit)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.setWindowTitle("Code Generator")

    def handleConfirm(self):
        if config.db_admin.validatePassword(self.passLineEdit.text()):
            self.accept()
        else:
            self.reject()
