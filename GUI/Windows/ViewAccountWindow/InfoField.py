from PyQt4.QtGui import QWidget, QLabel, QHBoxLayout

from GUI.Components.ClickableTextLabel import ClickableTextLabel


class InfoField(QWidget):

    def __init__(self, parent, title, value, editEvent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.editEvent = editEvent
        self.buildUI()

    def buildUI(self):

        self.titleLabel = QLabel()
        self.titleLabel.setText("{}:".format(self.title))

        self.valueLabel = QLabel()
        self.valueLabel.setText(self.value)
        self.valueLabel.setStyleSheet("font-weight: bold;")

        self.editLabel = ClickableTextLabel(self, "Edit", self.editEvent)

        layout = QHBoxLayout()

        layout.addWidget(self.titleLabel, 4)
        layout.addWidget(self.valueLabel, 9)
        layout.addWidget(self.editLabel, 1)

        self.setLayout(layout)
