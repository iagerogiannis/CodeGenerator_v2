from PyQt4.QtGui import QGroupBox, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QRadioButton
from PyQt4.QtCore import Qt

from Generic.MyJsonLib import MyJsonLib as jsonlib

from GUI.Components.MyLineEdit import MyLineEdit

import config


class SetupGroup(QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.central = self.parent.parent
        self.justSaved = False
        self.original_index = 0
        self.buildUI()

    def buildUI(self):

        self.setTitle("Setup Settings")

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.pressed.connect(self.handleSave)

        self.removeButton = QPushButton(self)
        self.removeButton.setText("Remove")
        self.removeButton.pressed.connect(self.handleRemove)

        self.buttonOverwrite = QRadioButton("Overwrite Selected Setup")
        self.buttonOverwrite.toggled.connect(lambda: self.radioButtonToggled(self.buttonOverwrite))

        self.buttonNew = QRadioButton("Save as New Setup")
        self.buttonNew.toggled.connect(lambda: self.radioButtonToggled(self.buttonNew))

        self.saveOptions = QButtonGroup(self)
        self.saveOptions.addButton(self.buttonOverwrite)
        self.saveOptions.addButton(self.buttonNew)

        self.setupName = MyLineEdit(self, "Give Setup Name:")
        self.setupName.setEnabled(False)

        self.edited = False
        self.editedFlag2 = False

        self.setupCombo = QComboBox(self)
        self.loadSetupsToCombo()
        self.setupCombo.currentIndexChanged.connect(self.handleSetupComboChanged)
        self.handleSetupComboChanged()

        buttons = QHBoxLayout()
        buttons.setMargin(0)
        buttons.setSpacing(0)
        buttons.addWidget(self.saveButton)
        buttons.addWidget(self.removeButton)

        layout = QVBoxLayout()
        layout.addWidget(self.setupCombo)
        layout.addWidget(self.buttonOverwrite)
        layout.addWidget(self.buttonNew)
        layout.addWidget(self.setupName)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def loadSetupsToCombo(self):
        file = "{}/{}".format("Database", "setups.json")
        i = 0
        for setup in (jsonlib.read_json(file)):
            if setup["User_id"] == config.db_admin.user_id or setup["User_id"] == 100:
                self.setupCombo.addItem(setup["Name"], setup["id"])
                self.setupCombo.setItemData(i, setup["id"], Qt.UserRole + 1)
                i += 1

    def reflectChange(self):

        if not self.edited:
            self.edited = True
            self.addEditedSetup()
        else:
            self.setButtonsState("by edit")

    def addEditedSetup(self):

        file = "{}/{}".format("Database", "setups.json")
        self.original_index = self.setupCombo.currentIndex()
        edited_id = jsonlib.next_index(file, "id")
        name = "{} (Edited)".format(self.setupCombo.currentText())
        self.setupCombo.addItem(name, edited_id)
        self.setupCombo.setCurrentIndex(self.setupCombo.count() - 1)

    def removeEditedSetup(self):
        self.setupCombo.removeItem(self.setupCombo.count() - 1)

    def setButtonsState(self, comboChangedBy):

        def byPress():

            self.saveOptions.setExclusive(False)

            self.buttonOverwrite.setChecked(False)
            self.buttonNew.setChecked(False)

            self.saveOptions.setExclusive(True)

            self.buttonOverwrite.setEnabled(False)
            self.buttonNew.setEnabled(False)

            self.saveButton.setEnabled(False)

            if self.setupCombo.currentIndex() != 0:
                self.removeButton.setEnabled(True)
            else:
                self.removeButton.setEnabled(False)

            self.setupName.setText("")
            self.setupName.setEnabled(False)

        def byEdit():

            if self.central.controlBoard.setupIsProper():
                if self.original_index != 0:
                    self.buttonOverwrite.setEnabled(True)
                self.buttonNew.setEnabled(True)
            else:
                self.buttonOverwrite.setEnabled(False)
                self.buttonNew.setEnabled(False)

        if comboChangedBy == "by press" or comboChangedBy == "by save":
            byPress()
        elif comboChangedBy == "by edit":
            byEdit()

    def radioButtonToggled(self, button):

        if button.isChecked():
            if button.text() == "Save as New Setup":
                self.setupName.setEnabled(True)
            elif button.text() == "Overwrite Selected Setup":
                self.setupName.setEnabled(False)
            self.saveButton.setEnabled(True)

    def handleSetupComboChanged(self):

        def loadSetup():
            index = self.setupCombo.currentIndex()
            setup_id = self.setupCombo.itemData(index, Qt.UserRole + 1)
            self.parent.parent.loadSetup(setup_id)

        # print("**********\nedited: {}\nedited2: {}\nsaved: {}".format(self.edited, self.editedFlag2, self.justSaved))

        if self.justSaved:
            # Refers to the case that a new setup gets added because of a new setup that I save
            # There are 3 cases:
            #   a. I save an unedited setup -> I do not need to remove the "{Setup} (Edited)"
            #   b. I save an edited setup   -> I need to remove the "{Setup} (Edited)"
            #                                  I also need to reset flags self.edited and self.editedFlag2
            #   c. I overwrite a setup      -> Remove "{Setup} (Edited)"
            # In the end I need to reset flag self.justSaved
            if self.edited:
                self.edited = False
                self.editedFlag2 = False
            self.justSaved = False
            changedBy = "by save"

        elif not self.edited and not self.editedFlag2:
            # Refers to the simple case that a saved setup is loaded and I choose another saved setup from combo box
            loadSetup()
            changedBy = "by press"

        elif self.edited and not self.editedFlag2:
            # Refers to the case that a selected saved setup gets changed because I edit keyboard or control board sett.
            # So a new setup named "{Setup} (Edited)" needs to be added.
            # Self.edited setter adds the new setup and selects it, so comboBoxChanged gets triggered
            self.editedFlag2 = True
            changedBy = "by edit"

        elif self.edited and self.editedFlag2 and not self.justSaved:
            # Refers to the case that I choose a setup from combo box while an edited setup is loaded
            # So I need to remove the last (edited) setup
            loadSetup()
            self.removeEditedSetup()
            self.edited = False
            self.editedFlag2 = False
            changedBy = "by press"

        else:
            print("I am an annoying little bug!")
            changedBy = "by bug"

        self.setButtonsState(changedBy)

    def handleSave(self):

        def handleSaveAsNew():
            nonlocal file, setup

            setup["Name"] = self.setupName.getText()
            setup["id"] = jsonlib.next_index(file, "id")

            jsonlib.append_to_json(setup, file)

            if self.edited:
                self.removeEditedSetup()

            self.setupCombo.addItem(setup["Name"], setup["id"])
            self.setupCombo.setItemData(self.setupCombo.count() - 1, setup["id"], Qt.UserRole + 1)

            self.setupCombo.setCurrentIndex(self.setupCombo.count() - 1)

        def handleOverwrite():

            nonlocal file, setup

            setup["id"] = self.setupCombo.itemData(self.original_index, Qt.UserRole + 1)
            setup["Name"] = self.setupCombo.itemData(self.original_index, 0)

            jsonlib.overwrite_by_id(file, "id", setup["id"], setup)

            self.justSaved = True
            self.setupCombo.setCurrentIndex(self.original_index)
            self.removeEditedSetup()

        file = "{}/{}".format("Database", "setups.json")
        setup = self.parent.parent.getSetup()
        setup["User_id"] = config.db_admin.user_id

        self.justSaved = True

        if self.buttonNew.isChecked():
            handleSaveAsNew()
        elif self.buttonOverwrite.isChecked():
            handleOverwrite()

    def handleRemove(self):

        file = "{}/{}".format("Database", "setups.json")
        index = self.setupCombo.currentIndex()
        self.setupCombo.setCurrentIndex(0)
        jsonlib.drop_by_id(file, "id", self.setupCombo.itemData(index, Qt.UserRole + 1))
        self.setupCombo.removeItem(index)
