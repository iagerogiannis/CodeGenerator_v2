from PyQt5.QtWidgets import QGroupBox, QVBoxLayout

from GUI.Components.MyCheckBox import MyCheckBox
from GUI.Windows.MainWindow.CodeGeneratorTab.ControlBoard.SubController import SubController


class Controller(QGroupBox):

    def __init__(self, parent, title):
        super().__init__(parent)
        self.parent = parent
        # Central refers to GeneratorTab
        self.central = self.parent.parent
        self.title = title
        self.buildUI()

    def buildUI(self):

        self.checkBox = MyCheckBox(self, self.title)
        self.checkBox.clicked.connect(self.handleCheckboxClicked)

        self.sub1 = SubController(self, "ShiftOut")
        self.sub2 = SubController(self, "ShiftIn")

        self.sub1.setEnabled(False)
        self.sub2.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addWidget(self.sub1)
        layout.addWidget(self.sub2)
        self.setLayout(layout)

        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)

    def handleSubControllers(self):

        if self.checkBox.isChecked():
            self.sub1.setEnabled(True)
            self.sub2.setEnabled(True)
        else:
            self.sub1.setEnabled(False)
            self.sub2.setEnabled(False)

    def handleCheckboxClicked(self):

        if self.checkBox.checkState() == 1:
            self.checkBox.setCheckState(2)

        for i in range(len(self.central.keyboard.keys)):
            key = self.central.keyboard.keys[i]
            type = key.properties["type"]
            if type == self.title[:-1]:
                if self.checkBox.isChecked():
                    key.pressed = True
                else:
                    key.pressed = False
                key.stateChangedByCheckBox()

        self.handleSubControllers()

        self.central.setupEdited()
