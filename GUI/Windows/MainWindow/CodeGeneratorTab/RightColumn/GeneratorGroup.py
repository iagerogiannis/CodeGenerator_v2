from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QLineEdit, QButtonGroup, QRadioButton


class GeneratorGroup(QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.code_to_edit_data = [None, None, None, None, None]
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
        if self.buttonNew.isChecked():
            self.centralWindow.popUpNewCodeWindow()
        elif self.buttonUpdate.isChecked():
            self.centralWindow.popUpUpdateCodeWindow(*self.code_to_edit_data)

    def resetRadioButtons(self):

        self.saveOptions.setExclusive(False)
        self.buttonUpdate.setChecked(False)
        self.buttonNew.setChecked(False)
        self.saveOptions.setExclusive(True)

    def buttonToggled(self, button):

        if button.isChecked():
            if button.text() == "Create New Code":
                self.code_to_edit_data = [None, None, None, None, None]
                self.code_to_edit.setText("(Select Code from View Tab)")
                self.code_to_edit.setEnabled(False)
                self.generatorButton.setEnabled(True)
            elif button.text() == "Update Existing Code":
                self.generatorButton.setEnabled(False)
                self.code_to_edit.setEnabled(True)
                self.central.parent.switchToTab(1)
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

    def resetButtons(self):
        self.code_to_edit.setText("(Select Code from View Tab)")
        self.resetRadioButtons()
        self.generatorButton.setEnabled(False)

    def choseCodeToUpdate(self, pass_id, account, username, email, password):

        self.code_to_edit_data = [pass_id, account, username, email, password]
        self.buttonUpdate.setChecked(True)
        self.code_to_edit.setText("{}; {}; {};".format(account, username, email))
        self.code_to_edit.setCursorPosition(0)
        self.central.parent.switchToTab(0)
        self.generatorButton.setEnabled(True)
