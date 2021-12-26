def getHighScore():
    with open("./1PYTH2/score.py", 'r') as file:
        lines = file.readlines()
        return lines[0]


def setScore(score):
    with open("score.txt", 'w') as file:
        file.write(str(score))
