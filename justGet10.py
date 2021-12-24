from random import *
from tkinter import *


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

        self.__state = 0
        self.__color = ""

        self.randomState()
        self.changeColor()

    def getInfo(self):
        return self.__state, self. __color

    def getColorDict(self):
        return self.__colorDict

    def getState(self):
        return self.__state

    def getColor(self):
        return self.__color

    def setState(self, n):
        assert n >= 0 and n <= 10
        self.__state = n

    def setColor(self, color):
        self.__color = color

    def randomState(self):
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


class Table():

    def __init__(self, row=5, col=5):
        self.__row = row
        self.__col = col

        self.__grid = self.initGrid()

    def getRow(self):
        return self.__row

    def getCol(self):
        return self.__col

    def initGrid(self):
        grid = [[Cell() for col in range(self.__col)]
                for row in range(self.__row)]
        return grid

    def getGrid(self):
        return self.__grid

    def setGrid(self, grid):
        self.__grid = grid


class gui():
    def __init__(self, width, height, cellCount):
        self.__width = width
        self.__height = height
        self.__cellCount = cellCount

        self.__root = Tk()
        self.__root.title = ("Game")

        # FRAME1
        self.__frame1 = Frame(self.__root)
        self.__frame1.grid(row=0, column=0)

        self.__canvas = Canvas(self.__frame1)
        self.__canvas.config(width=width, height=height,
                             highlightthickness=0, bd=0, bg="black")
        self.__canvas.pack()

        # FRAME2
        self.__frame2 = Frame(self.__root)
        self.__frame2.grid(row=0, column=1, padx=self.__width/10)

        self.__lbl1 = Label(self. __frame2, text="Jeux")
        self.__lbl1.pack(padx=10, pady=10)

        self.__table = self.initTable(self.__cellCount)

        self.update()

        self.__root.mainloop()

    def initTable(self, cellCount):
        return Table(cellCount, cellCount)

    def update(self):
        self.drawGrid()

    def drawGrid(self):
        tRow = self.__table.getCol()
        tCol = self.__table.getRow()

        sizeW = self.__width/tRow
        sizeH = self.__height/tCol

        for row in range(tRow):
            for col in range(tCol):
                self.__canvas.create_rectangle(
                    col*sizeW, row*sizeH, col*sizeW+sizeW, row*sizeH+sizeH, fill=self.__table.getGrid()[row][col].getColor(), outline="black")
                self.__canvas.create_text(
                    (col*sizeW)+sizeW*0.5, (row*sizeH)+sizeW*0.5, text=self.__table.getGrid()[row][col].getState(), font=("Purisa", 32))


g = gui(800, 800, 5)
