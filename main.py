import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from robot_boards import random_grid
import sys
from time import sleep
from grid import *
from random import choice
from copy import deepcopy
from playsound import playsound
from threading import Thread


MAN = """The GOAL_SQUARE is the coloured one. The GOAL is to move the robot with the same colour on it. Robots are allowed to move in the directions NORTH, EAST, SOUTH and WEST. Once a robot is moved in one of those directions, it moves until it hits a wall or another robot. This counts as a single MOVE. All players play simultaniously. Once a player finds a solution, that player may proclaim the number of moves and hit the bell (SPACE). Now a countdown of 30 seconds starts during which all other players may try to find faster solutions, which they themselves then may proclaim. The countdown ends with the same bell sound that it started with. You can cancel the countdown by pressing SPACE again.
After the countdown the player who proclaimed the fastest solution must present it. 
If the player cannot do so, the player with the second fastest solution may present their solution, afterwards the third and so on.
To move a robot, you have to click on it and then choose the direction (↑, ←, ↓, →) or alternatively (W, A, S, D). You can reset the board by pressing BACKSPACE. If you want to commit to a solution you can press ENTER. Afterwards a new GOAL_SQUARE is selected and the next round begins. You can end the game by pressing ESC."""


def print_title(title):
	print("""
	┌─{0}─┐
	│ {1} │
	└─{0}─┘
""".format(len(title)*'─', title.upper()))


os.system('clear')
print_title('RICOCHET ROBOT')
print(MAN)


BELL_FILE = 'bell.mp3'
TIME = 30

CELL_W, CELL_H = 60, 60
SIZE = WIDTH, HEIGHT = CELL_W * 16, CELL_H * 16

# LINES
TINY = 1
SMALL = 2
MEDIUM = 3
LARGE = 4
BIG = 5

LINE_W = BIG

# COLOURS 
BLACK  = [0x00, 0x00, 0x00]
GREY   = [0x88, 0x88, 0x88]
WHITE  = [0xff, 0xff, 0xff]
RED    = [0xcc, 0x00, 0x00]
GREEN  = [0x00, 0xcc, 0x55]
YELLOW = [0xff, 0xdd , 0x55]
BLUE   = [0x00, 0x88, 0xcc]

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

STATE = {'mode': 'figure', 'movements': None, 'position': None, 'target': None, 'counter': 0, 'countdown': False}

def draw_grid():
	global grid, STATE

	if STATE['target'] is not None:
		target = STATE['target']
		j, i = target.pos
		pygame.draw.rect(screen, DARK(COLOURS[target.colour], 0.8), (i * CELL_H, j * CELL_W, CELL_H, CELL_W))
		pygame.draw.rect(screen, DARK(COLOURS[target.colour], 0.6), (i * CELL_H + MEDIUM, j * CELL_W + MEDIUM, CELL_H - 2 * MEDIUM, CELL_W - 2 * MEDIUM))
		pygame.draw.rect(screen, DARK(COLOURS[target.colour], 0.8), (i * CELL_H + BIG, j * CELL_W + BIG, CELL_H - 2 * BIG, CELL_W - 2 * BIG))

	if STATE['counter']:
		font = pygame.font.SysFont(None, 128)
		img = font.render(str(STATE['counter']), True, BLACK)
		screen.blit(img, (int((7.6 if STATE['counter'] < 10 else 7.2) * CELL_W), int(7.35 * CELL_H)))
	# GRID
	for i in range(16):
		if i != 8:
			pygame.draw.line(screen, GREY, 
				(0, i * CELL_W), 
				(HEIGHT, i * CELL_W), TINY)
			pygame.draw.line(screen, GREY, 
				(i * CELL_H, 0), 
				(i * CELL_H, WIDTH), TINY)
		else:
			pygame.draw.line(screen, GREY, 
				(0, i * CELL_W), 
				(7 * CELL_H, i * CELL_W), TINY)
			pygame.draw.line(screen, GREY, 
				(9 * CELL_H, i * CELL_W), 
				(HEIGHT, i * CELL_W), TINY)
			pygame.draw.line(screen, GREY, 
				(i * CELL_H, 0), 
				(i * CELL_H, 7 * CELL_W), TINY)
			pygame.draw.line(screen, GREY, 
				(i * CELL_H, 9 * CELL_W), 
				(i * CELL_H, WIDTH), TINY)

	for i in range(16):
		for j in range(16):
			square = grid[i, j]

			# WALLS
			if square.north:
				pygame.draw.line(screen, BLACK, 
					(j * CELL_H - LINE_W//2, i * CELL_W), 
					((j + 1) * CELL_H + LINE_W//2, i * CELL_W), 
					LINE_W)
			if square.east:
				pygame.draw.line(screen, BLACK, 
					((j + 1) * CELL_H, i * CELL_W - LINE_W//2), 
					((j + 1) * CELL_H, (i + 1) * CELL_W + LINE_W//2), 
					LINE_W)
			if square.south:
				pygame.draw.line(screen, BLACK, 
					(j * CELL_H - LINE_W//2, (i + 1) * CELL_W), 
					((j + 1) * CELL_H + LINE_W//2, (i + 1) * CELL_W), 
					LINE_W)
			if square.west:
				pygame.draw.line(screen, BLACK, 
					(j * CELL_H, i * CELL_W - LINE_W//2), 
					(j * CELL_H, (i + 1) * CELL_W + LINE_W//2),  
					LINE_W)


def draw_figures():
	global grid

	for i in range(16):
		for j in range(16):
			if (figure := grid[i, j].figure) is not None:
				colour = COLOURS[figure.colour]
				pygame.draw.circle(screen, DARK(colour, 0.5), 
					(j * CELL_H + CELL_H//2, i * CELL_W + CELL_W//2), 
					min(CELL_H, CELL_W)//2 - BIG)
				pygame.draw.circle(screen, DARK(colour, 0.8), 
					(j * CELL_H + CELL_H//2, i * CELL_W + CELL_W//2), 
					min(CELL_H, CELL_W)//2 - BIG - SMALL)


def translate(pos):
	x, y = pos
	return y//CELL_W, x//CELL_H


def translate_inv(pos):
	x, y = pos
	return int((y + 0.5) * CELL_W), int((x + 0.5) * CELL_H)


def countdown():
	global STATE, BELL_FILE, TIME			
	Thread(target=lambda: playsound(BELL_FILE)).start()
	for _ in range(TIME):
		sleep(1)
		if not STATE['countdown']:
			return
	Thread(target=lambda: playsound(BELL_FILE)).start()


reset = lambda: screen.fill(WHITE)
update = lambda: pygame.display.update()

reset()
draw_grid()
draw_figures()
update()

quater = choice(grid.quaters)
STATE['target'] = choice([square for square in quater.colours if square.figure is None or square.figure.colour != square.colour])
grid_copy = deepcopy(grid)
grid_copy = deepcopy(grid)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			os.system('clear')
			quit()
		elif event.type == 5 and STATE['mode'] in ('figure', 'direction'):
			i, j = translate(event.__dict__['pos'])
			STATE['countdown'] = False
			reset()
			if grid[i, j].figure is not None:
				STATE['movements'] = grid.search((i, j))
				for pos in STATE['movements'].values():
					if pos is not None:
						x, y = pos
						colour = COLOURS[grid[i, j].figure.colour]
						pygame.draw.circle(screen, DARK(colour, 0.3), 
							(y * CELL_H + CELL_H//2, x * CELL_W + CELL_W//2), 
							min(CELL_H, CELL_W)//5 - BIG)
						pygame.draw.circle(screen, DARK(colour, 0.8), 
							(y * CELL_H + CELL_H//2, x * CELL_W + CELL_W//2), 
							min(CELL_H, CELL_W)//5 - BIG - TINY)
						pygame.draw.line(screen, 
							DARK(colour), 
							translate_inv((i, j)), 
							translate_inv(pos), 
							MEDIUM)
				STATE['mode'] = 'direction'
				STATE['position'] = (i, j)
		elif event.type == 2:
			key = event.__dict__['key']
			if key == 27:
				os.system('clear')
				quit()
			if key == 32:
				STATE['countdown'] = not STATE['countdown']
				if STATE['countdown']:
					Thread(target=countdown).start()
			if key == 13 and STATE['mode'] == 'validate':
				quater = choice([quater for quater in grid.quaters if any(square.figure is None or square.figure.colour != square.colour for square in quater.colours)])
				STATE['target'] = choice([square for square in quater.colours if square.figure is None or square.figure.colour != square.colour])
				STATE['mode'] = 'figure'
				STATE['counter'] = 0
				grid_copy = deepcopy(grid)
				reset()
				draw_grid()
				draw_figures()
				update()
			if key == 8:
				grid = grid_copy
				grid_copy = deepcopy(grid)
				STATE['target'] = grid[STATE['target'].pos]
				STATE['mode'] = 'figure'
				STATE['movements'] = None
				STATE['position'] = None
				STATE['counter'] = 0
				reset()
				draw_grid()
				draw_figures()
				update()
			if key not in directions or STATE['mode'] != 'direction':
				break
			direction = directions[key]
			origin = STATE['position']
			destination = STATE['movements'][direction]
			if destination is not None:
				grid[destination].figure = grid[origin].figure
				if origin  == destination:
					raise Exception('ARGH')
				grid[origin].figure = None
				STATE['counter'] += 1
				target = STATE['target']
				reset()
				STATE['movements'] = grid.search(destination)
				for pos in STATE['movements'].values():
					if pos is not None and (target is None or target.figure is None or target.figure.colour != target.colour):
						i, j = pos
						colour = COLOURS[grid[destination].figure.colour]
						pygame.draw.line(screen, 
							DARK(colour), 
							translate_inv(destination), 
							translate_inv(pos), 
							MEDIUM)
						pygame.draw.circle(screen, DARK(colour, 0.3), 
							(j * CELL_H + CELL_H//2, i * CELL_W + CELL_W//2), 
							min(CELL_H, CELL_W)//5 - BIG)
						pygame.draw.circle(screen, DARK(colour, 0.8), 
							(j * CELL_H + CELL_H//2, i * CELL_W + CELL_W//2), 
							min(CELL_H, CELL_W)//5 - BIG - TINY)
				STATE['position'] = destination

				if target is not None and target.figure is not None and target.figure.colour == target.colour:
					STATE['mode'] = 'validate'
					draw_grid()
					draw_figures()
					update()
		draw_grid()
		draw_figures()
		update()
	sleep(0.1)
