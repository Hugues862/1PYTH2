from os import system, name
from time import sleep
from cell import *


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


class Table():
    
    def __init__(self, level: int, row: int, col: int):
        """
        Intializes a new table.
        
            Parameters:
                level (int): Difficulty of the table. 1 to 3.
                row (int): Number of rows of the table.
                col (int): Numer of columns of the table.          
        """

        self.__row = row
        self.__col = col
        self.__level = level

        self.__positions = []
        self.__selected = False

        self.__grid = self.initGrid()

    # Getters

    def getRow(self):
        """
        Gets the number of rows of the table (if reset).
        
            Returns:
                int: Number of rows of the table.
        """
        return self.__row

    def getCol(self):
        """
        Gets the number of columns of the table (if reset).

            Returns:
                int: Number of columns of the table.
        """
        return self.__col

    def getGrid(self):
        """
        Gets the grid representing the table.

            Returns:
                matrice: Array of arrays of cells (object).
        """
        return self.__grid
    
    def getPositions(self):
        """
        Gets the positions of the last saved and checked neighbors.

            Returns:
                matrice: Arrays of tuples containing x,y positions of cells
        """
        return self.__positions

    def getSelected(self):
        """
        Gets if Cells have been selected or not.

            Returns:
                bool: Selected or not (cells highlighted or not).
        """
        return self.__selected
    # Setters

    def setGrid(self, grid):
        """
        Sets the grid to a new grid.
        
            Parameters:
                grid (matrice): Array of arrays of cells (object).
        """
        self.__grid = grid

    def setRow(self, row: int):
        """
        Sets the number of rows of the grid (if reset).
        
            Parameters:
                row (int): Number of rows if grid is reset.
        """
        self.__row = row

    def setCol(self, col: int):
        """
        Sets the number of cols of the grid (if reset).
        
            Parameters:
                col (int): Number of cols if grid is reset.
        """
        self.__col = col

    def setPositions(self, positions):
        """
        Sets new (x,y) positions of neighbors.

            Parameters:
                positions (arr): Arrays of tuples containing x,y positions of cells
        """
        self.__positions = positions
        
    def setSelected(self, selected: bool):
        """
        Sets if cells are selected or not.
        
            Parameters:
                selected (bool): Selected or not.
        """
        self.__selected = selected
        
    # Methods

    def initGrid(self):
        """
        Creates a new grid and replaces the previous one with it.
        
            Returns:
                matrice: Array of arrays of cells (object).
        """

        grid = [[Cell(self.__level) for col in range(self.__col)]
                for row in range(self.__row)] # inline for loop to create a 2D array of cells
        return grid

    def checkNeighbors(self, x: int, y: int):
        """
        Checks the neighbors of the clicked cell with the same value
        and gets their positions in a recursive way.

            Parameters: 
                x (int): X position of the current cell.
                y (int): Y position of the current cell.

            Returns:
                matrice: Arrays of tuples containing x,y positions of cells.
        """

        tab = [(x, y)] # Creates the list of neighbors of the current cell including the current cell

        self.getGrid()[y][x].setChecked(True) # Sets the current cell checked value to True to ignore it once checked

        top, bottom, left, right = [], [], [], [] # Creates temporary arrays to add the positions of neighbors in the recursion

    # Recursion Start

        # If the cell is not on the first row, if the cell above has the same value, if the cell above hasn't been checked yet, then
        if y != 0 and self.getGrid()[y - 1][x].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y - 1][x].getChecked() == False:

            top = self.checkNeighbors(x, y - 1) # Add the position of this cell to Top and proceed to check its own neighbors

        # If the cell is not on the last row, if the cell below has the same value, if the cell below hasn't been checked yet, then
        if y != self.getRow() - 1 and self.getGrid()[y + 1][x].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y + 1][x].getChecked() == False:

            bottom = self.checkNeighbors(x, y + 1) # Add the position of this cell to Bottom and proceed to check its own neighbors

        # If the cell is not on the first column, if the left cell has the same value, if the left cell hasn't been checked yet, then
        if x != 0 and self.getGrid()[y][x - 1].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y][x - 1].getChecked() == False:

            left = self.checkNeighbors(x - 1, y) # Add the position of this cell to Left and proceed to check its own neighbors

        # If the cell is not on the last column, if the right cell has the same value, if the right cell hasn't been checked yet, then
        if x != self.getCol() - 1 and self.getGrid()[y][x + 1].getState() == self.getGrid()[y][x].getState() and self.getGrid()[y][x + 1].getChecked() == False:

            right = self.checkNeighbors(x + 1, y) # Add the position of this cell to Right and proceed to check its own neighbors

    # Recursion End

        self.getGrid()[y][x].setChecked(False) 
        # After having checked every neighbors of the current cell, put the current cell back to unchecked

        # Add every tuple (x,y) to tab if not in tab and return it
        # This is to have a simple 2D array and avoid having a linked list which is harder to deal with

        for i in top:
            if i not in tab:
                tab.append(i)
        for i in bottom:
            if i not in tab:
                tab.append(i)
        for i in left:
            if i not in tab:
                tab.append(i)
        for i in right:
            if i not in tab:
                tab.append(i)

        return tab # Becomes top, bottom, left and right arrays within the recursion

    def updateNeighborsPos(self, x: int, y: int):
        """
        Updates positions of previously selected cell's neighbors to the newly selected cell's neighbors.
        
            Parameters:
                x (int): X position of the original cell.
                y (int): Y position of the original cell.
            
            Returns:
                matrice: Arrays of tuples containing x,y positions of cells.
        """

        self.__positions = self.checkNeighbors(x, y) # Saves the new neighbors's positions
        return self.__positions

    def displayTable(self):
        """
        Prints the grid with values/states in the console.
        """

        print() # Skip line
        display = [[None for col in range(self.__col)]
                   for row in range(self.__row)] # Creates a 2D array (col x row) with None as default values

        for row in range(self.__row):
            for col in range(self.__col):
                display[row][col] = str(self.__grid[row][col].getState()) # Changes the None to the values of the respective positions (x, y) in the grid
        
        # skip a line for every row (items), and join the values within each rows with a space
        for item in display:
            print(" ".join(item))

    def gravity(self):
        """
        Updates the positions of the cells within the grid by applying gravity
        by moving cells above downwards if current cell is empty.
        """
        
        empty = False # Consider there are no empty cells in grid
        for y in range(self.__row):
            for x in range(self.__col): # For every cell in grid
                if self.__grid[y][x].getState() == 0:  # if cell is empty (0)
                    
                    empty = True # Set empty to True

                    if self.__grid[y-1][x].getState() != 0 and y > 0:
                    # If cell above current cell is not empty, if current cell is not on first row

                        self.__grid[y][x].setState(self.__grid[y-1][x].getState()) # Move every cell downwards if cell below empty
                        self.__grid[y-1][x].setState(0) # Changed previous position of moved cell to empty (0)

                    if y == 0:
                    # If no cells with value above empty cells
                        self.__grid[y][x].randomState(self.__level) # Randomize the state of the cell
        
        if empty: # If empty cell(s) in grid
            self.gravity()
            # Restart the function to move the rest of the cells downwards and randomize the rest of the empty cells

    def win(self):
        """
        Checks the winning conditions and returns True or False accordingly.

            Returns:
                bool: Win or not.
        """

        for i in self.__grid:
            for j in i: # For every cell in grid

                if j.getState() == 10: # If value of any cell is equal to 10
                    return True
        
        # If no cell value is equal to 10
        return False
