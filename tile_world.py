import pygame
import pygame.locals

import random
import cv2


class TileManager(object):
    '''
        Load tileset image into memory
    '''
    def __init__(self, tile_width, tile_height):
        self.cache = {}
        self.tile_width = tile_width
        self.tile_height = tile_height

    def load(self, filename):
        if filename in self.cache:
            return self.cache[filename]
        else:
            table = self.load_tile_table(filename, self.tile_width, self.tile_height)
            self.cache[filename] = table
            return table

    def load_tile_table(self, filename, tile_width, tile_height):
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/tile_width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/tile_height):
                rect = (tile_x*tile_width, tile_y*tile_height, tile_width, tile_height)
                line.append(image.subsurface(rect))
        return tile_table, len(tile_table), len(tile_table[0])

class TileCanvaWindow(object):
    def __init__(self, width, height, tile_width, tile_height, background=((255,255,255))):
        self.width = width
        self.height = height
        self.background = background
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(self.background)

        self.overlays = pygame.sprite.RenderUpdates()

    def set(self, img, x, y):
        self.screen.blit(img, (x * self.tile_width, y * self.tile_height))
   
    def draw(self):
        self.overlays.draw(self.screen)
        pygame.display.flip()

if __name__=='__main__':
    TILE_WIDTH = 32
    TILE_HEIGHT = 32
    WIDTH = 320 + (8 * 32)
    HEIGHT = 320 + (32 * 32)
    NUM_TILE_WIDTH = WIDTH / TILE_WIDTH
    NUM_TILE_HEIGHT = HEIGHT / TILE_HEIGHT
    BACKGROUND = ((0, 0, 0))

    pygame.init()
    canva = TileCanvaWindow(WIDTH, HEIGHT, TILE_WIDTH, TILE_HEIGHT, BACKGROUND)
    tile_manager = TileManager(TILE_WIDTH, TILE_HEIGHT)
    table, num_tile_x, num_tile_y = tile_manager.load('default.bmp')
    
    clock = pygame.time.Clock()
    clock.tick(15)

    game_over = False
    

    bx = 10 + 1
    by = 0
    ctx = 0
    cty = 0

    def change_cell(x, y):
        canva.set(table[ctx][cty], x, y)

    for x in xrange(num_tile_x):
        for y in xrange(num_tile_y):
            canva.set(table[x][y], bx + x, by + y)
    t = 0
    while not game_over:
        canva.draw()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                x = (x / TILE_WIDTH)
                y = (y / TILE_HEIGHT)
                if x < 10 and y < 10:
                    change_cell(x, y)
                    rect = pygame.Rect(0, 0, 320, 320)
                    sub = canva.screen.subsurface(rect)
                    pygame.image.save(sub, "%d.jpg" % t) 
                    t += 1
                elif x > 10:
                    ctx = x - 11
                    cty = y
                    print ctx, cty
                    
                
