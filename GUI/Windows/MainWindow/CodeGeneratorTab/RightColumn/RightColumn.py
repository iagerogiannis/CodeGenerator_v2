from PyQt5.QtWidgets import QWidget, QVBoxLayout

from GUI.Windows.MainWindow.CodeGeneratorTab.RightColumn.GeneratorGroup import GeneratorGroup
from GUI.Windows.MainWindow.CodeGeneratorTab.RightColumn.SetupGroup import SetupGroup


class RightColumn(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.buildWidget()

    def buildWidget(self):

        self.setupBox = SetupGroup(self)
        self.generatorBox = GeneratorGroup(self)

        mainlayout = QVBoxLayout()
        mainlayout.setContentsMargins(1, 1, 1, 1)
        mainlayout.setSpacing(3)

        mainlayout.addWidget(self.setupBox)
        mainlayout.addWidget(self.generatorBox)

        self.setLayout(mainlayout)
