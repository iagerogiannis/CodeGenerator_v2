from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QLabel


class ClickableTextLabel(QLabel):

    def __init__(self, parent, initial_text, handleClickEvent=None):
        super().__init__(parent)
        self.setText(initial_text)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setStyleSheet("color: blue;")
        self.enableMouseHover()
        self.mousePressEvent = handleClickEvent

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
