from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout

from GUI.Windows.MainWindow.CodeGeneratorTab.ControlBoard.Controller import Controller
from GUI.Windows.MainWindow.CodeGeneratorTab.ControlBoard.NumberLineEdit import NumberLineEdit


class ControlBoard(QGroupBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.buildUI()

    def buildUI(self):
        self.controllers = [Controller(self, "Letters"),
                            Controller(self, "Numbers"),
                            Controller(self, "Symbols")]
        self.numberController = NumberLineEdit(self)

        controllersLayout = QHBoxLayout()
        controllersLayout.setContentsMargins(1, 1, 1, 1)
        controllersLayout.setSpacing(1)

        for controller in self.controllers:
            controllersLayout.addWidget(controller)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.numberController, 17)
        mainLayout.addLayout(controllersLayout, 83)

        self.setLayout(mainLayout)

        controllersLayout.setContentsMargins(0, 0, 0, 0)
        controllersLayout.setSpacing(1)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

    # Compares the sum of the values of sliders with the value of character numbers of lineedit
    def setupIsProper(self):

        num = 0

        for controller in self.controllers:
            if controller.checkBox.isChecked():
                for sub in [controller.sub1, controller.sub2]:
                    if sub.checkBox.isChecked():
                        num += sub.slider.value

        if num != self.numberController.value or num == 0:
            return False
        else:
            return True
