from PyQt4.QtGui import QCheckBox


class MyCheckBox(QCheckBox):

    def __init__(self, parent, title):
        super().__init__(parent)
        self.parent = parent
        self.setTristate(True)
        self.setText(title)
