from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QHBoxLayout, QLabel

from GUI.Components.ClickableTextLabel import ClickableTextLabel

import config


class RemoveAccountField(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.buildUI()

    def buildUI(self):

        self.empty = QLabel(self)

        self.text = ClickableTextLabel(self, "Remove Account")
        self.text.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text.mousePressEvent = self.handleRemoveAccount

        layout = QHBoxLayout()

        layout.addWidget(self.empty, 4)
        layout.addWidget(self.text, 1)

        self.setLayout(layout)

    def handleRemoveAccount(self, event):
        config.db_admin.removeUser()
