from random import *


class Cell():

    def __init__(self):
        self.__colorDict = {
            1: "#31CD32",
            2: "#4068E1",
            3: "#FF8C00",
            4: "#FF0000",
            5: "#8FBC8E",
            6: "#FF00FF",
            7: "#9400D3",
            8: "#5B00F7",
            9: "#32008F",
            0: "#000000"
        }
        # State of cell
        self.__state = 0
        # color of cell
        self.__color = ""
        self.__highlighted = False
        self.__checked = False

        self.randomState()
        self.changeColor()

    # Getters

    def getInfo(self):
        return self.__state, self. __color

    def getColorDict(self):
        return self.__colorDict

    def getState(self):
        return self.__state

    def getColor(self):
        return self.__color

    def getHighlight(self):
        return self.__highlighted

    def getChecked(self):
        return self.__checked

    # Setters

    def setHighlight(self, val):
        self.__highlighted = val

    def setState(self, n):
        self.__state = n
        self.__highlighted = False
        self.changeColor()

    def setColor(self, color):
        self.__color = color

    def setChecked(self, state):
        self.__checked = state

    # Methods

    def randomState(self):
        '''Selects a random state for the cell

        Uses probabilities.
        '''
        rdm = random()

        if rdm <= 0.4:
            self.setState(1)
            return

        if rdm <= 0.7:
            self.setState(2)
            return

        if rdm <= 0.95:
            self.setState(3)
            return

        if rdm <= 1:
            self.setState(4)
            return

    def changeColor(self):
        self.setColor(self.__colorDict[self.__state])
        return
