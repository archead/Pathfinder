import pygame, json, sys, queue, random, argparse, math

parser = argparse.ArgumentParser(description="Find optimal path for a given map file.")
parser.add_argument('-i', '--input', default='custom.mz', type=str, help='Input map file. (default: star.mz)')
parser.add_argument('-s', '--speed', type=int, help='Speed for alrgorithm execution, recommended values: 50-150')
parser.add_argument('-v','--verbose', action='store_true', help='Display verbose output.')
parser.add_argument('-r','--random', type=int, default=0, help='Amount of random obstacle blocks generated, recommended values: 50-150 (default: 0)')
parser.add_argument('-a','--algorithm', type=str, default="astar", help='Selects algorithm, currently available: grassfire, astar (BETA)')

args = parser.parse_args()

f = open(args.input)
maze = json.load(f)
f.close()

# Some default paramenters
# Change RGB values for desired colors
SPEED = args.speed or 100 # Determines how fast the algorithm will run, recommeded values: 10-100
BLACK = (31, 31, 31)
BACKGROUND = (195, 181, 255)
WHITE = (255, 255, 255)
RED = (252, 159, 159)
BLUE = (102,159,250)
GREEN = (167, 255, 120)
FOUND = False # DO NOT CHANGE
WINDOW_HEIGHT = 400 # DO NOT CHANGE
WINDOW_WIDTH = 400 # DO NOT CHANGE
BLOCK_SIZE = 20 # DO NOT CHANGE
STEP = 1 # DO NOT CHANGE

# Creates random obstacles, use the desired maze and the ammount of obstacles as the parameters
def createObstacles(maze, amount):
    for i in range(amount):
        randX = random.randint(0,19)
        randY = random.randint(0,19)
        if maze[randY][randX] != "E" or maze[randY][randX] != "S":
            maze[randY][randX] = "#"

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
                eCoords = [int(y/20), int(x/20)]
                return eCoords

def h(block):
    global maze
    S = findS(maze)
    E = [block[0],block[1]]
    return math.sqrt((E[0]-S[0])**2+(E[1]-S[1])**2)

# Validates if the next step is valid
def validateBlock(maze, put):
    if put[0] >= 0 and put[1] >= 0 and put[0] < 20 and put[1] < 20 and maze[put[0]][put[1]] ==  " ":
        return True

# Identical to validateBlock() but used for A*
def validateH(maze, put):
    if put[0] >= 0 and put[1] >= 0 and put[0] < 20 and put[1] < 20 and maze[put[0]][put[1]] !=  "#" and maze[put[0]][put[1]] !=  "S" and maze[put[0]][put[1]] !=  "E" and maze[put[0]][put[1]] ==  " ":
            return True

# Identical to validateBlock() but used for traceBack()
def validateStep(maze, put, prev):
    global END
    if put[0] >= 0 and put[1] >= 0 and put[0] < 20 and put[1] < 20 and maze[put[0]][put[1]] !=  "#" and maze[put[0]][put[1]] !=  " " and maze[put[0]][put[1]] !=  "S":
        if int(maze[put[0]][put[1]]) < int(maze[prev[0]][prev[1]]) and maze[put[0]][put[1]] !=  "0":
            return True
        elif maze[put[0]][put[1]] ==  "0":
            print("PATH FOUND!")
            END = True

# Returns the shortest possible step that should be taken out of the 4 or less possibilities
def smallestStep(comp):
    nextBlock = 999
    smallest = []
    for coord in comp:
        if int(h(coord)) + STEP <= nextBlock:
            nextBlock = int(h(coord)) + STEP
            smallest = coord
    return smallest
# Grassfire algorithm implementation
def grassFire(maze):
    global FOUND, STEP, START
    if not FOUND:
        temp = FIRE.get()
        for move in [1,-1]:
            for i in range(2):
                put = [temp[0],temp[1]]
                put[i] += move
                if validateBlock(maze,put):
                    FIRE.put(put)
                    maze[put[0]][put[1]] = str(STEP)
                elif put == findS(maze):
                    maze[put[0]][put[1]] = str(999)
                    E = findE(maze)
                    maze[E[0]][E[1]] = str(0)
                    FOUND = True
        STEP += 1

# A* algorithm implementation
def aStar(maze):
    global FOUND, STEP, START
    comp = []
    nextBlock = 999
    if not FOUND:
        temp = FIRE.get()
        for move in [1,-1]:
            for i in range(2):
                put = [temp[0],temp[1]]
                put[i] += move
                if validateH(maze, put):
                    maze[put[0]][put[1]] = str(STEP)
                    comp.append(put)
                elif put == findS(maze):
                    maze[put[0]][put[1]] = str(999)
                    E = findE(maze)
                    maze[E[0]][E[1]] = str(0)
                    FOUND = True
    if not FOUND:
        nextStep = smallestStep(comp)
        FIRE.put(nextStep)
        STEP += 1

# Calculates the step needed to get to the "E" block
# appends the coordinates into the PATH array
# stops after reaching the "E" block
def traceBack(maze, block):
    global PATH, START
    for move in [1,-1]:
            for i in range(2):
                put = [block[0],block[1]]
                put[i] += move
                if validateStep(maze, put, block):
                    START = put
                    block = put
                    PATH.append(put)
                                       
# Rendering function
def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if maze[int(y/20)][int(x/20)] != " ":
                pygame.draw.rect(SCREEN, BLUE, rect)
            if maze[int(y/20)][int(x/20)] == " ":
                pygame.draw.rect(SCREEN, BACKGROUND, rect)
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
    print("Beginning Search...")

    while True:
        if args.algorithm == "astar" and not FOUND:
            aStar(maze)
        elif args.algorithm == "grassfire" and not FOUND:
            grassFire(maze)
        drawGrid()
        pygame.display.update()

        if not FOUND:
            CLOCK.tick(SPEED)
            if args.verbose:
                print(maze)
        elif not END:
            traceBack(maze, START)
            CLOCK.tick(SPEED)
            if args.verbose and END:
                print("Steps taken:", STEP)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Change second value to desired ammount of obstacles
# NOTE: HIGH AMMOUNT OF OBSTACLES CAN POTENTIALLY CRASH THE PROGRAM
# Recommended ammount: 100-150
# If program does not start, run again to generate new obstacles     
createObstacles(maze, args.random)
main()