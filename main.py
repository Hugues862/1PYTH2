from table import *
from score import *

from random import *
from tkinter import *
from time import sleep, time
import math
from threading import *


class Game():

    def __init__(self, width, height, timer):
        self.__width = width
        self.__height = height

        self.__fontMult = 0.7
        self.__win = False

        self.__root = Tk()
        self.__root.configure(background='white')
        self.__root.bind('<Button-1>', self.updateClick)
        self.__root.bind('<Escape>', self.escapeKey)
        self.__root.attributes("-fullscreen", True)

        self.__root.title = ("Just Get Ten")

        # FRAME1
        self.__frame1 = Frame(self.__root)
        self.__frame1.grid(row=0, column=0)

        self.__canvas = Canvas(self.__frame1)
        self.__canvas.config(width=width, height=height,
                             highlightthickness=0, bd=0, bg="black")
        self.__canvas.pack()

        # FRAME2
        self.__frame2 = Frame(self.__root)
        self.__frame2.grid(
            row=0, column=1, padx=self.__width/10)

        self.__items = []
        self.__items.append(
            Label(self.__frame2, text="Just Get Ten", font=("Courier", int(44*self.__fontMult))))

        self.__items.append(
            Label(self.__frame2, text="High Score : ", font=("Courier", int(44*self.__fontMult))))

        self.__items.append(
            Label(self.__frame2, text="Score : ", font=("Courier", int(34*self.__fontMult))))

        self.__items.append(
            Label(self.__frame2, text="Max : ", font=("Courier", int(34*self.__fontMult))))

        self.__items.append(Scale(self.__frame2, orient='horizontal',
                                  from_=3, to=10, resolution=1, label="Cells", length=200, font=("Courier", int(24*self.__fontMult))))
        self.__items[4].set(5)

        self.__items.append(Button(
            self.__frame2, text="New Grid", command=self.newTable, font=("Courier", int(24*self.__fontMult))))

        self.__items.append(
            Label(self.__frame2, text="Time Left", font=("Courier", int(40*self.__fontMult))))
        self.__items.append(
            Label(self.__frame2, text="00:00", font=("Courier", int(40*self.__fontMult))))

        for item in self.__items:
            item.pack(padx=0, pady=5)

        self.__table = self.initTable()
        self.__cellCount = self.__items[4].get()
        self.__timer = None
        self.__defaultTime = timer

        self.__stopThread = False
        self.__timerThread = Thread(
            target=self.countdown, args=(self.__defaultTime,))
        self.__timerThread.start()

        self.update()

        self.__root.mainloop()

    # Getters

    def escapeKey(self, event=None):
        self.__root.destroy()
        return "break"

    def getWin(self):
        return self.__win

    def getScore(self):
        val = 0
        for y in range(self.__cellCount):
            for x in range(self.__cellCount):
                val += self.__table.getGrid()[y][x].getState()

        self.__score = val
        return str(self.__score)

    def getMax(self):
        val = 0
        for y in range(self.__table.getRow()):
            for x in range(self.__table.getCol()):
                if self.__table.getGrid()[y][x].getState() > val:
                    val = self.__table.getGrid()[y][x].getState()
        self.__max = val
        return str(val)

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getCellCount(self):
        return self.__cellCount

    def getTable(self):
        return self.__table

    # Setters

    def setWin(self, win):
        self.__win = win

    def setWidth(self, width):
        self.__width = width

    def setHeight(self, height):
        self.__height = height

    def setCellCount(self, cellCount):
        self.__cellCount = cellCount

    def setTable(self, table):
        self.__table = table

    # Methods

    def initTable(self):
        self.__cellCount = self.__items[4].get()
        return Table(self.__cellCount, self.__cellCount)

    def newTable(self):
        self.__table = self.initTable()

        self.update()

    def update(self):
        if self.__timer == "00:00":
            self.__root.destroy()

        else:
            self.__table.gravity()
            self.__table.displayTable()
            self.drawGrid()
            self.updateLabels()

            self.setWin(self.__table.win())

            if self.getWin() == True:

                self.__root.destroy()

    def updateLabels(self):
        self.__items[1].config(text="High Score : " + getHighScore())
        self.__items[2].config(text="Score : "+self.getScore())
        self.__items[3].config(text="Max : "+self.getMax())

        self.__items[7].config(text=self.__timer)

    def countdown(self, t):
        if self.__timer == None:
            while t:
                t -= 1
                mins, secs = divmod(t, 60)
                self.__timer = '{:02d}:{:02d}'.format(mins, secs)
                print(self.__timer, end="\r")
                sleep(1)
                self.updateLabels()
                if self.__stopThread == True:
                    self.__stopThread = False
                    break

    def updateClick(self, event):
        self.__mouseX = event.x
        self.__mouseY = event.y

        x = math.floor(((self.__mouseX - 0) / (self.__width - 0)) *
                       (self.__table.getCol() - 0) + 0)
        y = math.floor(((self.__mouseY - 0) / (self.__height - 0)) *
                       (self.__table.getRow() - 0) + 0)

        if event.x_root < self.__width:
            self.highlightCells(x, y)

    def highlightCells(self, x, y):
        neighborPos = self.getTable().getNeighborsPos(
            x, y)  # List of x and y of all neighbors
        if len(neighborPos) > 1:
            # Boolean of whether it's highlighted or not
            val = self.__table.getGrid()[neighborPos[0]
                                         [1]][neighborPos[0][0]].getHighlight()

            if val:
                self.removeCells(neighborPos[1:])
                self.__table.getGrid()[neighborPos[0][1]][neighborPos[0][0]].setHighlight(
                    False)
                self.addUp(neighborPos[0])

            for item in neighborPos:
                if val == False:
                    self.__table.getGrid()[item[1]][item[0]].setHighlight(
                        True)  # If not then add highlight
            del neighborPos

        self.update()

    def removeCells(self, items):
        for item in items:
            self.__table.getGrid()[item[1]][item[0]].setState(0)

    def addUp(self, item):
        val = self.__table.getGrid()[item[1]][item[0]].getState()
        self.__table.getGrid()[item[1]][item[0]].setState(val+1)
        self.__table.getGrid()[item[1]][item[0]].changeColor()

    def drawGrid(self):

        coef = ((self.__table.getCol()/100)+1)*1
        self.__canvas.delete("all")

        tRow = self.__table.getCol()
        tCol = self.__table.getRow()

        sizeW = self.__width/tRow
        sizeH = self.__height/tCol

        for row in range(tRow):
            for col in range(tCol):
                color = self.__table.getGrid()[row][col].getColor()
                text = self.__table.getGrid()[row][col].getState()
                highlighted = self.__table.getGrid()[row][col].getHighlight()

                if highlighted:
                    self.__canvas.create_rectangle(
                        col*sizeW+(10/coef), row*sizeH+(10/coef), col*sizeW+sizeW-(10/coef), row*sizeH+sizeH-(10/coef), fill="black", outline="black")
                else:
                    self.__canvas.create_rectangle(
                        col*sizeW, row*sizeH, col*sizeW+sizeW, row*sizeH+sizeH, fill=color, outline="black")

                self.__canvas.create_text(
                    (col*sizeW)+sizeW*0.5, (row*sizeH)+sizeW*0.5, text=text, font=("Purisa", int(38/coef)), fill="white")


g = Game(800, 800, 200)
