from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit


class EditField(QWidget):

    def __init__(self, parent, title, value=""):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.buildUI()

    def buildUI(self):

        self.titleLabel = QLabel()
        self.titleLabel.setText("{}:".format(self.title))

        self.lineEdit = QLineEdit()
        self.lineEdit.setText(self.value)
        self.lineEdit.textChanged.connect(self.handleTextChanged)

        layout = QHBoxLayout()

        layout.addWidget(self.titleLabel, 1)
        layout.addWidget(self.lineEdit, 2)

        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(3)

        self.setLayout(layout)

    def handleTextChanged(self):
        self.value = self.lineEdit.text()
