from random import *
from tkinter import *

class cell():
    
    def __init__(self) -> None:
        
        self.__state = 0
        self.__color = ""
        
        self.randomState()
        self.changeColor()
        
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
        
        state = self.getState()
        
        if state == 1:
            self.setColor("31CD32")
            return
        
        if state == 2:
            self.setColor("4068E1")
            return
        
        if state == 3:
            self.setColor("FF8C00")
            return
        
        if state == 4:
            self.setColor("FF0000")
            return
        
        if state == 5:
            self.setColor("8FBC8E")
            return
       
        if state == 6:
            self.setColor("FF00FF")
            return
        
        if state == 7:
            self.setColor("9400D3")
            return
        
        if state == 8:
            self.setColor("5B00F7")
            return
        
        if state == 9:
            self.setColor("32008F")
            return
        
        if state == 10:
            self.setColor("000000")
            return


class table():
    
    def __init__(self, x, y) -> None:
        
        self.__grid = [[cell() for j in range (x)] for i in range (y)]
    
    def getGrid(self):
        return self.__grid
    
    def setGrid(self, grid):
        self.__grid = grid
    
    
    
    
    def run(self, rows, cols, width, height):
        
        self.__xOrigin = width / 2
        self.__yOrigin = height / 2
        
        if rows == cols:
            self.caseSize = height / rows
            self.__yOrigin = 0
            self.__xOrigin = 0
        
        elif rows > cols:
            self.caseSize = height / rows
            self.__yOrigin = 0
            self.__xOrigin -= self.caseSize * (cols / 2)
            
        else:
            self.caseSize = width / cols
            self.__xOrigin = 0
            self.__yOrigin -= self.caseSize * (rows / 2)
            
            
            
        self.__root = Tk()
        
        self.__leftFrame = Frame(self.__root, padx = 50, pady = 50)
        self.__leftFrame.grid(row = 0, column = 0)
        
        self.__canvas = Canvas(self.__leftFrame, width = width, height = height)
        self.__canvas.pack()
        
    
    def drawCanvas(self):
        
        for rows in range (len(self.__grid)):
            
            for cols in range (len(self.__grid[rows])):
                
                self.__canvas.create_rectangle(self.__xOrigin + self.caseSize * cols, self.__yOrigin + self.caseSize * rows, self.__xOrigin + self.caseSize * (cols + 1), self.__yOrigin + self.caseSize * (rows + 1), fill = self.__grid[rows][cols].getColor())
                self.__canvas.create_text(self.__xOrigin + self.caseSize * cols, self.__yOrigin + self.caseSize * rows, text = str(self.__grid[rows][cols].getState()))
                
            