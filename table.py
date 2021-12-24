from cell import *


class Table():

    def __init__(self, row=5, col=5):
        self.__row = row
        self.__col = col

        self.__grid = self.initGrid()

    # Getters

    def getRow(self):
        return self.__row

    def getCol(self):
        return self.__col

    def getGrid(self):
        return self.__grid

    # Setters

    def setGrid(self, grid):
        self.__grid = grid

    def setRow(self, row):
        self.__row = row

    def setCol(self, col):
        self.__col = col

    # Methods

    def initGrid(self):
        grid = [[Cell() for col in range(self.__col)]
                for row in range(self.__row)]
        return grid

    def checkNeighbors(self, x, y):

        tab = [(x, y)]

        self.getGrid()[y][x].setChecked(True)

        top, bottom, left, right = [], [], [], []

        if y != 0 and self.getGrid()[y - 1][x].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y - 1][x].getChecked() == False:

            top = self.checkNeighbors(x, y - 1)

        if y != self.getRow() - 1 and self.getGrid()[y + 1][x].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y + 1][x].getChecked() == False:

            bottom = self.checkNeighbors(x, y + 1)

        if x != 0 and self.getGrid()[y][x - 1].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y][x - 1].getChecked() == False:

            left = self.checkNeighbors(x - 1, y)

        if x != self.getCol() - 1 and self.getGrid()[y][x + 1].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y][x + 1].getChecked() == False:

            right = self.checkNeighbors(x + 1, y)

        # self.getGrid()[y][x].setChecked(False) Makes the Highlight bug

        for i in top:
            tab.append(i)
        for i in bottom:
            tab.append(i)
        for i in left:
            tab.append(i)
        for i in right:
            tab.append(i)

        return tab

    def getNeighborsPos(self, x, y):

        positions = self.checkNeighbors(x, y)
        print(sorted(positions))

        return positions
