from PyQt4.QtGui import QLineEdit


class MyLineEdit(QLineEdit):

    def __init__(self, parent, placeholder: str, isPassword=False):
        super().__init__(parent)

        self.parent = parent

        self.isEmpty = True
        self.isPassword = isPassword

        self.setStyleSheet("color: grey")
        self.setPlaceholderText(placeholder)

        self.setText(self.placeholderText())
        self.setCursorPosition(0)

        self.textEdited.connect(self.handleEdit)
        self.cursorPositionChanged.connect(self.handleClick)

    def handleEdit(self):
        if self.isEmpty:
            self.isEmpty = False
            if self.isPassword:
                self.setEchoMode(QLineEdit.Password)
            self.setStyleSheet("color: black")
            self.setText(self.text()[0])
        else:
            if self.text() == "":
                self.isEmpty = True
                if self.isPassword:
                    self.setEchoMode(QLineEdit.Normal)
                self.setStyleSheet("color: grey")
                self.setText(self.placeholderText())
                self.setCursorPosition(0)

    def handleClick(self):
        if self.isEmpty and self.getText() == "":
            self.setCursorPosition(0)

    def getText(self):
        if self.isEmpty:
            return ""
        else:
            return self.text()

    def clearText(self):
        self.setText("a")
        self.backspace()
