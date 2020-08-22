import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QDialog

from GUI.Windows.AboutWindow import AboutWindow
from GUI.Windows.MainWindow.CodeGeneratorTab.CodeGeneratorTab import CodeGeneratorTab
from GUI.Windows.MainWindow.CodeViewerTab import CodeViewerTab
from GUI.Windows.MainWindow.MainMenu import MainMenu
from GUI.Windows.NewCodeWindow import NewCodeWindow
from GUI.Windows.SaveCodeWindow.SaveCodeWindow import SaveCodeWindow
from GUI.Windows.UpdateCodeWindow.UpdateCodeWindow import UpdateCodeWindow
from GUI.Windows.ViewAccountWindow.ViewAccountWindow import ViewAccountWindow
from Generic.Generator import Generator


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.return_to_login = False

        self.setWindowTitle("Code Generator")
        self.setWindowIcon(QIcon("Files/app.ico"))

        self.mainMenu = MainMenu(self)

        self.tabs = QTabWidget(self)

        self.tab1 = CodeGeneratorTab(self)
        self.tab2 = CodeViewerTab(self)

        self.tabs.addTab(self.tab1, "Code Generator")
        self.tabs.addTab(self.tab2, "Code Viewer")

        self.setCentralWidget(self.tabs)

        self.resize(900, 419)
        self.setMinimumHeight(230)

        self.show()

    def switchToTab(self, index):
        self.tabs.setCurrentIndex(index)

    def popUp(self):
        self.setEnabled(False)
        self.setWindowOpacity(.5)

    def popUpViewAccountWindow(self):
        self.popUp()
        self.viewAccountWindow = ViewAccountWindow(self)

    def popUpNewCodeWindow(self):
        self.password = ""
        self.popUp()
        new_code = Generator.produce_code(self.tab1.getSetup())
        self.newCodeWindow = NewCodeWindow(self, new_code)
        if self.newCodeWindow.exec_() == QDialog.Accepted:
            self.saveCodeWindow = SaveCodeWindow(self, self.password)

    def popUpUpdateCodeWindow(self, pass_id, account, username, email, old_password):
        self.password = ""
        self.popUp()
        new_code = Generator.produce_code(self.tab1.getSetup())
        self.newCodeWindow = NewCodeWindow(self, new_code)
        if self.newCodeWindow.exec_() == QDialog.Accepted:
            self.updateCodeWindow = UpdateCodeWindow(self, pass_id, account, username, email, old_password,
                                                     self.password)
        self.tab1.column.generatorBox.resetButtons()

    def popUpEditCodeWindow(self, pass_id, account, username, email, password):
        self.popUp()
        self.EditCodeWindow = SaveCodeWindow(self, password, pass_id, account, username, email, True)

    def popUpAboutWindow(self):
        self.popUp()
        self.aboutWindow = AboutWindow(self)

    def logOut(self):
        self.return_to_login = True
        self.close()

    def closeEvent(self, event):
        if not self.return_to_login:
            sys.exit()
