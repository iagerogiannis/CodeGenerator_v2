from PyQt4.QtGui import QWidget, QLabel, QHBoxLayout, QLineEdit

from GUI.Components.ClickableTextLabel import ClickableTextLabel


class EditFieldCopyable(QWidget):

    def __init__(self, parent, title, copyable=True):
        super().__init__(parent)
        self.title = title
        self.value = ""
        self.copyable = copyable
        self.buildUI()

    def buildUI(self):

        self.titleLabel = QLabel()
        self.titleLabel.setText("{}:".format(self.title))

        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.handleTextChanged)

        if self.copyable:
            self.copyLabel = ClickableTextLabel(self, "Copy")
        else:
            self.copyLabel = QLabel(self)

        layout = QHBoxLayout()

        layout.addWidget(self.titleLabel, 45)
        layout.addWidget(self.lineEdit, 45)
        layout.addWidget(self.copyLabel, 10)

        layout.setMargin(1)
        layout.setSpacing(10)

        self.setLayout(layout)

    def setValue(self, value):
        self.lineEdit.setText(value)

    def handleTextChanged(self):
        self.value = self.lineEdit.text()
