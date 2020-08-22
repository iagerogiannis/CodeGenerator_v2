from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap


# # noinspection PyCallByClass,PyArgumentList
class AboutWindow(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.build_UI()
        self.show()
        self.setFixedSize(self.size())

    def build_UI(self):

        # Logo --------------------------------------------------------------------------------------------------------
        image = QLabel()
        pixmap = QPixmap("Files/logo256.png")
        image.setPixmap(pixmap)
        image.setContentsMargins(0, 20, 0, 0)
        image.setAlignment(Qt.AlignCenter)

        title = QLabel()
        # title.setText("IAG Technologies")
        title.setText("IAG Solutions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font: 25pt Caveman; font-weight: bold ; color: #1c003f")
        title.setContentsMargins(10, 10, 10, 10)

        logoLayout = QVBoxLayout()
        logoLayout.addWidget(image)
        logoLayout.addWidget(title)

        # Info -------------------------------------------------------------------------------------------------------
        self.application = QLabel(self)
        self.application.setText("Code Generator")
        self.application.setStyleSheet("font: 25pt Cronus Round")

        self.version = QLabel(self)
        self.version.setText("Version 2.1.0")
        self.version.setStyleSheet("font: 11pt")

        self.built_on = QLabel(self)
        self.built_on.setText("Built on August, 2020")
        self.built_on.setStyleSheet("font: 11pt")

        self.developed_by = QLabel(self)
        self.developed_by.setText("Developed by IAGerogiannis")
        self.developed_by.setStyleSheet("font: 11pt")

        infoLayout = QVBoxLayout()
        infoLayout.addWidget(self.application)
        infoLayout.addWidget(self.version)
        infoLayout.addWidget(self.built_on)
        infoLayout.addWidget(self.developed_by)

        # Total Layout -------------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(logoLayout)
        mainLayout.addLayout(infoLayout)
        self.setLayout(mainLayout)

        mainLayout.setContentsMargins(30, 30, 30, 30)
        mainLayout.setSpacing(0)
        logoLayout.setContentsMargins(0, 0, 0, 0)
        logoLayout.setSpacing(5)
        infoLayout.setContentsMargins(10, 10, 10, 10)
        infoLayout.setSpacing(5)

        self.setWindowTitle("Code Generator")
        self.setWindowIcon(QIcon("Files/app.ico"))

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        self.parent.setWindowOpacity(1.)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
