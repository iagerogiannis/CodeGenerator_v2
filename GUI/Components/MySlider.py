from PyQt4.QtGui import *


class MySlider(QSlider):

    def __init__(self, parent, valueChangedEvent = lambda: None):
        super().__init__(parent)
        self.valueChangedEvent = valueChangedEvent
        self.valueChanged.connect(self.valueChangedEvent)

    def customSetValue(self, p_int):
        self.valueChanged.disconnect(self.valueChangedEvent)
        self.setValue(p_int)
        self.valueChanged.connect(self.valueChangedEvent)
