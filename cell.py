from random import *


class Cell():

    def __init__(self, level: int):
        """
        Will initialize a cell and assign it's value / color based on the level's difficulty.

            Parameters:
                level (int): Level difficuty. 1 to 3.
        """

        self.__colorDict = { # List of the HEX colors of each different cells (value)
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

        self.__diff = { # Probability of cell appearences based on level difficulty
            1: { # Diffuculty 1
                0: 0,
                1: 0.4,
                2: 0.7,
                3: 0.95,
                4: 1
            },
            2: { # Diffuculty 2
                0: 0,
                1: 0.1,
                2: 0.3,
                3: 0.6,
                4: 1
            },

            3: { # Difficulty 3
                0: 0,
                1: 0.1,
                2: 0.2,
                3: 0.3,
                4: 1
            }
        }
        
        self.__state = 0 # Value of the cell
        self.__color = "" # Hex color assigned based on earlier dictionnary
        self.__highlighted = False # Highlight (targeted) or not
        self.__checked = False # if has been already checked during the checkNeighbors function

        self.randomState(level) # Randomize the value of the cell depending on the difficulty probability
        self.changeColor() # Change color accordingly

# Getters Start

    def getInfo(self):
        """
        Gets the state and the color of the cell.
        
            Returns:
                (int, str): State of the cell, Hex color of the cell.
        """
        return self.__state, self. __color

    def getColorDict(self):
        """
        Gets the list of colors assigned to each state.

            Returns:
                (dict of int: str): Dictionnary of the HEX colors assigned to states as keys.
        """
        return self.__colorDict

    def getState(self):
        """
        Gets the state of the cell.

            Returns:
                int: State of the cell.
        """
        return self.__state

    def getColor(self):
        """
        Gets the color of the cell.

            Returns:
                str: Hex color of the cell.
        """
        return self.__color

    def getHighlight(self):
        """
        Gets if the cell is highlighted.

            Returns:
                bool: Highlighted or not.
        """
        return self.__highlighted

    def getChecked(self):
        """
        Gets if the cell has already been checked during the process of checking neighbors.

            Returns:
                bool: Has been checked or not.
        """
        return self.__checked

# End
    
# Setters Start

    def setHighlight(self, val: bool):
        """
        Sets the state of highlight of the cell.
        
            Parameters:
                val (bool): Highlight or remove highlight.
        """
        self.__highlighted = val

    def setState(self, n: int):
        """
        Sets the state of the cell and updates its highlight and color.
        
            Parameters:
                n (int): State of the cell.
        """
        self.__state = n
        self.__highlighted = False # When changing the state (value), remove highlight if there was one
        self.changeColor() # Change color accordingly to the state 

    def setColor(self, color: str):
        """
        Sets the color of the cell.
        
            Parameters:
                color (str): HEX color of the cell.
        """
        self.__color = color

    def setChecked(self, state: bool):
        """
        Sets if the cell has been checked within the chackNeighbors function.
        
            Parameters:
                state (bool): Checked or not.
        """
        self.__checked = state

# End

# Methods Start

    def randomState(self, diff: int):
        '''
        Selects a random state for the cell by using the probabilities given.
            
            Parameters:
                diff (int): Difficulty of the level. 1 to 3.
        '''
        rdm = random()

        for i in range(1, len(self.__diff[diff])):
            if self.__diff[diff][i-1] <= rdm <= self.__diff[diff][i]:
                self.setState(i)

    def changeColor(self):
        """
        Updates the color of the cell according to its state.
        """

        self.setColor(self.__colorDict[self.__state])

# End