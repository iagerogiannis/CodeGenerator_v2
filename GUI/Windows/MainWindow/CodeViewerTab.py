from PyQt4.QtCore import QEvent
from PyQt4.QtGui import QWidget, QTableWidget, QPushButton, QVBoxLayout, \
    QHBoxLayout, QAbstractItemView, QTableWidgetItem, QHeaderView, QMessageBox

import pyperclip
from pandas import DataFrame

from Generic.MyJsonLib import MyJsonLib as jsonlib

import config


# noinspection PyCallByClass
class CodeViewerTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.buildUI()
        self.selected_id = None
        self.setData(config.db_admin.getPasswords())

    def buildUI(self):

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Account', 'Username', 'Email', 'Password'])
        self.table.setSelectionBehavior(1)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.viewport().installEventFilter(self)
        self.table.itemSelectionChanged.connect(self.selected)
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        self.table.setColumnHidden(0, True)

        self.copyButton = QPushButton(self)
        self.copyButton.setText("Copy")
        self.copyButton.setEnabled(False)
        self.copyButton.clicked.connect(self.handleCopy)

        self.updateButton = QPushButton(self)
        self.updateButton.setText("Update")
        self.updateButton.setEnabled(False)
        self.updateButton.clicked.connect(self.handleUpdate)

        self.editButton = QPushButton(self)
        self.editButton.setText("Edit")
        self.editButton.setEnabled(False)
        self.editButton.clicked.connect(self.handleEdit)

        self.removeButton = QPushButton(self)
        self.removeButton.setText("Remove")
        self.removeButton.setEnabled(False)
        self.removeButton.clicked.connect(self.handleRemove)

        buttons = QHBoxLayout()
        buttons.setMargin(0)
        buttons.setSpacing(0)

        buttons.addWidget(self.copyButton)
        buttons.addWidget(self.updateButton)
        buttons.addWidget(self.editButton)
        buttons.addWidget(self.removeButton)

        mainlayout = QVBoxLayout()
        mainlayout.setMargin(0)

        mainlayout.addWidget(self.table)
        mainlayout.addLayout(buttons)
        mainlayout.setSpacing(2)

        self.setLayout(mainlayout)

    def addPassword(self, pass_id, account, username, email, password):

        data = self.getTable()

        data = data.append({"ID": pass_id,
                            "Account": account,
                            "Username": username,
                            "Email": email,
                            "Password": password
                            }, ignore_index=True)

        self.setData(data)

    def getTable(self):

        data = {"ID": [],
                "Account": [],
                "Username": [],
                "Email": [],
                "Password": [],
                }

        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                data[list(data.keys())[j]].append(self.table.item(i, j).text())

        return DataFrame(data)

    def setData(self, data):

        self.table.setRowCount(0)
        self.table.setRowCount(data.shape[0])
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(data.iloc[i, j]))

    def selected(self):
        selected_row = self.table.currentRow()
        try:
            self.selected_id = self.table.item(selected_row, 0).text()
        except AttributeError:
            self.selected_id = None

    def editPassword(self, pass_id, account, username, email, password):

        data = self.getTable()
        values = [account, username, email, password]

        for i, column in enumerate(['Account', 'Username', 'Email', 'Password']):
            data.loc[data["ID"] == pass_id, column] = values[i]

        self.clearSelection()
        self.disableButtons()
        self.setData(data)

    def handleCopy(self):
        pyperclip.copy(self.table.selectedItems()[3].text())

    def handleUpdate(self):
        pass

    def handleEdit(self):

        i = self.table.currentRow()

        (pass_id, account, username, email, password) = (self.table.item(i, 0).text(),
                                                         self.table.item(i, 1).text(),
                                                         self.table.item(i, 2).text(),
                                                         self.table.item(i, 3).text(),
                                                         self.table.item(i, 4).text())

        self.parent.popUpEditCodeWindow(pass_id, account, username, email, password)

    def handleRemove(self):

        config.db_admin.removePassword(self.selected_id)

        file = "{}/{}".format("Database", "salts.json")
        jsonlib.drop_by_id(file, "password_id", self.selected_id)

        data = self.getTable()
        data = data[data.ID != self.selected_id]
        self.clearSelection()
        self.disableButtons()
        self.setData(data)

        QMessageBox.information(self, "Success", "Password removed successfully!")

    def clearSelection(self):
        self.table.clearSelection()

    def enableButtons(self):
        self.copyButton.setEnabled(True)
        self.updateButton.setEnabled(True)
        self.editButton.setEnabled(True)
        self.removeButton.setEnabled(True)

    def disableButtons(self):
        self.copyButton.setEnabled(False)
        self.updateButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.removeButton.setEnabled(False)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress):
            if (source is self.table.viewport() and self.table.itemAt(event.pos()) is None):
                self.clearSelection()
                self.disableButtons()
            else:
                self.enableButtons()
        return QWidget.eventFilter(self, source, event)
