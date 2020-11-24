"""

##### x
     
 ▐█▌ 
     
##### n
╺━━━╸
 ▐█▌ 
     
##### e
    ╻
 ▐█▌┃
    ╹
##### s
     
 ▐█▌ 
╺━━━╸
##### w
╻    
┃▐█▌ 
╹    
##### f
╺━━━┓
 ▐█▌┃
    ╹
##### l
    ╻
 ▐█▌┃
╺━━━┛
##### a
╻    
┃▐█▌ 
┗━━━╸
##### c
┏━━━╸
┃▐█▌ 
╹    
##### v
╺━━━╸
 ▐█▌ 
╺━━━╸
##### h
╻   ╻
┃▐█▌┃
╹   ╹
##### W
╺━━━┓
 ▐█▌┃
╺━━━┛
##### N
╻   ╻
┃▐█▌┃
┗━━━┛
##### E
┏━━━╸
┃▐█▌ 
┗━━━╸
##### S
┏━━━┓
┃▐█▌┃
╹   ╹
##### o
┏━━━┓
┃▐█▌┃
┗━━━┛
#####

"""

from random import choice, shuffle
from grid import *
from os import system

system('clear')

walls = {
	'x': [],
	'n': ['north'],
	'e': ['east'],
	's': ['south'],
	'w': ['west'],
	'f': ['north', 'east'],
	'l': ['east', 'south'],
	'a': ['south', 'west'],
	'c': ['north', 'west'],
	'h': ['north', 'south', ],
	'v': ['east', 'west'],
	'N': ['east', 'south', 'west'],
	'E': ['north', 'south', 'west'],
	'S': ['north', 'east', 'west'],
	'W': ['north', 'east', 'south'],
	'o': ['north', 'east', 'south', 'west'],
}

colours = {
	'r': 'red',
	'b': 'blue',
	'g': 'green',
	'y': 'yellow',
	'a': 'all',
	' ': None,
}

symbols = {
	'm': 'moon',
	'p': 'planet',
	's': 'star',
	't': 'triangle',
	'v': 'vortex',
	' ': None,
}


# Quaters a, b, c, d front and back

example = """c n n n n n n n 
w x x x x x x x 
w x x x x x x x 
w x x x x x x x 
w x x x x x x x 
w x x x x x x x 
w x x x x x x s 
w x x x x x e c """

a_f = """c n n f c n n n 
w x x x x x x x 
w x x x x lbw x 
w x s x x n x x 
a x fgw x x x x 
c s x x x x e ar
v cyx x x x x h 
w x x x x x e c """

a_b = """c f c n h n n n 
w x x x fgw x x 
w x x x x x x x 
v arx x x x x x 
w n x x x s x x 
a x x x e cyx x 
c x x lbw x x s 
w x x n x x e c """

b_f = """c f c n h n n n 
w s x e crx x x 
w fgw x x x x x 
w x x x x x lyw 
w x x x x x n x 
a x x x x x x x 
c x e abx x x s 
w x x n x x e c """

b_b = """c f c h n n n n 
w x e cgx x x x 
w x x x x x x x 
w x x x x x lyw 
v arx x x x n x 
w n x x s x x x 
a x x x fbw x s 
c x x x x x e c """

c_f = """c n n f c n n n 
w x x x x lgw x 
v arx x x n x x 
a n x x x x s x 
c x x x x e cyx 
w x s x x x x x 
w x fbw x x x s 
w x x x x x e c """

c_b = """c n n n n f c n 
w x x s x x x x 
w x e cyx x x x 
a x s x e abx x 
c x frw x n x x 
w x x x lgw x x 
w x x x n x x s 
w x x x x x e c """

d_f = """c n n n f c n n 
w x lrw x x x x 
w x n x x x x x 
v agx x x x s x 
a n x x x e cyx 
c x x x x s x x 
w x x x x fbw s 
w x x l w x e c """

d_b = """c n f c n n n n 
w x x x e abx x 
w x x x x n x l 
a x x x x x x n 
c x x lrw x s x 
w s x n x e cgx 
w fyw x x x x s 
w x x x x x e c """


def to_quater(quater_string):
	return Quater([[Square(walls[line[i]], colour=colours[line[i+1]]) for i in range(0, len(line), 2)] for line in quater_string.split('\n')])


A_f = to_quater(a_f)
A_b = to_quater(a_b)
B_f = to_quater(b_f)
B_b = to_quater(b_b)
C_f = to_quater(c_f)
C_b = to_quater(c_b)
D_f = to_quater(d_f)
D_b = to_quater(d_b)


#G = Grid([D_b.rotate(0), B_b.rotate(1), C_b.rotate(3), A_b.rotate(2)])
G = Grid([A_f.rotate(0), B_f.rotate(1), D_f.rotate(3), C_f.rotate(2)])
#print(G)

def random_grid(verbose = False):
	quaters = [[A_f, A_b], [B_f, B_b], [C_f, C_b], [D_f, D_b]]
	shuffle(quaters)
	G = Grid([choice(qs).rotate(i) for qs, i in zip(quaters, (0, 1, 3, 2))])
	if verbose:
		print(G)
	return G
