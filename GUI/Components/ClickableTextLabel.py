from PyQt4.QtCore import Qt, QEvent
from PyQt4.QtGui import QLabel


class ClickableTextLabel(QLabel):

    def __init__(self, parent, text):
        super().__init__(parent)
        self.text = text
        self.buildUI()

    def buildUI(self):

        self.setText(self.text)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setStyleSheet("color: blue;")
        self.enableMouseHover()
        self.mousePressEvent = self.handleClickEdit

    def handleClickEdit(self, event):
        print("clicked")

    def enableMouseHover(self):
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton:
                self.setStyleSheet("color: blue; text-decoration: underline;")
        elif event.type() == QEvent.Leave:
            self.setStyleSheet("color: blue; text-decoration: none;")
        return QLabel.eventFilter(self, source, event)
