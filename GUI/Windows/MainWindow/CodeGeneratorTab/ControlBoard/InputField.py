from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit


class InputField(QGroupBox):

    description: QLabel
    lineEdit: QLineEdit

    def __init__(self, parent, value):
        super().__init__(parent)
        self.value = value
        self.buildUI()

    def buildUI(self):

        self.description = QLabel(self)
        self.description.setGeometry(2, 0, 100, 20)
        self.description.setText(" Total Characters")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(self.description.width(), 0, 40, 20))
        self.lineEdit.setText(str(self.value))
        self.lineEdit.textEdited.connect(self.handleChangedValue)

        self.resize(self.description.width() + self.lineEdit.width(), self.lineEdit.height() + 1)

    def handleChangedValue(self):
        if self.lineEdit.text() == "":
            self.value = 0
        elif not self.lineEdit.text().isdigit():
            self.lineEdit.setText(str(self.value))
        else:
            self.value = int(self.lineEdit.text())
