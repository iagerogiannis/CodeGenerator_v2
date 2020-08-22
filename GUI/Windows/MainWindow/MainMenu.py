from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QFileDialog

import config
from Generic.MyJsonLib import MyJsonLib as jsonlib


class MainMenu:

    def __init__(self, parent: QMainWindow):
        super().__init__()
        self.parent = parent
        self.centralWindow = self.parent
        self.buildMenu()

    def buildMenu(self):

        def buildFileMenu():

            nonlocal mainMenu

            fileMenu = mainMenu.addMenu("File")

            ImportCodesAction = QAction("Import Codes File", self.parent)
            ImportCodesAction.setStatusTip("")
            ImportCodesAction.triggered.connect(self.handleImportFile)

            ExportCodesAction = QAction("Export Codes File", self.parent)
            ExportCodesAction.setStatusTip("")
            ExportCodesAction.triggered.connect(self.handleExportFile)

            fileMenu.addAction(ImportCodesAction)
            fileMenu.addAction(ExportCodesAction)

        def buildAccountMenu():

            nonlocal mainMenu

            accountMenu = mainMenu.addMenu("Account")

            ViewAccountAction = QAction("View", self.parent)
            ViewAccountAction.setStatusTip("")
            ViewAccountAction.triggered.connect(self.handleViewAccount)

            LogOutAction = QAction("Log Out", self.parent)
            LogOutAction.setStatusTip("")
            LogOutAction.triggered.connect(self.handleLogOut)

            accountMenu.addAction(ViewAccountAction)
            accountMenu.addAction(LogOutAction)

        def buildHelpMenu():

            nonlocal mainMenu

            helpMenu = mainMenu.addMenu("Help")

            aboutAction = QAction("About", self.parent)
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

    def handleExportFile(self):
        data = self.parent.tab2.getTable().drop(["ID"], axis=1)
        filename = QFileDialog.getSaveFileName(self.parent, 'Export Codes File', 'CodesFile',
                                                              filter="JSON Files (*.json)")
        if filename[0] != '':
            jsonlib.export_data(data, filename[0])
            QMessageBox.information(self.parent, "Success", "Codes File Exported successfully!")

    def handleImportFile(self):
        filename = QFileDialog.getOpenFileName(self.parent, 'Import Codes File',
                                                              filter="JSON Files (*.json)")
        if filename[0] != '':
            codes_data = jsonlib.import_data(filename[0])
            for i in range(codes_data.shape[0]):
                config.db_admin.addPassword(*codes_data.iloc[[i]].values.tolist()[0])
                pass_id = str(int(config.db_admin.getLastIndex()))
                self.parent.tab2.addPassword(pass_id, *codes_data.iloc[[i]].values.tolist()[0])
            QMessageBox.information(self.parent, "Success", "Codes File Imported successfully!")
