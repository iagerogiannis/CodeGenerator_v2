from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QIcon, QLineEdit, QLabel

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
        self.newButton.setText("New Code")
        self.newButton.clicked.connect(self.handleNewCode)

        self.changeRowButton = QPushButton(self)
        self.changeRowButton.setText("Change Row")
        self.changeRowButton.clicked.connect(self.handleChangeRow)

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save Code")
        self.saveButton.clicked.connect(self.handleSaveCode)

        codelayout = QHBoxLayout()
        codelayout.addWidget(self.label, 1)
        codelayout.addWidget(self.codeLine, 2)

        buttons = QHBoxLayout()
        buttons.addWidget(self.newButton)
        buttons.addWidget(self.changeRowButton)
        buttons.addWidget(self.saveButton)

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(codelayout)
        mainlayout.addLayout(buttons)

        codelayout.setMargin(1)
        codelayout.setSpacing(4)

        buttons.setMargin(0)
        buttons.setSpacing(5)

        mainlayout.setMargin(20)
        mainlayout.setSpacing(7)

        self.setLayout(mainlayout)
        self.setWindowTitle("Code Generator")
        self.setWindowIcon(QIcon("Files/app.ico"))

        self.setMinimumWidth(350)

    def handleSaveCode(self, event):
        self.closedDueToSave = True
        self.close()
        self.parent.popUpSaveCodeWindow(self.codeLine.text())

    def handleChangeRow(self, event):
        new_code = Generator.rearange(self.codeLine.text())
        self.codeLine.setText(new_code)

    def handleNewCode(self, event):
        new_code = Generator.produce_code(self.parent.tab1.getSetup())
        self.codeLine.setText(new_code)

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        if not self.closedDueToSave:
            self.parent.setWindowOpacity(1.)
