from PyQt5.QtWidgets import QGroupBox, QLabel
from PyQt5.QtCore import Qt, QEvent

from typing_extensions import TypedDict

from Styles.styles import KeyStyle


class PrimaryKeyProperties(TypedDict):
    id: int
    type: str
    shiftOut: str
    shiftIn: str


class PrimaryKey(QGroupBox):

    parent: QGroupBox
    properties: PrimaryKeyProperties
    key_size: int
    pressed: bool
    myStyle: KeyStyle

    def __init__(self, parent, properties, pressed=False):

        super().__init__(parent)

        self.parent = parent
        # Central refers to GeneratorTab
        self.central = self.parent.parent
        self.key_size = 10
        self.properties = properties
        self.myStyle = parent.myStyle["keyStyle"]
        self.parts = [QLabel(self) for i in range(4)]
        self.pressed = pressed

        self.enableMouseHover()
        self.mousePressEvent = self.handlePress
        self.mouseReleaseEvent = self.handleRelease

    def buildKey(self, state):

        def build(offset, color1, color2):

            def combineParts():

                self.parts[0].move(offset, offset)
                self.parts[1].move(offset, self.key_size / 2)
                self.parts[2].move(self.key_size / 2, offset)
                self.parts[3].move(self.key_size / 2, self.key_size / 2)

                for i in range(4):
                    self.parts[i].resize(self.key_size / 2 - offset, self.key_size / 2 - offset)

            def setText():

                self.parts[0].setText(self.properties["shiftIn"])
                self.parts[0].setAlignment(Qt.AlignCenter)

                if self.properties["type"] != "Letter":
                    self.parts[1].setText(self.properties["shiftOut"])
                    self.parts[1].setAlignment(Qt.AlignCenter)

            def setStyle():

                nonlocal color1, color2

                StyleSheet = "font-family: {}; " \
                             "font-size: {}px; " \
                             "background-color: {}; " \
                             "color: {}".format(self.myStyle["fontFamily"],
                                                str(int(0.3 * (self.key_size - 2 * offset))), color1, color2)

                for i in range(4):
                    self.parts[i].setStyleSheet(StyleSheet)

            combineParts()
            setText()
            setStyle()

        if state == "active":
            build(0,
                  self.myStyle["colors"]["active"]["background"],
                  self.myStyle["colors"]["active"]["text"])
        elif state == "inactive":
            build(0,
                  self.myStyle["colors"]["inactive"]["background"],
                  self.myStyle["colors"]["inactive"]["text"])
        elif state == "onPress":
            build(self.myStyle["offset"],
                  self.myStyle["colors"]["onPress"]["background"],
                  self.myStyle["colors"]["onPress"]["text"])
        elif state == "onHover":
            build(0,
                  self.myStyle["colors"]["onHover"]["background"],
                  self.myStyle["colors"]["onHover"]["text"])

    def enableMouseHover(self):
        self.setMouseTracking(True)
        for i in range(4):
            self.parts[i].setMouseTracking(True)
        self.installEventFilter(self)

    def handlePress(self, event):
        self.buildKey("onPress")

    def handleRelease(self, event):
        self.pressed = not self.pressed
        self.stateChangedByPress()

    def eventFilter(self, source, event):
        if not self.pressed:
            if event.type() == QEvent.MouseMove:
                if event.buttons() == Qt.NoButton:
                    self.buildKey("onHover")
            elif event.type() == QEvent.Leave:
                self.buildKey("inactive")
        return QLabel.eventFilter(self, source, event)

    def resizeEvent(self, event):
        self.key_size = self.size().width()
        if self.key_size > 0:
            if self.pressed:
                state = "active"
            else:
                state = "inactive"
            self.buildKey(state)

    def stateChanged(self):
        if self.pressed:
            self.buildKey("active")
        else:
            self.buildKey("inactive")

    def stateChangedByPress(self):
        self.stateChanged()
        self.parent.handleControllers(self.properties["type"])
        self.central.setupEdited()

    def stateChangedByCheckBox(self):
        self.stateChanged()
