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
STEP = 1 # DO NOT CHANGE

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

def validateStep(maze, put, prev):
    global END
    if put[0] >= 0 and put[1] >= 0 and put[0] < 20 and put[1] < 20 and maze[put[0]][put[1]] !=  "#" and maze[put[0]][put[1]] !=  " " and maze[put[0]][put[1]] !=  "S":
        if int(maze[put[0]][put[1]]) < int(maze[prev[0]][prev[1]]):
            return True
    elif maze[prev[0]][prev[1]] ==  "0":
        print("END")
        END = True      

# grassFire algorithm implementation
def grassFire(maze):
    global FOUND, STEP, START
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
                    maze[put[0]][put[1]] = str(999)
                    E = findE(maze)
                    maze[E[0]][E[1]] = str(0)
                    FOUND = True
        STEP += 1

# Calculates the step needed to get to the "E" block
# appends the coordinates into the PATH array
# stops after reaching the "E" block
def traceBack(maze, block):
    global PATH, START, END
    for move in [1,-1]:
            for i in range(2):
                put = [block[0],block[1]]
                put[i] += move
                if validateStep(maze, put, block):
                    START = put
                    block = put
                    PATH.append(put)
                    print(PATH)
                    
                    
# Rendering function
def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if maze[int(y/20)][int(x/20)] != " " and [int(y/20),int(x/20)] != PATH[-1]:
                pygame.draw.rect(SCREEN, BLUE, rect)
            if maze[int(y/20)][int(x/20)] == " ":
                pygame.draw.rect(SCREEN, WHITE, rect)
            elif maze[int(y/20)][int(x/20)] == "#":
                pygame.draw.rect(SCREEN, BLACK, rect)
            elif maze[int(y/20)][int(x/20)] == "S" or maze[int(y/20)][int(x/20)] == "999":
               pygame.draw.rect(SCREEN, GREEN, rect)
            elif maze[int(y/20)][int(x/20)] == "E" or maze[int(y/20)][int(x/20)] == "0":
                pygame.draw.rect(SCREEN, RED, rect)
            elif [int(y/20),int(x/20)] in PATH:
                pygame.draw.rect(SCREEN, GREEN, rect)
                
# Main loop
def main():
    global SCREEN, CLOCK, FIRE, PATH, START, END 
    pygame.init()
    pygame.display.set_caption('Pathfinder')
    FIRE = queue.Queue()
    FIRE.put(findE(maze))
    START = findS(maze)
    PATH = []
    PATH.append(START)
    END = False
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    print(findE(maze))

    while True:
        grassFire(maze)
        drawGrid()
        if not FOUND:
            CLOCK.tick(SPEED)
            pygame.display.update()
            print(maze)
        elif not END:
            traceBack(maze, START)
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