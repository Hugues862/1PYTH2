from random import *


class Cell():

    def __init__(self, level):
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
        self.__diff = {
            1: {
                0: 0,
                1: 0.4,
                2: 0.7,
                3: 0.95,
                4: 1
            },
            2: {
                0: 0,
                1: 0.1,
                2: 0.3,
                3: 0.6,
                4: 1
            }
        }
        # State of cell
        self.__state = 0
        # color of cell
        self.__color = ""
        self.__highlighted = False
        self.__checked = False
        self.__level = level

        self.randomState(self.__level)
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

    def randomState(self, diff):
        '''Selects a random state for the cell

        Uses probabilities.
        '''
        rdm = random()

        for i in range(1, len(self.__diff[diff])):
            if self.__diff[diff][i-1] <= rdm <= self.__diff[diff][i]:
                self.setState(i)

    def changeColor(self):
        self.setColor(self.__colorDict[self.__state])
        return
