from PyQt4.QtGui import QMessageBox, QDialog, QLabel, QCheckBox, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from PyQt4.QtCore import QTimer, Qt

import config
from Generic.MyJsonLib import MyJsonLib as jsonlib
from GUI.Windows.ConfirmWindow import ConfirmWindow


class DeleteWindow(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.build_UI()
        self.show()

    def build_UI(self):

        self.text = QLabel(self)
        self.text.setText("If you remove your account all of your saved data will be lost. \n"
                          "Are you sure you want to proceed?")

        self.cb = QCheckBox(self)
        self.cb.setText("Export Codes File")
        self.cb.clicked.connect(self.handleCheckboxClicked)
        self.cb.setChecked(True)

        self.path = QLineEdit(self)
        self.path.setPlaceholderText("Insert Path:")

        self.select = QPushButton("Select")
        self.select.clicked.connect(self.handleSelectPath)

        self.proceed = QPushButton("Proceed")
        self.proceed.clicked.connect(self.handleProceed)

        pathLayout = QHBoxLayout()

        pathLayout.addWidget(self.path)
        pathLayout.addWidget(self.select)

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.text)
        mainLayout.addWidget(self.cb)
        mainLayout.addLayout(pathLayout)
        mainLayout.addWidget(self.proceed)

        self.setLayout(mainLayout)

    def handleSelectPath(self):

        # data = self.parent.tab2.getTable().drop(["ID"], axis=1)
        filename = QFileDialog.getSaveFileNameAndFilter(self, 'Export Codes File', 'CodesFile',
                                                              filter="JSON Files (*.json)")
        if filename[0] != '':
            self.path.setText(filename[0])

    def handleProceed(self):

        def delete_and_exit():
            self.confirm = ConfirmWindow(self)
            if self.confirm.exec_() == QDialog.Accepted:
                config.db_admin.removeUser()
                self.close()
                self.parent.close()
                self.parent.parent.logOut()
                QMessageBox.information(self, "Success", "Your account has been successfully removed! We hope to see you soon again!")
            else:
                QMessageBox.warning(self, "Error", "Wrong Password!")

        if self.cb.isChecked():
            if self.path.text() != "":
                data = self.parent.parent.tab2.getTable()
                jsonlib.export_data(data, self.path.text())
                delete_and_exit()
            else:
                self.complaint()
        else:
            delete_and_exit()

    def handleCheckboxClicked(self):

        if self.cb.isChecked():
            self.path.setEnabled(True)
            self.select.setEnabled(True)
        else:
            self.path.setEnabled(False)
            self.select.setEnabled(False)

    def complaint(self):

        def fade():
            nonlocal unfade, counter, interval, times
            self.path.setEnabled(False)
            if counter != times:
                counter += 1
                QTimer.singleShot(interval, unfade)
            else:
                lastUnfade()

        def unfade():
            nonlocal fade, interval
            self.path.setEnabled(True)
            QTimer.singleShot(interval, fade)

        def lastUnfade():
            self.path.setEnabled(True)

        interval = 100
        times = 3
        counter = 0
        fade()
