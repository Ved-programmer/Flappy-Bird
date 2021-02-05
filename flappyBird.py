import pygame
import random
from pygame.constants import K_SPACE
# import time

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SPEED = 6
score = 0

bg = pygame.transform.scale(pygame.image.load('birdupbg.png'), (WIDTH, HEIGHT))

gapBetweenPipes = int(HEIGHT//3)
pipeWidth = int(WIDTH//10)
pipeImage = pygame.image.load('birduppipe.png')

birdWidth = int(WIDTH//20)
birdHeight = int(HEIGHT//20)
birdX = int(WIDTH/2 - birdWidth / 2)
birdY = int(HEIGHT/2 - birdHeight/2)
targetBirdY = birdY
bird = pygame.transform.scale(pygame.image.load('birdup.png'), (birdWidth, birdHeight))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)

pygame.display.update()

clock = pygame.time.Clock()

gameOn = True

def putPipe(height, facing = "up"):
    customPipe = pygame.transform.scale(pygame.image.load('birduppipe.png'), (pipeWidth, height))
    y = HEIGHT - height

    if facing == "down":
        customPipe = pygame.transform.rotate(customPipe, 180)
        y = 0

    # screen.blit(customPipe, (x, y))
    return [customPipe, y]

class fullPipeObstacle:

    def __init__(self):
        self.upperPipeHeight = random.randint(1, int(HEIGHT - gapBetweenPipes))
        self.lowerPipeHeight = HEIGHT - (self.upperPipeHeight + gapBetweenPipes)
        self.upperPipe, self.upperPipeY = putPipe(self.upperPipeHeight, "down")
        self.lowerPipe, self.lowerPipeY = putPipe(self.lowerPipeHeight, "up")
        self.x = WIDTH
        self.passedThrough = False

    def update(self):
        self.x -= SPEED
        screen.blit(self.upperPipe, (self.x, self.upperPipeY))
        screen.blit(self.lowerPipe, (self.x, self.lowerPipeY))
    
def checkCollidingXWithBird(obstacle): 
    obstacleX = obstacle.x 
    return obstacleX <= birdX <= (obstacleX + pipeWidth + SPEED) or obstacleX <= birdX + birdWidth <= obstacleX + pipeWidth

def collidedWithBird(pipeObstacle):
    upperPipeHeight, lowerPipeY = pipeObstacle.upperPipeHeight, pipeObstacle.lowerPipeY
    upperPipeCollided = birdY <= upperPipeHeight
    lowerPipeCollided = (birdY + birdHeight) >= lowerPipeY

    return upperPipeCollided or lowerPipeCollided

def updateBirdY():
    global birdY, targetBirdY
    if targetBirdY - HEIGHT/100 < birdY < targetBirdY + HEIGHT/100:
        birdY += HEIGHT//150
        targetBirdY += HEIGHT//150
    else:
        birdY -= HEIGHT/50

def exitSequence():
    global score, fullPairPipes, targetBirdY, birdY, gameOn

    endScreenOn = True
    continueGame = False
    while endScreenOn:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                endScreenOn = False
            
            if e.type == pygame.KEYDOWN:
                if e.unicode == "q":
                    endScreenOn = False

                if e.unicode == "p":
                    continueGame = True
                    endScreenOn = False

        screen.fill(WHITE)

        showText(f"Press P to play again, Q to quit, your score was {score}", WIDTH/2, HEIGHT/2, True)

        pygame.display.update()

    if continueGame:
        fullPairPipes = [fullPipeObstacle()]
        score = 0
        targetBirdY = birdY = int(HEIGHT / 2)
    else:
        gameOn = False
    

fullPairPipes = [fullPipeObstacle()]

def showText(text, x = 0 , y = 0, center = False):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(text), True, WHITE, BLACK)
    textRect = text.get_rect()
    if not center:
        textRect.x = x
        textRect.y = y
    else:
        textRect.center = (x, y)
    screen.blit(text, textRect)

while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False

        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                targetBirdY -= int(HEIGHT//10)

    screen.fill(WHITE)
    screen.blit(bg, (0, 0))
    
    showText(score)
    
    # if not fullPairPipes[0].update():
    #     fullPairPipes.append(fullPipeObstacle())
    #     fullPairPipes.pop(0)

    if fullPairPipes[-1].x <= int(WIDTH//2):
        fullPairPipes.append(fullPipeObstacle())

    if fullPairPipes[0].x <= -pipeWidth:
        fullPairPipes.pop(0)
    
    updateBirdY()

    screen.blit(bird, (birdX, birdY))

    for fullPairPipe in fullPairPipes:
        if checkCollidingXWithBird(fullPairPipe):
            if collidedWithBird(fullPairPipe):
                exitSequence()
            else:
                pipeEnd = fullPairPipe.x + pipeWidth
                if birdX >= pipeEnd: 
                    score += 1 if not fullPairPipe.passedThrough else 0
                    fullPairPipe.passedThrough = True

        fullPairPipe.update()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
