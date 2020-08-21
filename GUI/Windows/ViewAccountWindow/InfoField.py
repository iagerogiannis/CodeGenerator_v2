from PyQt4.QtGui import QWidget, QLabel, QHBoxLayout, QDialog, QMessageBox

from GUI.Components.MyLineEdit import MyLineEdit

from GUI.Components.ClickableTextLabel import ClickableTextLabel
from GUI.Windows.ConfirmWindow import ConfirmWindow

import config
from Errors.DatabaseErrors import *


class InfoField(QWidget):

    def __init__(self, parent, title, value):
        super().__init__(parent)
        self.parent = parent
        self.title = title
        self.value = value
        self.new_value = value
        self.times_pressed_done = 0
        self.buildUI()

    def buildUI(self):

        self.titleLabel = QLabel()
        self.titleLabel.setText("{}:".format(self.title))

        self.valueLabel = QLabel()
        self.valueLabel.setText(self.value)
        self.valueLabel.setStyleSheet("font-weight: bold;")

        self.editLabel = ClickableTextLabel(self, "Edit", self.handlePressed)

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.titleLabel, 30)
        self.layout.addWidget(self.valueLabel, 50)
        self.layout.addWidget(self.editLabel, 20)

        self.setLayout(self.layout)

    def resetLayout(self):

        number_of_widgets = self.layout.count()

        for i in range(number_of_widgets):
            self.layout.removeItem(self.layout.itemAt(0))

    def turnToEditable(self):

        self.resetLayout()

        self.valueLabel.deleteLater()
        if self.title == "Password":
            self.valueLineEdit = MyLineEdit(self, "Enter new Password:", True)
        else:
            self.valueLineEdit = MyLineEdit(self, "Enter new {}:".format(self.title))

        self.valueLineEdit.setFocus()

        self.layout.addWidget(self.titleLabel, 285)
        self.layout.addWidget(self.valueLineEdit, 515)
        self.layout.addWidget(self.editLabel, 200)

        self.editLabel.setText("Done")

    def setFixedValue(self):

        self.resetLayout()

        self.valueLineEdit.deleteLater()
        self.valueLabel = QLabel()
        self.valueLabel.setStyleSheet("font-weight: bold;")
        if self.title != "Password":
            self.valueLabel.setText(self.value)
        else:
            self.valueLabel.setText("************")

        self.layout.addWidget(self.titleLabel, 30)
        self.layout.addWidget(self.valueLabel, 50)
        self.layout.addWidget(self.editLabel, 20)

        self.editLabel.setText("Edit")
        self.times_pressed_done = 0
        self.parent.edited = False

    def handlePressed(self, event):

        if self.editLabel.text() == "Edit":
            self.handleEdit()
            self.parent.getEditedChild(self, True)
        else:
            self.handleDone()
            if self.title != "Password":
                self.parent.getEditedChild(self, False)
            else:
                if self.times_pressed_done == 1:
                    self.parent.getEditedChild(self, True)

    def handleEdit(self):

        self.turnToEditable()

    def handleDone(self):

        if self.title != "Password":

            self.new_value = self.valueLineEdit.text()
            try:
                title = self.title.lower()
                if title == "email address":
                    title = "email"
                config.db_admin.checkUserData(title, self.new_value)
                self.confirm = ConfirmWindow(self)
                if self.confirm.exec_() == QDialog.Accepted:
                    self.value = self.new_value
                    config.db_admin.editUser(title, self.value)
                    QMessageBox.information(self, "Success", "{} updated succesfully!".format(self.title))
                else:
                    QMessageBox.warning(self, "Error", "Wrong Password!")
            except EmptyUsernameError:
                QMessageBox.warning(self, "Error", "Username may not be blank!")
            except InvalidCharactersInUsernameError:
                QMessageBox.warning(self, "Error", "Username may contain only letters (A-Z, a-z), "
                                                   "numbers (0-9) and underscore (_)!")
            except UsernameUsedError:
                QMessageBox.warning(self, "Error", "Username is already used!")
            except EmailUsedError:
                QMessageBox.warning(self, "Error", "Email Address is already used!")
            except UsernameLengthError:
                QMessageBox.warning(self, "Error", "Username must contain between 6 and 48 characters!")
            except EmailLengthError:
                QMessageBox.warning(self, "Error", "Email Address must contain between 6 and 48 characters!")
            self.setFixedValue()

        else:

            self.times_pressed_done = (self.times_pressed_done + 1) % 2
            if self.times_pressed_done == 1:
                self.new_value = self.valueLineEdit.text()
                self.valueLineEdit.setPlaceholderText("Retype new Password:")
                self.valueLineEdit.clearText()
            else:
                if self.new_value == self.valueLineEdit.text():
                    try:
                        config.db_admin.checkUserData(self.title.lower(), self.new_value)
                        self.confirm = ConfirmWindow(self)
                        if self.confirm.exec_() == QDialog.Accepted:
                            self.value = self.new_value
                            config.db_admin.editUser(self.title.lower(), self.value)
                            QMessageBox.information(self, "Success", "Password updated succesfully!")
                        else:
                            QMessageBox.warning(self, "Error", "Wrong Password!")
                    except PasswordLengthError:
                        QMessageBox.warning(self, "Error", "Password must contain between 6 and 48 characters!")
                else:
                    QMessageBox.warning(self, "Error", "Passwords do not match!")
                self.setFixedValue()

