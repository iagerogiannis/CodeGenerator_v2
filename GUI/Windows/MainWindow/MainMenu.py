from PyQt4 import QtGui


class MainMenu:

    def __init__(self, parent: QtGui.QMainWindow):
        super().__init__()
        self.parent = parent
        self.centralWindow = self.parent
        self.buildMenu()

    def buildMenu(self):

        def buildFileMenu():

            nonlocal mainMenu

            fileMenu = mainMenu.addMenu("File")

            ImportCodesAction = QtGui.QAction("Import Codes File", self.parent)
            ImportCodesAction.setStatusTip("")

            ExportCodesAction = QtGui.QAction("Export Codes File", self.parent)
            ExportCodesAction.setStatusTip("")

            fileMenu.addAction(ImportCodesAction)
            fileMenu.addAction(ExportCodesAction)

        def buildAccountMenu():

            nonlocal mainMenu

            accountMenu = mainMenu.addMenu("Account")

            ViewAccountAction = QtGui.QAction("View", self.parent)
            ViewAccountAction.setStatusTip("")
            ViewAccountAction.triggered.connect(self.handleViewAccount)

            LogOutAction = QtGui.QAction("Log Out", self.parent)
            LogOutAction.setStatusTip("")
            LogOutAction.triggered.connect(self.handleLogOut)

            accountMenu.addAction(ViewAccountAction)
            accountMenu.addAction(LogOutAction)

        def buildHelpMenu():

            nonlocal mainMenu

            helpMenu = mainMenu.addMenu("Help")

            aboutAction = QtGui.QAction("About", self.parent)
            aboutAction.setStatusTip("Shows information about Code Generator")
            aboutAction.triggered.connect(self.handleAbout)


            helpMenu.addAction(aboutAction)

        mainMenu = self.parent.menuBar()

        buildFileMenu()
        buildAccountMenu()
        buildHelpMenu()

        self.parent.statusBar()

    def handleViewAccount(self):
        self.centralWindow.popUpViewAccountWindow()

    def handleAbout(self):
        self.centralWindow.popUpAboutWindow()

    def handleLogOut(self):
        self.parent.logOut()
