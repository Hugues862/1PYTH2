from os import error
from table import *
import score
import timer

from random import *
from tkinter import *
from tkinter import ttk
from time import sleep, time
import math
import threading
from functools import partial


"""
        Summary
        
            Parameters:
            
            
            Returns:
            
"""



def clear():
    """
    Clears the console for better clarity and reading.
    """

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
class Game():

    def __init__(self, width, height):

        clear()

        self.__width = width
        self.__height = height
        self.__fontMult = 0.7

        self.__win = False
        self.__score = 0
        self.__defaultTime = 60
        self.__game = None
        self.__level = 1
        self.__updateThread = True

        self.__root = Tk()
        self.__root.configure(background='white')
        self.__root.bind('<Button-1>', self.updateClick)
        self.__root.bind('<Escape>', self.escapeKey)
        self.__root.attributes("-fullscreen", True)

        self.__root.title = ("Just Get Ten")

        # BASE

        self.__base = Frame(self.__root)
        self.__base.grid(row=0, column=0)

        self.changeMenu(0)

        self.__root.mainloop()

    # Getters

    def escapeKey(self, event=None):
        self.destroy()

    def getMax(self):
        val = 0
        for y in range(self.__table.getRow()):
            for x in range(self.__table.getCol()):
                if self.__table.getGrid()[y][x].getState() > val:
                    val = self.__table.getGrid()[y][x].getState()
        self.__max = val
        return str(val)

    def getTimer(self):
        return self.__timerThread.getTimer()

    # Setters

    def setDefaultTimer(self, time):
        self.__defaultTime = time

    def setLevel(self, level):
        self.__level = level

    # Methods

    def initTable(self):
        self.__cellCount = self.__items[4].get()
        return Table(self.__level, self.__cellCount, self.__cellCount)

    def newTable(self):

        self.__table = self.initTable()
        self.updateHighscore()
        self.__score = 0
        self.startCountdown()
        self.update()

    def frameDisplay(self):

        for widget in self.__base.winfo_children():
            widget.destroy()

        if self.__display == 0:
            title = "Just Get Ten"

        if self.__display == 2:

            if self.__win:
                title = "YOU WIN"
            else:
                title = "YOU LOSE"

        if self.__display == 0 or self.__display == 2:  # Menu

            self.__game = False

            # Menu Frame

            self.__menuItems = []

            self.__menuItems.append(
                Label(self.__base, text=title, font=("Courier", int(60*self.__fontMult))))

            self.__menuItems.append(
                Label(self.__base, text="High Score : " + score.getHighScore(), font=("Courier", int(44*self.__fontMult))))

            self.__menuItems.append(
                Label(self.__base, text="Score : " + str(self.__score), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(
                self.__base, text="New Game", command=partial(self.changeMenu, 1), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(
                Label(self.__base, text="Select Time", font=("Courier", int(44*self.__fontMult))))

            self.__menuItems.append(Button(
                self.__base, text="1 min", command=partial(self.setDefaultTimer, 60), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(
                self.__base, text="3 min", command=partial(self.setDefaultTimer, 180), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(
                self.__base, text="Endless", command=partial(self.setDefaultTimer, -1), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(
                Label(self.__base, text="Select Difficulty", font=("Courier", int(44*self.__fontMult))))

            self.__menuItems.append(Button(
                self.__base, text="Easy", command=partial(self.setLevel, 1), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(
                self.__base, text="Hard", command=partial(self.setLevel, 2), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(
                self.__base, text="Harder", command=partial(self.setLevel, 3), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(
                Label(self.__base, text="Press ESC to exit", font=("Courier", int(30*self.__fontMult))))

            for i in range(len(self.__menuItems)):
                self.__menuItems[i].grid(row=i, column=0)

        if self.__display == 1:  # Game

            self.__game = True
            self.__win = False
            self.__score = 0

            # Game Frame

            self.__frame1 = Frame(self.__base)
            self.__frame1.grid(row=0, column=0, )

            self.__canvas = Canvas(self.__frame1)
            self.__canvas.config(width=self.__width, height=self.__height,
                                 highlightthickness=0, bd=0, bg="black")
            self.__canvas.pack()

            # User Frame

            self.__frame2 = Frame(self.__base)
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
                self.__frame2, text="New Grid", command=self.reset, font=("Courier", int(24*self.__fontMult))))

            self.__items.append(
                Label(self.__frame2, text="Time Left", font=("Courier", int(40*self.__fontMult))))
            self.__items.append(
                Label(self.__frame2, text="00:00", font=("Courier", int(40*self.__fontMult))))

            self.__items.append(
                Label(self.__frame2, text="Select Time", font=("Courier", int(40*self.__fontMult))))

            self.__items.append(Button(
                self.__frame2, text="1 min", command=partial(self.setDefaultTimer, 60), font=("Courier", int(24*self.__fontMult))))

            self.__items.append(Button(
                self.__frame2, text="3 min", command=partial(self.setDefaultTimer, 180), font=("Courier", int(24*self.__fontMult))))

            self.__items.append(Button(
                self.__frame2, text="Endless", command=partial(self.setDefaultTimer, -1), font=("Courier", int(24*self.__fontMult))))

            self.__items.append(
                Label(self.__frame2, text="Select Difficulty", font=("Courier", int(40*self.__fontMult))))

            self.__items.append(Button(
                self.__frame2, text="Easy", command=partial(self.setLevel, 1), font=("Courier", int(24*self.__fontMult))))

            self.__items.append(Button(
                self.__frame2, text="Hard", command=partial(self.setLevel, 2), font=("Courier", int(24*self.__fontMult))))

            self.__items.append(Button(
                self.__frame2, text="Harder", command=partial(self.setLevel, 3), font=("Courier", int(24*self.__fontMult))))

            self.__items.append(
                Label(self.__frame2, text="Press ESC to exit", font=("Courier", int(30*self.__fontMult))))

            for item in self.__items:
                item.pack(padx=0, pady=5)

            self.__table = self.initTable()
            self.__cellCount = self.__items[4].get()

            self.startCountdown()

            self.__updateTimerThread = threading.Thread(
                target=self.updateTimer, name="updateTimerThread")
            self.__updateTimerThread.start()

            self.update()

        if self.__display == 2:  # Game Over

            self.__game = False

            pass

    def changeMenu(self, displayState):

        self.__display = displayState
        self.frameDisplay()
        self.update()

    def update(self):

        if self.__display == 1:

            self.__table.gravity()
            # self.__table.displayTable()
            self.drawGrid()
            self.updateLabels()

            self.__win = self.__table.win()

            if self.__win == True:

                self.changeMenu(2)

    def updateLabels(self):

        self.__items[1].config(text="High Score : " + score.getHighScore())
        self.__items[2].config(text="Score : " + str(self.__score))
        self.__items[3].config(text="Max : " + self.getMax())
        self.__items[7].config(text=self.getTimer())

    def updateTimer(self):
        while self.__updateThread:
            if self.getTimer() == "00:00":
                self.changeMenu(2)
                self.__timerThread.stop()
                break
            try:
                self.__items[7].config(text=self.getTimer())

            except:
                self.__timerThread.stop()
                break
            # sleep(1)

    def reset(self):
        self.__timerThread.stop()
        self.newTable()

    def startCountdown(self):
        self.__timerThread = timer.TimerClass(self.__defaultTime)
        self.__timerThread.start()

    def updateClick(self, event):
        self.__mouseX = event.x
        self.__mouseY = event.y

        x = math.floor(((self.__mouseX) / (self.__width)) *
                       (self.__table.getCol()))
        y = math.floor(((self.__mouseY) / (self.__height)) *
                       (self.__table.getRow()))

        if event.x_root < self.__width:
            self.highlightCells(x, y)

    def highlightCells(self, x, y):

        if self.__game:

            if self.__table.getSelected() == True and self.__table.getGrid()[y][x].getHighlight() == False:

                for item in self.__table.getPositions():

                    self.__table.getGrid()[item[1]][item[0]].setHighlight(
                        False)  # If yes then remove highlight
                self.__table.setSelected(False)

            else:

                neighborPos = self.__table.updateNeighborsPos(
                    x, y)  # List of x and y of all neighbors
                if len(neighborPos) > 1:
                    # Boolean of whether it's highlighted or not
                    val = self.__table.getGrid()[neighborPos[0]
                                                 [1]][neighborPos[0][0]].getHighlight()

                    if val:

                        self.__table.setSelected(False)

                        self.addScore(len(neighborPos) *
                                      self.__table.getGrid()[y][x].getState())

                        self.removeCells(neighborPos[1:])
                        self.__table.getGrid()[neighborPos[0][1]][neighborPos[0][0]].setHighlight(
                            False)
                        self.addUp(neighborPos[0])

                    if val == False:

                        self.__table.setSelected(True)

                        for item in neighborPos:
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

    def updateHighscore(self):
        if self.__score > int(score.getHighScore()):
            score.__score = self.__score

    def destroy(self, leave=True):

        try:
            self.__timerThread.stop()
        except:
            pass

        self.__updateThread = False
        self.updateHighscore()
        self.__root.destroy()

        if leave:
            exit()

    def addScore(self, score):
        self.__score = self.__score + score


g = Game(800, 800)
