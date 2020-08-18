from PyQt4.QtGui import QGroupBox

from GUI.Windows.MainWindow.CodeGeneratorTab.Keyboard.PrimaryKey import PrimaryKey
from GUI.Windows.MainWindow.CodeGeneratorTab.Keyboard.SecondaryKey import SecondaryKey
from Styles.styles import KeyboardStyle
from config import primary_key_properties, secondary_key_properties


class Keyboard(QGroupBox):

    keys: []
    myStyle: KeyboardStyle
    key_size: int

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.myStyle = parent.myStyle["keyboardStyle"]
        self.buildUI()

    def buildUI(self):

        def appendPrimaryKey():
            nonlocal prim_counter
            self.keys.append(PrimaryKey(self, primary_key_properties[prim_counter]))
            prim_counter += 1

        def appendSecondaryKey():
            nonlocal sec_counter
            self.keys.append(SecondaryKey(self, secondary_key_properties[sec_counter]))
            sec_counter += 1

        prim_counter = 0
        sec_counter = 0

        self.keys = []
        for i in range(13):
            appendPrimaryKey()
        for i in range(2):
            appendSecondaryKey()
        for i in range(13):
            appendPrimaryKey()
        appendSecondaryKey()
        for i in range(11):
            appendPrimaryKey()
        for i in range(2):
            appendSecondaryKey()
        for i in range(10):
            appendPrimaryKey()
        appendSecondaryKey()

    def setSize(self, width_max, height_max):

        def calculate_key_size():
            nonlocal width_max, height_max, a, gap

            key_size_1 = (width_max - 15 * gap) / (13 + a)
            key_size_2 = (height_max - 5 * gap) / 4

            size = int(min(key_size_1, key_size_2))

            if size % 2 == 1:
                size -= 1

            if size < 32:
                gap = 1
            else:
                gap = 2

            return size

        def calculate_actual_dimensions():

            actual_width = (13 + a) * self.key_size + 15 * gap
            actual_height = 4 * self.key_size + 5 * gap

            return actual_width, actual_height

        def calculate_secondary_sizes():

            secondary_key_size = [0 for i in range(6)]

            secondary_key_size[0] = width - 13 * self.key_size - 15 * gap
            secondary_key_size[1] = width - 13 * self.key_size - 15 * gap
            secondary_key_size[2] = int((width - 11 * self.key_size - 14 * gap) *
                                        secondary_key_properties[2]["aspectRatio"][0] /
                                        secondary_key_properties[2]["aspectRatio"][1])
            secondary_key_size[3] = width - 11 * self.key_size - 14 * gap - secondary_key_size[2]
            secondary_key_size[4] = int((width - 10 * self.key_size - 13 * gap) *
                                        secondary_key_properties[4]["aspectRatio"][0] /
                                        secondary_key_properties[4]["aspectRatio"][1])
            secondary_key_size[5] = width - 10 * self.key_size - 13 * gap - secondary_key_size[4]

            return secondary_key_size

        def resize_keys():

            def redifine_key(j, size):
                nonlocal position
                self.keys[j].setGeometry(*position, *size)
                position[0] += self.keys[j].size().width() + gap

            def new_line():
                nonlocal position
                position = [gap, position[1] + self.key_size + gap]

            position = [gap, gap]

            for i in range(13):
                redifine_key(i, [self.key_size, self.key_size])
            redifine_key(13, [secondary_key_sizes[0], self.key_size])
            new_line()
            redifine_key(14, [secondary_key_sizes[1], self.key_size])
            for i in range(15, 28):
                redifine_key(i, [self.key_size, self.key_size])
            new_line()
            redifine_key(28, [secondary_key_sizes[2], self.key_size])
            for i in range(29, 40):
                redifine_key(i, [self.key_size, self.key_size])
            redifine_key(40, [secondary_key_sizes[3], self.key_size])
            new_line()
            redifine_key(41, [secondary_key_sizes[4], self.key_size])
            for i in range(42, 52):
                redifine_key(i, [self.key_size, self.key_size])
            redifine_key(52, [secondary_key_sizes[5], self.key_size])

        gap = 0
        a = secondary_key_properties[0]["aspectRatio"][0] / secondary_key_properties[0]["aspectRatio"][1]

        self.key_size = calculate_key_size()
        width, height = calculate_actual_dimensions()
        secondary_key_sizes = calculate_secondary_sizes()

        resize_keys()

        self.resize(width, height + 1)

    def handleControllers(self, type):

        totalKeys = 0
        activeKeysNum = 0

        for i in range(len(self.keys)):
            if self.keys[i].properties["type"] == type:
                totalKeys += 1
                if self.keys[i].pressed:
                    activeKeysNum += 1

        if activeKeysNum == totalKeys:
            controllerCB_state = 2
        elif activeKeysNum == 0:
            controllerCB_state = 0
        else:
            controllerCB_state = 1

        for i in range(3):
            if self.parent.controlBoard.controllers[i].title == "{}s".format(type):
                self.parent.controlBoard.controllers[i].checkBox.setCheckState(controllerCB_state)
                self.parent.controlBoard.controllers[i].handleSubControllers()
