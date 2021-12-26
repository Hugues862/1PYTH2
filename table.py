from os import system, name
from time import sleep
from cell import *


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class Table():

    def __init__(self, row=5, col=5, level=2):
        self.__row = row
        self.__col = col
        self.__level = level

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
        grid = [[Cell(self.__level) for col in range(self.__col)]
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

        self.getGrid()[y][x].setChecked(False)  # Makes the Highlight bug

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

        return positions

    def displayTable(self):
        print()
        display = [[[] for col in range(self.__col)]
                   for row in range(self.__row)]

        # Ajoute les objets Tree() a la listes
        for row in range(self.__row):
            for col in range(self.__col):
                display[row][col] = str(self.__grid[row][col].getState())
        # Affiche la liste avec comme espaceur " "
        for item in display:
            print(" ".join(item))

    def gravity(self):
        def isEmpty():
            empty = False
            for y in range(self.__row-1):
                for x in range(self.__col):
                    print(y, x)
                    if self.__grid[y][x].getState() == 0:
                        empty = True
            return empty

        def down():
            empty = False
            for y in range(self.__row):
                for x in range(self.__col):
                    if self.__grid[y][x].getState() == 0:  # vide
                        # case au dessus
                        empty = True
                        if self.__grid[y-1][x].getState() != 0 and y > 0:

                            self.__grid[y][x].setState(
                                self.__grid[y-1][x].getState())
                            self.__grid[y-1][x].setState(0)

                        # fin au dessus
                        if y == 0:
                            self.__grid[y][x].randomState(self.__level)
            if empty:
                down()

        down()

    def addState(self, x, y):  # Adds 1 to state in pos X Y in the grid

        self.__grid[y][x].setState(self.__grid[y][x].getState() + 1)

    def win(self):

        for i in self.__grid:

            for j in i:

                if j.getState() == 10:
                    return True
        return False
