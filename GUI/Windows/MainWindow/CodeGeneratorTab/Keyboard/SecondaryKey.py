from PyQt4 import QtGui, QtCore
from typing_extensions import TypedDict

from Styles.styles import KeyStyle


class SecondaryKeyProperties(TypedDict):
    id: int
    text: str
    side: str
    aspectRatio: float


class SecondaryKey(QtGui.QLabel):

    parent: QtGui.QGroupBox
    properties: SecondaryKeyProperties
    key_size: []
    myStyle: KeyStyle

    def __init__(self, parent, properties):

        super().__init__(parent)
        self.parent = parent
        self.properties = properties
        self.key_size = [10, 10]
        self.myStyle = parent.myStyle["keyStyle"]
        self.build()

    def build(self):

        self.setStyleSheet("font-family: {};"
                           "font-size: {}px;"
                           "background-color: {};"
                           "color: {};"
                           .format(self.myStyle["fontFamily"],
                                   str(int(.25 * self.key_size[1])),
                                   self.myStyle["colors"]["inactive"]["background"],
                                   self.myStyle["colors"]["inactive"]["text"]))
        if self.properties["side"] == "right":
            self.setText(self.properties["text"] + "  ")
            self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if self.properties["side"] == "left":
            self.setText("  " + self.properties["text"])
            self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

    def resizeEvent(self, event):
        self.key_size = [self.size().width(), self.size().height()]
        if self.key_size[0] > 0 and self.key_size[1] > 0:
            self.build()
