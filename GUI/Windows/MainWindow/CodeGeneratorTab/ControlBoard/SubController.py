from PyQt4.QtGui import *

from GUI.Components.TextSlider import TextSlider


class SubController(QGroupBox):

    checkBox: QCheckBox
    slider: TextSlider

    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title
        self.parent = parent
        # Central refers to GeneratorTab
        self.central = self.parent.parent.parent
        self.buildUI()

    def buildUI(self):

        self.checkBox = QCheckBox(self)
        self.checkBox.setText(self.title)
        self.checkBox.clicked.connect(self.handleCheckboxClicked)

        self.slider = TextSlider(self, 16)
        self.slider.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        layout.setMargin(1)
        layout.setSpacing(0)

    def handleSliders(self):
        if self.checkBox.isChecked():
            self.slider.setEnabled(True)
        else:
            self.slider.setEnabled(False)

    # Gets triggered when I press SubController's CheckBox by hand
    def handleCheckboxClicked(self):
        self.handleSliders()
        self.central.setupEdited()

    # Function that enables other components of program to edit CheckBox's state
    def setState(self, state):
        self.checkBox.setChecked(state)
        self.handleSliders()
