def getHighScore():
    """
    Gets the current high score stored in score.txt.

        Returns:
            str: Returns the first line of score.txt.     
    """
    with open("./score.txt", 'r') as file: # Opens score.txt and read it as "file"
        lines = file.readlines() # Read all the lines of "file" and store them in an array named lines
        return lines[0] # return the first line


def setScore(score):
    """
    Sets a new high score by rewriting score.txt.
    
        Parameters:
            score (int): Value of the new high score.
    """
    with open("./score.txt", 'w') as file: # Rewrite the file
        file.write(str(score)) # Write the new hih score
