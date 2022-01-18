# from os import error
# from types import NoneType

from table import *
import score
import timer

from random import *
from tkinter import *
# from tkinter import ttk
# from time import sleep, time
import math
import threading
from functools import partial


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

    def __init__(self, width: int, height: int):
        """
        Initialize variables and start the game window.

            Parameters:
                width (int): width of the main game interface.
                height (int): height of the main game interface.
        """

        clear()  # Clear console

        self.__width = width
        self.__height = height
        self.__fontMult = 0.7  # Font size multiplier

        # Sets the default value of the game when the window pops

        self.__win = False
        self.__score = 0
        self.__defaultTime = 60
        self.__game = False  # Game state (in game or in menu)
        self.__level = 1
        # Want the thread to run at all time when called and break when trying to exit game
        self.__updateThread = True

        # Creates the tkinter window

        self.__root = Tk()
        self.__root.configure(background='white')
        # Binds buttons / keys to methods
        # Left click initiate self.updateClick
        self.__root.bind('<Button-1>', self.updateClick)
        # Escape key initiate self.excapeKey
        self.__root.bind('<Escape>', self.escapeKey)
        self.__root.attributes("-fullscreen", True)

        self.__root.title = ("Just Get Ten")

        # BASE

        # Create a base frame where everything will be displayed
        self.__base = Frame(self.__root)
        self.__base.grid(row=0, column=0)  # Displays it in grid form

        self.changeMenu(0)  # Inititate the creation and display of menu (0)

        self.__root.mainloop()  # Start the window

    # Getters Start

    def getMax(self):
        """
        Checks every state of the cells within the game grid and returns a string of the Max value.

            Returns:
                str: String of the current max value.
        """

        val = 0
        for y in range(self.__table.getRow()):  # For every cell in the grid
            for x in range(self.__table.getCol()):
                # If the value of current cell is higher than last saved value
                if self.__table.getGrid()[y][x].getState() > val:
                    # Then update the highest value
                    val = self.__table.getGrid()[y][x].getState()
        # self.__max = val
        return str(val)

    def getTimer(self):
        """
        Gets the Time left to the timer.

            Returns:
                str: String of the time left to the game.
        """

        return self.__timerThread.getTimer()  # Gets string from Timer class in timer.py

# Getters End

# Setters Start

    def setDefaultTimer(self, time: int):
        """
        Sets the value of the default timer.

            Parameters:
                time (int): Value of the new default time.
        """

        self.__defaultTime = time

    def setLevel(self, level: int):
        """
        Sets the level of the Game.

            Parameters:
                level (int): Level of the game (1, 2, 3).
        """

        self.__level = level

# Setters End

# Methods Start

    def initTable(self):
        """
        Initialise a new Table object with the value of the Level, and Cell count.

            Returns:
                Table: Table object for table.py
        """

        # Gets the Cell count from the slider input in the in-game menu
        self.__cellCount = self.__items[4].get()
        
        return Table(self.__level, self.__cellCount, self.__cellCount)

    def newTable(self):
        """
        Updates the interface as well as changes the current Table to a new one.
        """

        self.__table = self.initTable()  # Initialise a new table
        self.updateHighscore()
        self.__score = 0  # Reset scores after updating high score if needed
        self.startCountdown()  # Restart countdown
        self.update()  # Update the Display grid

    def frameDisplay(self):
        """
        Creates all the widgets and frames needed to display depending on the state of the game.
        (Start menu, In-Game, Win / Lose Menu)
        """

        # Destroy everything in self.__base to have a clean frame.
        for widget in self.__base.winfo_children():
            widget.destroy()

        # Changes title depending on Menu

        if self.__display == 0:  # Start Menu
            title = "Just Get Ten"

        if self.__display == 2:

            if self.__win:  # Win Menu
                title = "YOU WIN"
            else:  # Lose Menu
                title = "YOU LOSE"

        # Menus (Start, Win and Lose)
        if self.__display == 0 or self.__display == 2:

            self.__game = False  # Game not in progress

        # Menu Frame

            self.__menuItems = []  # Creates a list of items in the menu to display them in a loop

            self.__menuItems.append(  # Title displaying the title variable contents
                Label(self.__base, text=title, font=("Courier", int(60*self.__fontMult))))

            self.__menuItems.append(  # High score display
                Label(self.__base, text="High Score : " + score.getHighScore(), font=("Courier", int(44*self.__fontMult))))

            self.__menuItems.append(  # Last score (0 on start menu)
                Label(self.__base, text="Score : " + str(self.__score), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(  # New Game button (Changes the menu to Game menu)
                self.__base, text="New Game", command=partial(self.changeMenu, 1), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(  # Select timer text
                Label(self.__base, text="Select Time", font=("Courier", int(44*self.__fontMult))))

            self.__menuItems.append(Button(  # Button to change default timer to 60
                self.__base, text="1 min", command=partial(self.setDefaultTimer, 60), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(  # Button to change defalt timer to 180
                self.__base, text="3 min", command=partial(self.setDefaultTimer, 180), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(  # Button to change default timer -1
                self.__base, text="Endless", command=partial(self.setDefaultTimer, -1), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(  # Select difficulty text
                Label(self.__base, text="Select Difficulty", font=("Courier", int(44*self.__fontMult))))

            self.__menuItems.append(Button(  # Changes level to 1
                self.__base, text="Easy", command=partial(self.setLevel, 1), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(  # Changes level to 2
                self.__base, text="Hard", command=partial(self.setLevel, 2), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(Button(  # Changes level to 3
                self.__base, text="Harder", command=partial(self.setLevel, 3), font=("Courier", int(34*self.__fontMult))))

            self.__menuItems.append(  # Press to ESC to exit text
                Label(self.__base, text="Press ESC to exit", font=("Courier", int(30*self.__fontMult))))

            for i in range(len(self.__menuItems)):  # Display items in row with a loop
                self.__menuItems[i].grid(row=i, column=0)

        # Menu Frame End

        if self.__display == 1:  # In-Game

            self.__game = True  # Game in-progress
            self.__win = False  # Restart the game so win set to False
            self.__score = 0  # Score to 0

        # Game Frame

            # Creation of Frame to contain canvas where the grid of the game will be drawn

            self.__frame1 = Frame(self.__base)
            self.__frame1.grid(row=0, column=0, )

            self.__canvas = Canvas(self.__frame1)
            self.__canvas.config(width=self.__width, height=self.__height,
                                 highlightthickness=0, bd=0, bg="black")
            self.__canvas.pack()

        # Game Frame End

        # User Interface Start

            # Creates another frame to have a in-game menu with mostly the same options as the Start Menu
            # Changed the New game button to NewGrid (using self.reset)
            # Added a slider to chose the dimensions of the grid.

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

        # User Interface End

        # Initialization of Game variables

            self.__table = self.initTable()  # Creates a new Table object

            self.startCountdown()  # Start the countdown with a Thread

            self.__updateTimerThread = threading.Thread(  # Creates another thread allowing the constant display update of the timer
                target=self.updateTimer, name="updateTimerThread")
            self.__updateTimerThread.start()  # Start the thread

        # Init End

            self.update()  # Updates the labels and the grid (game rules) and displays it in the canvas

    def changeMenu(self, displayState: int):
        """
        Changes the displayed Menu on the window.

            Parameters:
                displayState (int): Value of the menu wanted to be displayed (0: Start Menu; 1: In-Game; 2: Win / Lose Menu)
        """

        self.__display = displayState  # Changes display value
        # Clears and Changes the widgets displayed depending on the display value
        self.frameDisplay()

    def update(self):
        """
        Updates the grid using the game logic and draws it in the canvas and then updates labels.
        """

        if self.__display == 1:  # Only if in-game

            self.__table.gravity()  # Apply gravity to the cells in the grid
            # self.__table.displayTable()
            self.drawGrid()  # Draw the grid in the canvas
            self.updateLabels()  # Update the labels in the user interface

            self.__win = self.__table.win()  # Check if the board has a winning condition

            if self.__win == True:  # If it does then change to Win Menu

                self.changeMenu(2)  # With self.__win = True

    def updateLabels(self):
        """
        Updates the Labels in the User interface.
        """

        self.__items[1].config(text="High Score : " + score.getHighScore())
        self.__items[2].config(text="Score : " + str(self.__score))
        self.__items[3].config(text="Max : " + self.getMax())
        self.__items[7].config(text=self.getTimer())

    def updateTimer(self):
        """
        Runs in a Thread. Constantly updates the timer label in the User interface. Also checks for lose condition.
        """
        while self.__updateThread:  # True except when exiting program
            if self.getTimer() == "00:00":  # If timer reaches 0 sec
                self.updateHighscore()
                # Changes to Lose Menu (with self.__win = False)
                self.changeMenu(2)
                self.__timerThread.stop()  # Stops the timer thread.
                break  # Break the loop because Game ended

            try:
                # Tries to change the test of the timer label in the user interface
                self.__items[7].config(text=self.getTimer())

            except:  # if exceptin raised (SystemExit)
                self.__timerThread.stop()  # Stops the timer thread.
                break  # Break the loop because Game exited

    def reset(self):
        """
        Stops the timer and start a new one with a new grid.
        """
        self.__timerThread.stop()  # Stop the timer thread
        self.newTable()  # Start new grid / game

    def startCountdown(self):
        """
        Creates a new timer object and start a thread.
        """
        self.__timerThread = timer.TimerClass(
            self.__defaultTime)  # Timer object with default time as timer value
        self.__timerThread.start()  # Start its thread

    def updateClick(self, event):
        """
        Gets the mouse position within the window and uses it to update the grid.

            Parameters:
                event ([type]): [description]
        """

        # Mouse X Y position in pixels
        self.__mouseX = event.x
        self.__mouseY = event.y

        # X Y position of the cells in the grid from the mouse position
        x = math.floor(((self.__mouseX) / (self.__width)) *
                       (self.__table.getCol()))
        y = math.floor(((self.__mouseY) / (self.__height)) *
                       (self.__table.getRow()))

        if event.x_root < self.__width:  # If the mouse is within the canvas
            self.highlightCells(x, y)  # Then apply the highlight function

    def escapeKey(self, event=None):
        """
        When the escape button is pressed, exit tkinter window and program.

            Parameters:
                event (NoneType): Necessary for key input function. Defaults to None.

            Raises:
                SystemExit: Tkinter module exception
        """

        # (tkinter window exits but program doesn't when in-game because of tkinter module exception on SystemExit)
        # File "C:\Users\yoann\AppData\Local\Programs\Python\Python310\lib\tkinter\__init__.py", line 1921, in __call__
        # return self.func(*args)

        self.destroy()  # Exit Tkinter window and program

    def highlightCells(self, x: int, y: int):
        """
        Highlights the selected cell and its neighbors if possible.
        Fuses if already highlighted.
        Deselect if highlight is called with x, y cell not highlighted.

            Parameters:
                x (int): X position of a cell within the grid.
                y (int): Y position of a cell within the grid.
        """

        if self.__game:  # if state of game active

            if self.__table.getSelected() == True and self.__table.getGrid()[y][x].getHighlight() == False:
                # if selected cell is not highlighted when other cells are already selected

                for item in self.__table.getPositions():  # For previously highlighted cells

                    self.__table.getGrid()[item[1]][item[0]].setHighlight(
                        False)  # remove highlight
                self.__table.setSelected(False)  # No cells highlighted anymore

            else:

                neighborPos = self.__table.updateNeighborsPos(
                    x, y)  # List of x and y of all neighbors
                if len(neighborPos) > 1:  # If there's at least one neighbor

                    # Boolean of whether selected cell is highlighted or not
                    val = self.__table.getGrid()[y][x].getHighlight()

                    if val:  # If selected cell is already highlighted

                        self.addScore(len(neighborPos) *
                                      self.__table.getGrid()[y][x].getState())
                        # Add to the score the number of neighbors (including selected cell) times the value of the selected cell

                        # Remove every cell except selected one
                        self.removeCells(neighborPos[1:])
                        self.__table.getGrid()[y][x].setHighlight(
                            False)  # Remove highlight from selected cell
                        # Add 1 to the value of the selected cell
                        self.addUp((x, y))

                        # No cells highlighted anymore
                        self.__table.setSelected(False)

                    if val == False:  # if selected cell is not highlighted

                        for item in neighborPos:
                            self.__table.getGrid()[item[1]][item[0]].setHighlight(
                                True)  # highlight every cell in neighborhood

                        # Cells are now highlighted
                        self.__table.setSelected(True)

                del neighborPos  # Delete neighborPos for memory

            self.update()  # Update the grid

    def removeCells(self, items: list[tuple[int, int]]):
        """
        Change value of every cell in the list to 0.

            Parameters:
                items (list of tuples of int): List containing tuples of x,y positions of cells.
        """

        for item in items:
            self.__table.getGrid()[item[1]][item[0]].setState(0)

    def addUp(self, item: tuple[int, int]):
        """
        Adds one to the value of the X, Y cell in the grid.

            Parameters:
                item (tuple of int): Tuple of the X, Y position of the selected cell.
        """

        # Gets current value
        val = self.__table.getGrid()[item[1]][item[0]].getState()
        self.__table.getGrid()[item[1]][item[0]].setState(
            val+1)  # Adds one to value

        # Updates the color
        self.__table.getGrid()[item[1]][item[0]].changeColor()

    def drawGrid(self):
        """
        Draws the grid within the canvas with the values of the Table.
        """

        coef = ((self.__table.getCol()/100)+1)*1
        self.__canvas.delete("all")  # Cleans the canvas

        # Gets number of columns and rows
        tRow = self.__table.getRow()
        tCol = self.__table.getCol()

        # Gets width and height of one cell
        sizeW = self.__width/tCol
        sizeH = self.__height/tRow

        for row in range(tRow):  # For every cell position
            for col in range(tCol):

                color = self.__table.getGrid()[row][col].getColor()
                text = self.__table.getGrid()[row][col].getState()
                highlighted = self.__table.getGrid()[row][col].getHighlight()

                if highlighted:  # If cell highlighted then draw rectangle with black background
                    self.__canvas.create_rectangle(
                        col*sizeW+(10/coef), row*sizeH+(10/coef), col*sizeW+sizeW-(10/coef), row*sizeH+sizeH-(10/coef), fill="black", outline="black")

                else:  # If not highlighted then draw rectangle with the cell color as background
                    self.__canvas.create_rectangle(
                        col*sizeW, row*sizeH, col*sizeW+sizeW, row*sizeH+sizeH, fill=color, outline="black")

                # Write the value on the current cell
                self.__canvas.create_text(
                    (col*sizeW)+sizeW*0.5, (row*sizeH)+sizeW*0.5, text=text, font=("Purisa", int(38/coef)), fill="white")

    def updateHighscore(self):
        """
        Updates the High score.
        """

        if self.__score > int(score.getHighScore()):
            score.setScore(self.__score)

    def destroy(self):
        """
        Destroys the window and exits the program.
        """

        try:
            self.__timerThread.stop()  # Tries to stop the timer thread
        except:
            pass

        self.__updateThread = False  # Stops the updateTimer thread
        self.updateHighscore()
        self.__root.destroy()  # Destroy window

        exit()  # Exit program

    def addScore(self, score: int):
        """
        Adds a value to the current score.

            Parameters:
                score (int): Walue added to the score.
        """

        self.__score = self.__score + score

# Methods End

g = Game(800, 800)
