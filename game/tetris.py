import sys, pygame
import random as rand

pygame.init()

screen_width = 800
screen_height = 700
play_width = 300
play_height = 600
block_size = 30

rows, cols = (10, 22)

timer_counter = 0

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
orange = (255,255,0)
cyan = (0,255,255)
yellow = (255,255,0)
purple = (128,0,128)


BlockLocation = [[ 0 for y in range(cols)] for x in range(rows)]

is_block_active = True

screen = pygame.display.set_mode([screen_width, screen_height])

allsprites = pygame.sprite.Group()
active_blocks = []
static_blocks = []

class Block(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([block_size, block_size])
        self.image.fill(colour)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x*block_size
        self.rect.y = y*block_size

        allsprites.add(self)

        BlockLocation[self.x][self.y] = 1

    def moveDown(self):
        BlockLocation[self.x][self.y] = 0
        self.rect.y += 1*block_size
        self.y += 1
        BlockLocation[self.x][self.y] = 1

    def moveLeft(self):
        BlockLocation[self.x][self.y] = 0
        self.rect.x -= 1*block_size
        self.x -= 1
        BlockLocation[self.x][self.y] = 1

    def moveRight(self):
        BlockLocation[self.x][self.y] = 0
        self.rect.x += 1*block_size
        self.x += 1
        BlockLocation[self.x][self.y] = 1

    def getBlockLocation(self):
        return (self.x, self.y)
    
    def intersects(self,x,y):
        if(self.x == x and self.y == y):
            return True
        else:
            return False

class Tetromino():
    def __init__(self,colour,coordinates):
        x1,x2,x3,x4,y1,y2,y3,y4 = coordinates
        self.block1 = Block(colour,x1,y1)
        self.block2 = Block(colour,x2,y2)
        self.block3 = Block(colour,x3,y3)
        self.block4 = Block(colour,x4,y4)

    def intersects(self):
        x1,y1 = self.block1.getBlockLocation()
        x2,y2 = self.block2.getBlockLocation()
        x3,y3 = self.block3.getBlockLocation()
        x4,y4 = self.block4.getBlockLocation()
        if(y1 >= cols-1 or y2 >= cols-1 or y3 >= cols-1 or y4 >= cols-1):
            return True
        for i in static_blocks:
            if(i.intersects(x1,y1+1) or i.intersects(x2,y2+1) or i.intersects(x3,y3+1) or i.intersects(x4,y4+1)):
                return True
        return False

    def moveDown(self):
        if(self.intersects()):
            active_blocks.remove(self)
            static_blocks.append(self.block1)
            static_blocks.append(self.block2)
            static_blocks.append(self.block3)
            static_blocks.append(self.block4)
        else:
            self.block1.moveDown()
            self.block2.moveDown()
            self.block3.moveDown()
            self.block4.moveDown()

    def moveLeft(self):
        print("Not implemented yet")

    def moveRight(self):
        print("Not implemented yet")

class LineBlock(Tetromino):
    def __init__(self):
        coordinates = (4,5,6,7,2,2,2,2)
        Tetromino.__init__(self,cyan,coordinates)

class LeftBlock(Tetromino):
    def __init__(self):
        coordinates = (4,4,5,6,3,2,2,2)
        Tetromino.__init__(self,orange,coordinates)

class TBlock(Tetromino):
    def __init__(self):
        coordinates = (4,5,5,6,2,2,3,2)
        Tetromino.__init__(self,purple,coordinates)

class RightBlock(Tetromino):
    def __init__(self):
        coordinates = (4,5,6,6,2,2,2,3)
        Tetromino.__init__(self,blue,coordinates)


def is_empty(x,y):
    if(BlockLocation[x][y] == 0):
        return True
    else:
        return False

clock = pygame.time.Clock()

active_blocks.append(LeftBlock())

#game loop
while 1:
    clock.tick(30)
    screen.fill(black)

    if(len(active_blocks) == 0):
        print(rand.randrange(7))
        active_blocks.append(RightBlock())

    if(timer_counter == 10):
        for i in active_blocks:
            i.moveDown()
            timer_counter = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                for i in active_blocks:
                    i.moveLeft()
            if(event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                for i in active_blocks:
                    i.moveRight()
    
    timer_counter += 1
    allsprites.draw(screen)
    pygame.display.flip()
    