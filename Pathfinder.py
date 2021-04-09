import pygame, json, sys, queue, random

# Choose the desired map
f = open('star.mz',)
maze = json.load(f)
f.close()

# Some default paramenters
# Change RGB values for desired colors

SPEED = 100 # Determines how fast the algorithm will run, recommeded values: 10-100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
FOUND = False # DO NOT CHANGE
WINDOW_HEIGHT = 400 # DO NOT CHANGE
WINDOW_WIDTH = 400 # DO NOT CHANGE
BLOCK_SIZE = 20 # DO NOT CHANGE
STEP = 0 # DO NOT CHANGE

# Creates random obstacles, use the desired maze and the ammount of obstacles as the parameters
def createObstacles(maze, amount):
    for i in range(amount):
        maze[random.randint(0,19)][random.randint(0,19)] = "#"

# Finds the coordinates of S (starting block)
# NOTE: ALL COORDINATES ARE WRITTEN IN (Y,X) FORM!!!
def findS(maze):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            if maze[int(y/20)][int(x/20)] == "S":
                sCoords = [int(y/20), int(x/20)]
                return sCoords

# Finds the coordinates of E (ending block)
# NOTE: ALL COORDINATES ARE WRITTEN IN (Y,X) FORM!!!
def findE(maze):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            if maze[int(y/20)][int(x/20)] == "E":
                sCoords = [int(y/20), int(x/20)]
                return sCoords

# Validates if the next step is valid
def validateBlock(maze, put):
    if put[0] >= 0 and put[1] >= 0 and put[0] < 20 and put[1] < 20 and maze[put[0]][put[1]] ==  " ":
            return True

# Grassfire algorithm implementation
def grassFIRE(maze):
    global FOUND, STEP
    if not FOUND:
        temp = FIRE.get()
        for move in [1,-1]:
            for i in range(2):
                put = [temp[0],temp[1]]
                put[i] = put[i] + move
                if validateBlock(maze,put):
                    FIRE.put(put)
                    maze[put[0]][put[1]] = str(STEP)    
                elif put == findS(maze):
                    FOUND = True
        STEP += 1

# Rendering function
def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if maze[int(y/20)][int(x/20)] != " ":
                pygame.draw.rect(SCREEN, BLUE, rect)
            if maze[int(y/20)][int(x/20)] == " ":
                pygame.draw.rect(SCREEN, WHITE, rect)
            if maze[int(y/20)][int(x/20)] == "#":
                pygame.draw.rect(SCREEN, BLACK, rect)
            elif maze[int(y/20)][int(x/20)] == "S":
               pygame.draw.rect(SCREEN, GREEN, rect)
            elif maze[int(y/20)][int(x/20)] == "E":
                pygame.draw.rect(SCREEN, RED, rect)

# Main loop
def main():
    global SCREEN, CLOCK, FIRE
    pygame.init()
    pygame.display.set_caption('Pathfinder')
    FIRE = queue.Queue()
    FIRE.put(findE(maze))
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        grassFIRE(maze)
        drawGrid()
        print(maze)
        if not FOUND:
            CLOCK.tick(SPEED)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Change second value to desired ammount of obstacles
# NOTE: HIGH AMMOUNT OF OBSTACLES CAN POTENTIALLY CRASH THE PROGRAM
# Recommended ammount: 100-150
# If program does not start, run again to generate new obstacles     
createObstacles(maze, 0)
main()