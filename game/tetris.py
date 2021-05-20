import sys, pygame
import random as rand

pygame.init()

screen_width = 500
screen_height = 690
play_width = 300
play_height = 690
block_size = 30

location_saved_block_x = 340
location_saved_block_y = 90

rows, cols = (10, 23)

timer_counter = 0

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
orange = (255,165,0)
cyan = (0,255,255)
yellow = (255,255,0)
purple = (128,0,128)
green = (72,251,0)
red = (255,0,0)
gray = (169,169,169)


BlockLocation = [[ 0 for y in range(rows)] for x in range(cols)]

is_block_active = True

screen = pygame.display.set_mode([screen_width, screen_height])

allsprites = pygame.sprite.Group()
active_blocks = []
static_blocks = []
save_blocks = []


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

    def moveDown(self):
        self.rect.y += 1*block_size
        self.y += 1

    def moveLeft(self):
        self.rect.x -= 1*block_size
        self.x -= 1

    def moveRight(self):
        self.rect.x += 1*block_size
        self.x += 1

    def getBlockLocation(self):
        return (self.x, self.y)
    
    def intersects(self,x,y):
        if(self.x == x and self.y == y):
            return True
        else:
            return False
    
    def intersect_static(self, x_offset, y_offset):
        if(self.y+y_offset >= cols):
            return True
        if(self.x+x_offset < 0):
            return True
        if(self.x+x_offset >= rows):
            return True
        for i in static_blocks:
            if(i.intersects(self.x+x_offset,self.y+y_offset)):
                return True
        return False

    def set_location(self,x,y):
        self.rect.x = x*block_size
        self.rect.y = y*block_size
        self.x = x
        self.y = y

    def set_active(self):
        BlockLocation[self.y][self.x] = 1

    def set_deactive(self):
        BlockLocation[self.y][self.x] = 0
    
    def remove_self(self):
        allsprites.remove(self)

class Tetromino():
    def __init__(self,colour,coordinates):
        x1,y1,x2,y2,x3,y3,x4,y4 = coordinates
        self.block1 = Block(colour,x1,y1)
        self.block2 = Block(colour,x2,y2)
        self.block3 = Block(colour,x3,y3)
        self.block4 = Block(colour,x4,y4)

    def intersects(self,x_offset, y_offset):
        x1,y1 = self.block1.getBlockLocation()
        x2,y2 = self.block2.getBlockLocation()
        x3,y3 = self.block3.getBlockLocation()
        x4,y4 = self.block4.getBlockLocation()
        if(y1+y_offset >= cols or y2+y_offset >= cols or y3+y_offset >= cols or y4+y_offset >= cols):
            return True
        if(x1+x_offset < 0 or x2+x_offset < 0 or x3+x_offset < 0 or x4+x_offset< 0):
            return True
        if(x1+x_offset >= rows or x2+x_offset >= rows or x3+x_offset >= rows or x4+x_offset >= rows):
            return True
        for i in static_blocks:
            if(i.intersects(x1+x_offset,y1+y_offset) or i.intersects(x2+x_offset,y2+y_offset) or i.intersects(x3+x_offset,y3+y_offset) or i.intersects(x4+x_offset,y4+y_offset)):
                return True
        return False

    def set_blocks_deactive(self):
        self.block1.set_deactive()
        self.block2.set_deactive()
        self.block3.set_deactive()
        self.block4.set_deactive()

    def set_blocks_active(self):
        self.block1.set_active()
        self.block2.set_active()
        self.block3.set_active()
        self.block4.set_active()

    def moveDown(self):
        if(self.intersects(0,1)):
            active_blocks.remove(self)
            static_blocks.append(self.block1)
            static_blocks.append(self.block2)
            static_blocks.append(self.block3)
            static_blocks.append(self.block4)
        else:
            self.set_blocks_deactive()
            self.block1.moveDown()
            self.block2.moveDown()
            self.block3.moveDown()
            self.block4.moveDown()   
            self.set_blocks_active()

    def moveLeft(self):
        if(not self.intersects(-1,0)):
            self.set_blocks_deactive()
            self.block1.moveLeft()
            self.block2.moveLeft()
            self.block3.moveLeft()
            self.block4.moveLeft()
            self.set_blocks_active()

    def moveRight(self):
        if(not self.intersects(1,0)):
            self.set_blocks_deactive()
            self.block1.moveRight()
            self.block2.moveRight()
            self.block3.moveRight()
            self.block4.moveRight()
            self.set_blocks_active()
    
    def dropDown(self):
        while(not self.intersects(0,1)):
            self.set_blocks_deactive()
            self.block1.moveDown()
            self.block2.moveDown()
            self.block3.moveDown()
            self.block4.moveDown()   
            self.set_blocks_active()
        active_blocks.remove(self)
        static_blocks.append(self.block1)
        static_blocks.append(self.block2)
        static_blocks.append(self.block3)
        static_blocks.append(self.block4)

    def rotate_clockwise(self):
        x1,y1 = self.block1.getBlockLocation()
        x2,y2 = self.block2.getBlockLocation()
        x3,y3 = self.block3.getBlockLocation()
        x4,y4 = self.block4.getBlockLocation()

        x1_rel = x1-x3
        y1_rel = y1-y3

        x2_rel = x2-x3
        y2_rel = y2-y3

        x3_rel = 0
        y3_rel = 0

        x4_rel = x4-x3
        y4_rel = y4-y3

        if(not self.block1.intersect_static(-x1+x3+y1_rel,-y1+y3-x1_rel) and not self.block2.intersect_static(-x2+x3+y2_rel,-y2+y3-x2_rel) and not self.block3.intersect_static(y3_rel,x3_rel) and not self.block4.intersect_static(-x4+x3+y4_rel,-y4+y3-x4_rel)):
            self.set_blocks_deactive()
            self.block1.set_location(x3+y1_rel,y3-x1_rel)
            self.block2.set_location(x3+y2_rel,y3-x2_rel)
            self.block3.set_location(x3+y3_rel,y3-x3_rel)
            self.block4.set_location(x3+y4_rel,y3-x4_rel)
            self.set_blocks_active()

    def remove_blocks(self):
        self.block1.remove_self()
        self.block2.remove_self()
        self.block3.remove_self()
        self.block4.remove_self()




class LineBlock(Tetromino):
    def __init__(self,x,y):
        coordinates = (x,y,x+1,y,x+2,y,x+3,y)
        Tetromino.__init__(self,cyan,coordinates)

class LeftBlock(Tetromino):
    def __init__(self,x,y):
        coordinates = (x,y+1,x+1,y,x,y,x+2,y)
        Tetromino.__init__(self,orange,coordinates)

class TBlock(Tetromino):
    def __init__(self,x,y):
        coordinates = (x,y,x+1,y+1,x+1,y,x+2,y)
        Tetromino.__init__(self,purple,coordinates)

class RightBlock(Tetromino):
    def __init__(self,x,y):
        coordinates = (x,y,x+2,y,x+1,y,x+2,y+1)
        Tetromino.__init__(self,blue,coordinates)

class SBlock(Tetromino):
    def __init__(self,x,y):
        coordinates = (x,y+1,x+1,y,x+1,y+1,x+2,y)
        Tetromino.__init__(self,green, coordinates)

class ZBlock(Tetromino):
    def __init__(self,x,y):
        coordinates = (x,y,x+1,y+1,x+1,y,x+2,y+1)
        Tetromino.__init__(self,red, coordinates)

class Cube(Tetromino):
    def __init__(self,x,y):
        coordinates = (x,y,x+1,y,x,y+1,x+1,y+1)
        Tetromino.__init__(self,yellow,coordinates)

def check_line():
    to_remove = []
    to_shift = []
    i = cols-1
    while i > 0:
        row_full = True
        for j in range(rows):
            if(BlockLocation[i][j] == 0):
                row_full = False
                break

        if(row_full):
            for j in range(rows):
                BlockLocation[i][j] = 0
            for k in static_blocks:
                x,y = k.getBlockLocation()
                if(y == i):
                    to_remove.append(k)
                    allsprites.remove(k)
                elif(y < i):
                    to_shift.append(k)
            for l in to_remove:
                l.set_deactive()
            for l in to_remove:
                static_blocks.remove(l)
            for k in to_shift:
                k.set_deactive()
            for k in to_shift:
                k.moveDown()
            for k in to_shift:
                k.set_active()
            to_remove.clear()
            to_shift.clear()
            i += 1
        i -= 1

def drawGrid():
    for x in range(0, play_width, block_size):
        for y in range(0, play_height, block_size):
            rect = pygame.Rect(x ,y, block_size,block_size)
            pygame.draw.rect(screen, gray, rect, 1)

def save_block():
    block_type = active_blocks[0]
    active_blocks[0].remove_blocks()
    active_blocks.clear()
    if(len(save_blocks) == 1):
        saved_block = save_blocks[0]
        saved_block.remove_blocks()
        if(isinstance(save_blocks[0], LineBlock)):
           active_blocks.append(create_block(0,4,2))
        elif(isinstance(save_blocks[0],LeftBlock)):
            active_blocks.append(create_block(1,4,2))
        elif(isinstance(save_blocks[0],TBlock)):
            active_blocks.append(create_block(2,4,2))
        elif(isinstance(save_blocks[0],RightBlock)):
            active_blocks.append(create_block(3,4,2))
        elif(isinstance(save_blocks[0],SBlock)):
            active_blocks.append(create_block(4,4,2))
        elif(isinstance(save_blocks[0],ZBlock)):
            active_blocks.append(create_block(5,4,2))
        elif(isinstance(save_blocks[0],Cube)):
            active_blocks.append(create_block(6,4,2))
        save_blocks.remove(saved_block)

    if(isinstance(block_type, LineBlock)):
        save_blocks.append(create_block(0,11,3))
    elif(isinstance(block_type,LeftBlock)):
        save_blocks.append(create_block(1,11,3))
    elif(isinstance(block_type,TBlock)):
        save_blocks.append(create_block(2,11,3))
    elif(isinstance(block_type,RightBlock)):
        save_blocks.append(create_block(3,11,3))
    elif(isinstance(block_type,SBlock)):
        save_blocks.append(create_block(4,11,3))
    elif(isinstance(block_type,ZBlock)):
        save_blocks.append(create_block(5,11,3))
    elif(isinstance(block_type,Cube)):
        save_blocks.append(create_block(6,11,3))


def create_block(rand_num,x,y):
    if(rand_num == 0):
        return LineBlock(x,y)
    elif(rand_num == 1):
        return LeftBlock(x,y)
    elif(rand_num == 2):
        return TBlock(x,y)
    elif(rand_num == 3):
        return RightBlock(x,y)
    elif(rand_num == 4):
        return SBlock(x,y)
    elif(rand_num == 5):
        return ZBlock(x,y)
    elif(rand_num == 6):
        return Cube(x,y)


clock = pygame.time.Clock()

active_blocks.append(LeftBlock(4,2))

#game loop
while 1:
    clock.tick(30)
    screen.fill(black)
    drawGrid()

    if(len(active_blocks) == 0):
        check_line()
        rand_num = rand.randrange(7)
        active_blocks.append(create_block(rand_num,4,2))

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
            if(event.key == pygame.K_UP) or (event.key == pygame.K_w):
                for i in active_blocks:
                    i.rotate_clockwise()
            if(event.key == pygame.K_SPACE):
                for i in active_blocks:
                    i.dropDown()
            if(event.key == pygame.K_LSHIFT) or (event.key == pygame.K_RSHIFT):
                save_block()

    
    timer_counter += 1
    allsprites.draw(screen)
    pygame.display.flip()

