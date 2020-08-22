from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QSlider, QLineEdit, QLabel


class NumberLineEdit(QGroupBox):

    slider: QSlider
    lineEdit: QLineEdit
    value: int

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.central = self.parent.parent
        self.value = 16
        self.buildUI()
        self.margin = 0
        self.spacing = 0
        self.stretchFactor = 0.8

    def buildUI(self):

        self.label = QLabel(self)
        self.label.setText(" Number of Characters:")

        self.valueField = QLineEdit(self)
        self.valueField.setAlignment(Qt.AlignCenter)
        self.valueField.textChanged.connect(self.handleValueChanged)

        self.setValue(self.value)

    # Takes care so that valueField will not get dumb values
    def protectValue(self):
        if self.valueField.text() == "":
            self.valueField.setText("0")
        elif not self.valueField.text().isdigit():
            self.valueField.setText(str(self.value))
        elif int(self.valueField.text()) > 48:
            self.valueField.setText("48")
        else:
            self.valueField.setText(str(int(self.valueField.text())))
            self.value = int(self.valueField.text())
        for i in range(3):
            self.parent.controllers[i].sub1.slider.maxValue = self.value
            self.parent.controllers[i].sub2.slider.maxValue = self.value

    def setValue(self, value):
        self.valueField.setText(str(value))
        self.protectValue()

    def handleValueChanged(self):
        self.protectValue()
        self.central.setupEdited()

    def setSize(self):
        availableSpace = [self.size().width() - 2 * self.margin, self.size().height() - 2 * self.margin]
        availableLabelSpace = [self.stretchFactor * (availableSpace[0] - self.spacing), availableSpace[1]]
        valueFieldSpace = [(1 - self.stretchFactor) * (availableSpace[0] - self.spacing), availableSpace[1] - 1]

        self.label.move(self.margin, self.margin)
        self.label.resize(*availableLabelSpace)

        self.valueField.move(self.margin + availableLabelSpace[0] + self.spacing, self.margin)
        self.valueField.resize(*valueFieldSpace)

        fontSizeLabel = min(0.05 * self.size().width(), 0.5 * self.size().height())
        self.label.setStyleSheet("font-size: {}pt;".format(fontSizeLabel))

        fontSizeValueField = min(0.075 * self.size().width(), 0.5 * self.size().height())
        self.valueField.setStyleSheet("font-size: {}pt;".format(fontSizeValueField))

    def resizeEvent(self, event):
        self.setSize()
