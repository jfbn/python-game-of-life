import pygame, sys, random
import random
from configuration import *

pygame.init()

def create_grid(cells_in_dimension):
    """Returns a 2d list (lists stored in a list) filled with 1s or 0s.

    If 'running' variable is set to true, approximately half the elements will be assigned to 0, the others to 1 (random() returns a float between 0.0 and 1.0, we multiply it by 10 and compare it to 5))
    If 'running' is set to false, all elements will be 0

    Keyword arguments:
    cells_in_dimension -- how many elements we want in each row and column
    """
    if running:
        return [[0 if random.random()*10 > 5 else 1 for i in range(cells_in_dimension)] for j in range(cells_in_dimension)]
    return [[0 for i in range(cells_in_dimension)] for j in range(cells_in_dimension)]

def create_heat_map(cells_in_dimension):
    """Returns a 2d list (lists stored in a list) filled with 0s
    Later this value will be incremented whenever a cell has been alive at the correlating list of cells"""
    return [[0 for i in range(cells_in_dimension)] for j in range(cells_in_dimension)]

def display_cells():
    """Draws a rectangle on the screen for each element in our 2D list 'cells'.
    The color of the rectangle is determined by the value of the element.    
    """
    for i in range(CELLS_PER_DIMENSION):
        for y in range(CELLS_PER_DIMENSION):
            # the cell is alive
            if cells[i][y] == 1:
                pygame.draw.rect(screen, CELL_COLOR, (i * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            else:
                pygame.draw.rect(screen, BG_COLOR, (i * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            # draw a border
            pygame.draw.rect(screen, BORDER_COLOR, (i * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            
def display_heat():
    """Visualizes how often the given cell has been alive by drawing a transparent red rectangle"""
    for i in range(CELLS_PER_DIMENSION):
        for y in range(CELLS_PER_DIMENSION):
            s.set_alpha(min(heat_map[i][y], 254))
            screen.blit(s, (i*CELL_SIZE, y*CELL_SIZE))

def count_live_neighbours(pos1, pos2):
    """Returns the amount of 'living' neighbours of the given cell.

    Imagine a grid like so:
    X X X 
    X 0 X
    X X X
    When checking the neighbours of 0, we must access elements that are located at these positions relative to itself:
    top left:       x = -1  , y = -1
    top midle:      x = 0   , y = -1   
    top right:      x = 1   , y = -1
    middle left:    x = -1  , y = 0
    self:           x = 0   , y = 0
    middle right:   x = 1   , y = 0
    bottom left:    x = -1  , y = 1
    bottom middle:  x = 0   , y = 1
    bottom right:   x = -1  , y = 1

    Because this method also checks itself, we need to subtract 1 from alive_count if the given cell (itself) is also alive

    Keyword arguments:
    pos1 -- the x coordinate of the cell (also identifies which list in our cells list the element is stored in)
    pos2 -- the y coordinate of the cell (also identifies the index of its position in its parent list)    
    """
    alive_count = 0
    for i in range(pos1-1, pos1+2):
        for y in range(pos2-1, pos2+2):
            if i >= 0 and i < CELLS_PER_DIMENSION and y >= 0 and y < CELLS_PER_DIMENSION:
                if cells[i][y] == 1:
                    alive_count += cells[i][y]
    if cells[pos1][pos2] == 1:
        alive_count -= 1
    return alive_count

def invert_cells(to_invert):
    """Inverts the value of cells

    Keyword arguments:
    to_invert -- a list of tuples that each hold an x and y value, representing their position in the grid (and also used to lookup the cell in our 2d list)
    """
    for cell in to_invert:
        x = cell[0]
        y = cell[1]
        if cells[x][y] == 1:
            cells[x][y] = 0
        else:
            cells[x][y] = 1

def invert_cell(event):
    """Inverts a cell at the mouses position
    Reads the position of the mouse from the event, calculates which cell belongs to that position, inverts the value of the cell

    Keyword arguments:
    event -- carries information about the mousepress event - such as the position of the mouse when the event was fired
    """
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    cell_x = mouse_x // CELL_SIZE
    cell_y = mouse_y // CELL_SIZE

    if cells[cell_x][cell_y] == 1:
        cells[cell_x][cell_y] = 0
    else:
        cells[cell_x][cell_y] = 1
   
def update_board(): 
    """Updates the status of the board. 
    Iterates over all cells, gets their neighbour count, and determines which cells need inverting before next frame update.
    """
    to_invert = []
    alive_neighbours = 0

    for x in range(CELLS_PER_DIMENSION):
        for y in range(CELLS_PER_DIMENSION):
            alive_neighbours = count_live_neighbours(x, y)
            # the cell is alive
            if cells[x][y] == 1:
                if SHOW_HEATMAP:
                    # increase the heat amount of the location
                    heat_map[x][y] += HEAT_INCR
                if alive_neighbours < MIN_ALIVE_NEIGHBOURS or alive_neighbours > MAX_ALIVE_NEIGHBOURS:
                    to_invert.append((x, y))
            else:
                if alive_neighbours == ALIVE_FOR_RESPAWN:
                    to_invert.append((x, y))
    invert_cells(to_invert)

"""Determines whether or not the rules of the game should apply for the next frame update"""
running = False 
"""Determines whether or not a custom grid has been designed by the user"""
custom_grid = False 

screen = pygame.display.set_mode(size)
cells = create_grid(CELLS_PER_DIMENSION)

if SHOW_HEATMAP:
    heat_map = create_heat_map(CELLS_PER_DIMENSION)
    s = pygame.Surface((CELL_SIZE, CELL_SIZE))
    s.fill((204, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #if you press a mouse butotn
        if event.type == pygame.MOUSEBUTTONDOWN:
            custom_grid = True
            invert_cell(event)

        #if you press a key
        if event.type == pygame.KEYDOWN:

            #if you pressed R
            if event.key == 114:
                running = False
                custom_grid = False
                cells = create_grid(CELLS_PER_DIMENSION)

            #if you pressed space
            if event.key == 32:
                running = True
                if not custom_grid:
                    cells = create_grid(CELLS_PER_DIMENSION)
                    if SHOW_HEATMAP:
                        heat_map = create_heat_map(CELLS_PER_DIMENSION)
                    
            #if you pressed enter
            if event.key == 13:
                cells = create_grid(CELLS_PER_DIMENSION)

    screen.fill(black)
    display_cells()
    #pygame.display.update()
    if SHOW_HEATMAP:
        display_heat()
    pygame.display.flip()
    if running:   
        update_board()