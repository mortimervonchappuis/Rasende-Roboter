import pygame
from robot_boards import random_grid
import sys
from time import sleep
from grid import *
from random import choice
from copy import deepcopy

CELL_W, CELL_H = 48, 48
SIZE = WIDTH, HEIGHT = CELL_W * 16, CELL_H * 16

# LINES
SMALL = 1
MEDIUM = 3
LARGE = 4
BIG = 5

# COLOURS 
BLACK  = [0x00, 0x00, 0x00]
GREY   = [0x88, 0x88, 0x88]
WHITE  = [0xff, 0xff, 0xff]
RED    = [0xff, 0x00, 0x00]
GREEN  = [0x00, 0xee, 0x00]
YELLOW = [0xff, 0xff, 0x33]
BLUE   = [0x00, 0x88, 0xff]

DARK = lambda c, l=0.7: [int(c[0] * l), int(c[1] * l), int(c[2] * l)]

DARK_RED    = DARK(RED)
DARK_GREEN  = DARK(GREEN)
DARK_YELLOW = DARK(YELLOW)
DARK_BLUE   = DARK(BLUE)

COLOURS = {
	'black': BLACK,
	'grey': GREY,
	'white': WHITE,
	'red': RED,
	'green': GREEN,
	'yellow': YELLOW,
	'blue': BLUE,
}


pygame.init()
screen = pygame.display.set_mode(SIZE)
grid = random_grid()

RED_F    = Figure('red',    ( 3,  3), grid)
YELLOW_F = Figure('yellow', ( 3, 12), grid)
GREEN_F  = Figure('green',  (12,  3), grid)
BLUE_F   = Figure('blue',   (12, 12), grid)


directions = {
	119: 'north', 
	273: 'north', 
	115: 'south', 
	274: 'south', 
	100: 'east', 
	275: 'east', 
	97: 'west', 
	276: 'west',
}

state = {'mode': 'validate', 'movements': None, 'position': None, 'target': None}

def draw_grid():
	global grid, state

	if state['target'] is not None:
		target = state['target']
		j, i = target.pos
		pygame.draw.rect(screen, DARK(COLOURS[target.colour], 0.7), (i * CELL_H, j * CELL_W, CELL_H, CELL_W))
		pygame.draw.rect(screen, DARK(COLOURS[target.colour], 0.6), (i * CELL_H + MEDIUM, j * CELL_W + MEDIUM, CELL_H - 2 * MEDIUM, CELL_W - 2 * MEDIUM))
		pygame.draw.rect(screen, DARK(COLOURS[target.colour], 0.7), (i * CELL_H + BIG, j * CELL_W + BIG, CELL_H - 2 * BIG, CELL_W - 2 * BIG))

	
	# GRID
	for i in range(16):
		if i != 8:
			pygame.draw.line(screen, GREY, 
				(0, i * CELL_W), 
				(HEIGHT, i * CELL_W), SMALL)
			pygame.draw.line(screen, GREY, 
				(i * CELL_H, 0), 
				(i * CELL_H, WIDTH), SMALL)
		else:
			pygame.draw.line(screen, GREY, 
				(0, i * CELL_W), 
				(7 * CELL_H, i * CELL_W), SMALL)
			pygame.draw.line(screen, GREY, 
				(9 * CELL_H, i * CELL_W), 
				(HEIGHT, i * CELL_W), SMALL)
			pygame.draw.line(screen, GREY, 
				(i * CELL_H, 0), 
				(i * CELL_H, 7 * CELL_W), SMALL)
			pygame.draw.line(screen, GREY, 
				(i * CELL_H, 9 * CELL_W), 
				(i * CELL_H, WIDTH), SMALL)

	for i in range(16):
		for j in range(16):
			square = grid[i, j]

			# WALLS
			if square.north:
				pygame.draw.line(screen, BLACK, 
					(j * CELL_H, i * CELL_W), 
					((j + 1) * CELL_H, i * CELL_W), 
					LARGE)
			if square.east:
				pygame.draw.line(screen, BLACK, 
					((j + 1) * CELL_H, i * CELL_W), 
					((j + 1) * CELL_H, (i + 1) * CELL_W), 
					LARGE)
			if square.south:
				pygame.draw.line(screen, BLACK, 
					(j * CELL_H, (i + 1) * CELL_W), 
					((j + 1) * CELL_H, (i + 1) * CELL_W), 
					LARGE)
			if square.west:
				pygame.draw.line(screen, BLACK, 
					(j * CELL_H, i * CELL_W), 
					(j * CELL_H, (i + 1) * CELL_W),  
					LARGE)


def draw_figures():
	global grid

	for i in range(16):
		for j in range(16):
			if (figure := grid[i, j].figure) is not None:
				colour = COLOURS[figure.colour]
				pygame.draw.circle(screen, DARK(colour, 0.3), 
					(j * CELL_H + CELL_H//2, i * CELL_W + CELL_W//2), 
					min(CELL_H, CELL_W)//2 - BIG)
				pygame.draw.circle(screen, DARK(colour, 0.7), 
					(j * CELL_H + CELL_H//2, i * CELL_W + CELL_W//2), 
					min(CELL_H, CELL_W)//2 - BIG - SMALL)


def translate(pos):
	x, y = pos
	return y//CELL_W, x//CELL_H


def translate_inv(pos):
	x, y = pos
	return int((y + 0.5) * CELL_W), int((x + 0.5) * CELL_H)


reset = lambda: screen.fill(WHITE)
update = lambda: pygame.display.update()

reset()
draw_grid()
draw_figures()
update()

grid_copy = deepcopy(grid)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == 5 and state['mode'] in ('figure', 'direction'):
			i, j = translate(event.__dict__['pos'])
			reset()
			if grid[i, j].figure is not None:
				state['movements'] = grid.search((i, j))
				for b in state['movements'].values():
					if b is not None:
						pygame.draw.line(screen, 
							DARK(COLOURS[grid[i, j].figure.colour]), 
							translate_inv((i, j)), 
							translate_inv(b), 
							MEDIUM)
				state['mode'] = 'direction'
				state['position'] = (i, j)
		elif event.type == 2:
			key = event.__dict__['key']
			if key == 13 and state['mode'] == 'validate':
				state['target'] = None
				state['mode'] = 'figure'
				quater = choice(grid.quaters)
				state['target'] = choice([square for square in quater.colours if square.figure is None or square.figure.colour != square.colour])
				grid_copy = deepcopy(grid)
				reset()
				draw_grid()
				draw_figures()
				update()
			if key == 8:
				grid = grid_copy
				grid_copy = deepcopy(grid)
				state['target'] = grid[state['target'].pos]
				state['mode'] = 'figure'
				state['movements'] = None
				state['position'] = None
				reset()
				draw_grid()
				draw_figures()
				update()
			if key not in directions or state['mode'] != 'direction':
				continue
			direction = directions[key]
			destination = state['movements'][direction]
			if destination is not None:
				grid[destination].figure = grid[i, j].figure
				grid[i, j].figure = None
				state['mode'] = 'figure'
				target = state['target']
				reset()
				if target is not None and target.figure is not None and target.figure.colour == target.colour:
					state['mode'] = 'validate'
					draw_grid()
					draw_figures()
					update()
		draw_grid()
		draw_figures()
		update()
	sleep(0.1)
