def init():
    global gridSize, screenWidth, screenHeight, width, height
    screenWidth = 1440
    screenHeight = 870
    width, height = 20, 20
    gridSize = (min(screenWidth, screenHeight) - 200) // width