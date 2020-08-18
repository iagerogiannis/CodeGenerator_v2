import sys
from PyQt4.QtGui import QMainWindow, QIcon, QTabWidget

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

    def popUpNewCodeWindow(self):
        self.setEnabled(False)
        self.setWindowOpacity(.5)
        new_code = Generator.produce_code(self.tab1.getSetup())
        self.newCodeWindow = NewCodeWindow(self, new_code)

    def popUpViewAccountWindow(self):
        self.setEnabled(False)
        self.setWindowOpacity(.5)
        self.viewAccountWindow = ViewAccountWindow(self)

    def popUpSaveCodeWindow(self, password):
        self.setEnabled(False)
        self.setWindowOpacity(.5)
        a = True
        if a:
            self.saveCodeWindow = SaveCodeWindow(self, password)
        else:
            self.saveCodeWinow = UpdateCodeWindow(self)

    def popUpAboutWindow(self):
        self.setEnabled(False)
        self.setWindowOpacity(.5)
        self.aboutWindow = AboutWindow(self)

    def logOut(self):
        self.return_to_login = True
        self.close()

    def closeEvent(self, event):
        if not self.return_to_login:
            sys.exit()
