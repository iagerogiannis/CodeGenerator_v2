from PyQt5.QtWidgets import QLineEdit, QSlider, QGroupBox
from PyQt5.QtCore import Qt
from GUI.Components.MySlider import MySlider


class TextSlider(QGroupBox):

    slider: MySlider
    lineEdit: QLineEdit
    value: int

    def __init__(self, parent, maxValue):
        super().__init__(parent)
        self.parent = parent
        self.central = self.parent.parent.parent.parent
        self.buildUI()
        self.value = 0
        self.maxValue = maxValue
        self.setValue(self.value)
        self.margin = 0
        self.spacing = 0
        self.sliderMargin = [10, 3]
        self.stretchFactor = 0.8

    def buildUI(self):

        self.slider = MySlider(self, self.handleChangedSlider)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit.textEdited.connect(self.handleGhangedLineEdit)

    def setValue(self, value):
        self.value = value
        self.slider.customSetValue(value)
        self.lineEdit.setText(str(value))
        self.protectLineEditValue()

    def protectLineEditValue(self):
        if self.lineEdit.text() == "":
            self.value = 0
        elif not self.lineEdit.text().isdigit():
            self.lineEdit.setText(str(self.value))
        elif int(self.lineEdit.text()) > self.maxValue:
            self.value = self.maxValue
            self.lineEdit.setText(str(self.maxValue))
        else:
            self.value = int(self.lineEdit.text())

    def handleChangedSlider(self):
        self.value = self.slider.value()
        self.lineEdit.setText(str(self.value))
        self.central.setupEdited()

    def handleGhangedLineEdit(self):
        self.protectLineEditValue()
        self.slider.customSetValue(self.value)
        self.central.setupEdited()

    def setSize(self):
        availableSpace = [self.size().width() - 2 * self.margin, self.size().height() - 2 * self.margin]
        availableSliderSpace = [self.stretchFactor * (availableSpace[0] - self.spacing), availableSpace[1]]
        actualSliderSpace = [availableSliderSpace[0] - 2 * self.sliderMargin[0],
                             availableSliderSpace[1] - 2 * self.sliderMargin[1]]
        lineEditSpace = [(1 - self.stretchFactor) * (availableSpace[0] - self.spacing), availableSpace[1] - 1]

        self.slider.move(self.margin + self.sliderMargin[0], self.margin + self.sliderMargin[1])
        self.slider.resize(*actualSliderSpace)

        self.lineEdit.move(self.margin + availableSliderSpace[0] + self.spacing, self.margin)
        self.lineEdit.resize(*lineEditSpace)

        font_size = min(0.07 * self.size().width(), 0.45 * self.size().height())
        self.lineEdit.setStyleSheet("font-size: {}pt;".format(font_size))

    def resizeEvent(self, event):
        self.setSize()

    @property
    def maxValue(self):
        return self.__maxValue

    @maxValue.setter
    def maxValue(self, maxValue):
        self.__maxValue = maxValue
        self.slider.setMaximum(self.maxValue)
