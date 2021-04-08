import pygame
import json
import sys
import queue
import random

f = open('map.mz',)
maze = json.load(f)
f.close()

FOUND = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BLOCK_SIZE = 20
STEP = 0


def createObstacles(maze, amount):
    for i in range(amount):
        maze[random.randint(0,19)][random.randint(0,19)] = "#"

def findS(maze):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            if maze[int(y/20)][int(x/20)] == "S":
                sCoords = [int(y/20), int(x/20)]
                return sCoords

def findE(maze):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            if maze[int(y/20)][int(x/20)] == "E":
                sCoords = [int(y/20), int(x/20)]
                return sCoords

def validateBlock(maze, put):
    if put[0] >= 0 and put[1] >= 0 and put[0] < 20 and put[1] < 20 and maze[put[0]][put[1]] ==  " ":
            return True


def grassFIRE(maze):
    global FOUND, STEP
    if not FOUND:
        print("SEARCHING...")
        temp = FIRE.get()
        for move in [1,-1]:
            for i in range(2):
                put = [temp[0],temp[1]]
                put[i] = put[i] + move
                if validateBlock(maze,put):
                    FIRE.put(put)
                    maze[put[0]][put[1]] = str(STEP)
                    
                elif put == findS(maze):

                    print("FOUND")
                    FOUND = True
        STEP += 1


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
            CLOCK.tick(50)
            pygame.display.update()
        else:
            while not FIRE.empty:
                print(FIRE.get())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

 
    
main()