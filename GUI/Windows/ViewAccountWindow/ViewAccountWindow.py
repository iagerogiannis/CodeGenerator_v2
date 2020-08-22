from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap

from GUI.Windows.ViewAccountWindow.InfoField import InfoField
from GUI.Windows.ViewAccountWindow.RemoveAccountField import RemoveAccountField

import config


# # noinspection PyCallByClass,PyArgumentList
class ViewAccountWindow(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.childEdited = None
        self.edited = False
        self.username_value, self.email_value = config.db_admin.getUserData()
        self.build_UI()
        self.show()

    def build_UI(self):

        # Image --------------------------------------------------------------------------------------------------------
        image = QLabel()
        pixmap = QPixmap("Files/avatar.png")
        image.setPixmap(pixmap)
        image.setContentsMargins(0, 20, 0, 0)
        image.setAlignment(Qt.AlignCenter)

        # Title --------------------------------------------------------------------------------------------------------
        title = QLabel()
        title.setText("Account Info")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font: 25pt Cronus Round")
        title.setContentsMargins(10, 10, 10, 10)

        # Labels -------------------------------------------------------------------------------------------------------
        self.username = InfoField(self, "Username", self.username_value)
        self.email = InfoField(self, "Email Address", self.email_value)
        self.password = InfoField(self, "Password", "************")
        self.remove = RemoveAccountField(self)

        # Total Layout -------------------------------------------------------------------------------------------------
        layout = QVBoxLayout()

        layout.addWidget(image)
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.remove)

        self.setLayout(layout)

        layout.setContentsMargins(20, 20, 20, 20)
        self.setWindowTitle("Code Generator")
        self.setWindowIcon(QIcon("Files/app.ico"))
        self.setFixedSize(350, 435)

    def getEditedChild(self, current_child, edited):
        if self.edited:
            if self.childEdited:
                if not (self.childEdited.title == "Password" and current_child.title == "Password"):
                    self.childEdited.setFixedValue()
        self.childEdited = current_child
        self.edited = edited

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        self.parent.setWindowOpacity(1.)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if not self.edited:
                self.close()
            else:
                self.childEdited.setFixedValue()
            self.edited = False
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.edited:
                self.childEdited.handleDone()
