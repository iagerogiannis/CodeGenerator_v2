from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtGui import QIcon

from Generic.Generator import Generator


class NewCodeWindow(QDialog):

    def __init__(self, parent, code):
        super().__init__(parent)
        self.parent = parent
        self.code = code
        self.closedDueToSave = False
        self.build_UI()
        self.show()

    def build_UI(self):

        self.label = QLabel(self)
        self.label.setText("Generated Code:")

        self.codeLine = QLineEdit(self)
        self.codeLine.setText(self.code)
        self.codeLine.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.codeLine.setReadOnly(True)

        self.newButton = QPushButton(self)
        self.newButton.setText("New")
        self.newButton.clicked.connect(self.handleNew)

        self.shuffleButton = QPushButton(self)
        self.shuffleButton.setText("Shuffle")
        self.shuffleButton.clicked.connect(self.handleShuffle)

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.handleSave)

        codelayout = QHBoxLayout()
        codelayout.addWidget(self.label, 1)
        codelayout.addWidget(self.codeLine, 2)

        buttons = QHBoxLayout()
        buttons.addWidget(self.newButton)
        buttons.addWidget(self.shuffleButton)
        buttons.addWidget(self.saveButton)

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(codelayout)
        mainlayout.addLayout(buttons)

        codelayout.setContentsMargins(1, 1, 1, 1)
        codelayout.setSpacing(4)

        buttons.setContentsMargins(0, 0, 0, 0)
        buttons.setSpacing(5)

        mainlayout.setContentsMargins(20, 20, 20, 20)
        mainlayout.setSpacing(7)

        self.setLayout(mainlayout)
        self.setWindowTitle("Code Generator")
        self.setWindowIcon(QIcon("Files/app.ico"))

        self.setMinimumWidth(350)

    def handleSave(self, event):
        self.parent.password = self.codeLine.text()
        self.accept()

    def handleShuffle(self, event):
        new_code = Generator.rearange(self.codeLine.text())
        self.codeLine.setText(new_code)

    def handleNew(self, event):
        new_code = Generator.produce_code(self.parent.tab1.getSetup())
        self.codeLine.setText(new_code)

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        self.parent.setWindowOpacity(1.)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()