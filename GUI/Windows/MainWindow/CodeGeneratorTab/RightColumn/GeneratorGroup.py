from PyQt4.QtGui import QGroupBox, QVBoxLayout, QPushButton, QLineEdit, QButtonGroup, QRadioButton


class GeneratorGroup(QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.central = self.parent.parent
        self.centralWindow = self.parent.parent.parent
        self.buildWidget()

    def buildWidget(self):

        self.setTitle("Generator Settings")

        self.saveOptions = QButtonGroup(self)

        self.buttonNew = QRadioButton("Create New Code")
        self.buttonNew.toggled.connect(lambda: self.buttonToggled(self.buttonNew))

        self.buttonUpdate = QRadioButton("Update Existing Code")
        self.buttonUpdate.toggled.connect(lambda: self.buttonToggled(self.buttonUpdate))

        self.saveOptions.addButton(self.buttonNew)
        self.saveOptions.addButton(self.buttonUpdate)

        self.code_to_edit = QLineEdit(self)
        self.code_to_edit.setText("(Select Code from View Tab)")
        self.code_to_edit.setReadOnly(True)
        self.code_to_edit.setEnabled(False)

        self.generatorButton = QPushButton(self)
        self.generatorButton.setText("Generate Code")
        self.generatorButton.setEnabled(False)
        self.generatorButton.clicked.connect(self.handleGenerateCode)

        layout = QVBoxLayout()
        layout.addWidget(self.buttonNew)
        layout.addWidget(self.buttonUpdate)
        layout.addWidget(self.code_to_edit)
        layout.addWidget(self.generatorButton)
        self.setLayout(layout)

    def handleGenerateCode(self, event):
        self.centralWindow.popUpNewCodeWindow()

    def resetRadioButtons(self):

        self.saveOptions.setExclusive(False)
        self.buttonUpdate.setChecked(False)
        self.buttonNew.setChecked(False)
        self.saveOptions.setExclusive(True)

    def buttonToggled(self, button):

        if button.isChecked():
            if button.text() == "Create New Code":
                self.generatorButton.setEnabled(True)
                self.code_to_edit.setEnabled(False)
            elif button.text() == "Update Existing Code":
                self.generatorButton.setEnabled(False)
                self.code_to_edit.setEnabled(True)
        else:
            if button.text() == "Update Existing Code":
                self.code_to_edit.setEnabled(False)

    def reflectChange(self):
        if not self.central.controlBoard.setupIsProper():
            self.buttonNew.setEnabled(False)
            self.buttonUpdate.setEnabled(False)
            self.generatorButton.setEnabled(False)
            self.code_to_edit.setEnabled(False)
        else:
            self.buttonNew.setEnabled(True)
            self.buttonUpdate.setEnabled(True)
            if self.buttonNew.isChecked():
                self.generatorButton.setEnabled(True)
            if self.buttonUpdate.isChecked():
                self.code_to_edit.setEnabled(True)
