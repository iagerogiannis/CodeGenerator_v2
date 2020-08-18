from PyQt4.QtGui import QWidget

import config
from GUI.Windows.MainWindow.CodeGeneratorTab.ControlBoard.ControlBoard import ControlBoard
from GUI.Windows.MainWindow.CodeGeneratorTab.ControlBoard.Controller import Controller
from GUI.Windows.MainWindow.CodeGeneratorTab.Keyboard.Keyboard import Keyboard
from GUI.Windows.MainWindow.CodeGeneratorTab.RightColumn.RightColumn import RightColumn
from Styles.styles import Style

from Generic.MyJsonLib import MyJsonLib as jsonlib


class CodeGeneratorTab(QWidget):
    keyboard: Keyboard
    controller: Controller
    myStyle: Style

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.myStyle = config.styles[0]
        self.buildUI()

    def buildUI(self):
        self.controlBoard = ControlBoard(self)
        self.keyboard = Keyboard(self)
        self.column = RightColumn(self)

    def getSetup(self):

        setup = {
            "id": 0,
            "Name": "",
            "User_id": 0,
            "Key_ids": [],
            "Letters": {
                "ShiftOut": 0,
                "ShiftIn": 0
            },
            "Numbers": {
                "ShiftOut": 0,
                "ShiftIn": 0
            },
            "Symbols": {
                "ShiftOut": 0,
                "ShiftIn": 0
            }
        }

        for key in self.keyboard.keys:
            if key.properties["type"] != "Secondary":
                if key.pressed:
                    setup["Key_ids"].append(key.properties["id"])

        for controller in self.controlBoard.controllers:
            if not controller.checkBox.isChecked():
                setup[controller.title]["ShiftOut"] = 0
                setup[controller.title]["ShiftIn"] = 0
            else:
                for sub in [controller.sub1, controller.sub2]:
                    if not sub.checkBox.isChecked():
                        setup[controller.title][sub.title] = 0
                    else:
                        setup[controller.title][sub.title] = sub.slider.value
                if setup[controller.title]["ShiftOut"] + setup[controller.title]["ShiftIn"] == 0:
                    for key in self.keyboard.keys:
                        if "{}s".format(key.properties["type"]) == controller.title:
                            if key.properties["id"] in setup["Key_ids"]:
                                setup["Key_ids"].remove(key.properties["id"])

        return setup

    def loadSetup(self, setup_id):

        def resetControllers():

            for i in range(len(self.controlBoard.controllers)):

                controller = self.controlBoard.controllers[i]

                controller.sub1.slider.setValue(0)
                controller.sub1.setState(False)

                controller.sub2.slider.setValue(0)
                controller.sub2.setState(False)

        def calculateCharacters():
            nonlocal selected_setup
            characters = 0
            for key_type in ["Letters", "Numbers", "Symbols"]:
                for shift in ["ShiftIn", "ShiftOut"]:
                    characters += selected_setup[key_type][shift]
            return characters

        resetControllers()

        file = "{}/{}".format("Database", "setups.json")
        selected_setup = jsonlib.locate_by_id(file, "id", setup_id)

        self.controlBoard.numberController.setValue(calculateCharacters())

        for i in range(len(self.keyboard.keys)):
            key = self.keyboard.keys[i]
            if key.properties["type"] != "Secondary":
                if key.properties["id"] in selected_setup["Key_ids"]:
                    self.keyboard.keys[i].pressed = True
                else:
                    self.keyboard.keys[i].pressed = False
                key.stateChangedByCheckBox()

            i += 1

        for type in ["Letter", "Number", "Symbol"]:
            self.keyboard.handleControllers(type)

        for i in range(len(self.controlBoard.controllers)):

            controller = self.controlBoard.controllers[i]

            if controller.checkBox.isChecked():

                controller.sub1.slider.setValue(selected_setup[controller.title]["ShiftOut"])

                if selected_setup[controller.title]["ShiftOut"] != 0:
                    controller.sub1.setState(True)
                else:
                    controller.sub1.setState(False)

                controller.sub2.slider.setValue(selected_setup[controller.title]["ShiftIn"])

                if selected_setup[controller.title]["ShiftIn"] != 0:
                    controller.sub2.setState(True)
                else:
                    controller.sub2.setState(False)

    def setupEdited(self):

        try:
            self.column.setupBox.reflectChange()
            self.column.generatorBox.reflectChange()
        except AttributeError:
            pass

    def resizeEvent(self, event):
        default_margin = 8
        default_spacing = 9

        horizontal_aspect_ratio = 0.75
        vertical_aspect_ratio = 0.6

        keyboard_width = horizontal_aspect_ratio * (self.size().width() - 2 * default_margin - default_spacing)
        keyboard_height = vertical_aspect_ratio * (self.size().height() - 2 * default_margin - default_spacing)

        self.keyboard.setSize(keyboard_width, keyboard_height)
        self.keyboard.move(default_margin + 1, default_margin + 1)

        control_board_width = self.keyboard.size().width()
        control_board_height = self.size().height() - self.keyboard.size().height() \
                               - 2 * default_margin - default_spacing

        self.controlBoard.resize(control_board_width, control_board_height)
        self.controlBoard.move(default_margin + 1, self.keyboard.size().height() + default_margin + default_spacing + 1)

        column_width = self.size().width() - self.keyboard.size().width() - 2 * default_margin - default_spacing - 1
        column_height = self.size().height() - default_margin

        self.column.resize(column_width, column_height)
        self.column.move(self.keyboard.size().width() + default_margin + default_spacing + 1, 2)