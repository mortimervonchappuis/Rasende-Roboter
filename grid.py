from colorama import Fore


class Grid:
	def __init__(self, quaters):
		self.quaters = quaters
		self.squares = [left + right for left, right in zip(quaters[0], quaters[1])] + [left + right for left, right in zip(quaters[2], quaters[3])]
		self.a = quaters[0]
		self.b = quaters[1]
		self.c = quaters[3]
		self.d = quaters[2]
		for i, line in enumerate(self.squares):
			for j, square in enumerate(line):
				square.pos = (i, j)

	def __getitem__(self, idx):
		i, j = idx
		try:
			return self.squares[i][j]
		except:
			print(i, j)
			exit()

	def search(self, pos):
		i, j = pos
		result = {'north': None, 'east': None, 'south': None, 'west': None}

		# North
		if not self[i, j].north:
			d = -1
			while self[i + d + 1, j].leave('north') and self[i + d, j].enter('north'):
				d -= 1
			result['north'] = (i + d + 1, j)

		# South
		if not self[i, j].south:
			d = 1
			while self[i + d - 1, j].leave('south') and self[i + d, j].enter('south'):
				d += 1
			result['south'] =  (i + d - 1, j)

		# West
		if not self[i, j].west:
			d = -1
			while self[i, j + d + 1].leave('west') and self[i, j + d].enter('west'):
				d -= 1
			result['west'] =  (i, j + d + 1)
		
		# East
		if not self[i, j].east:
			d = 1
			while self[i, j + d - 1].leave('east') and self[i, j + d].enter('east'):
				d += 1
			result['east'] =  (i, j + d - 1)

		return result
	


	def rotate(self, n):
		if (n := n % 4) == 0:
			return self
		else:
			return Grid([
				self.quaters[2].rotate(1), 
				self.quaters[0].rotate(1), 
				self.quaters[3].rotate(1), 
				self.quaters[1].rotate(1)]).rotate(n - 1)

	def __str__(self):
		return Fore.WHITE + ('\n'.join(left + right for left, right in zip(
			str(self.quaters[0]).split('\n'), 
			str(self.quaters[1]).split('\n'))) + '\n' + '\n'.join(left + right for left, right in zip(
			str(self.quaters[2]).split('\n'), 
			str(self.quaters[3]).split('\n')))).replace('R', Fore.RED + 'R' + Fore.WHITE).replace('B', Fore.BLUE + 'B' + Fore.WHITE).replace('Y', Fore.YELLOW + 'Y' + Fore.WHITE).replace('G', Fore.GREEN + 'G' + Fore.WHITE)


class Quater:
	def __init__(self, squares):
		self.squares = squares
		for line in squares:
			for square in line:
				if square.colour == 'red':
					self.red = square
				elif square.colour == 'yellow':
					self.yellow = square
				elif square.colour == 'green':
					self.green = square
				elif square.colour == 'blue':
					self.blue = square
		self.colours = [self.red, self.yellow, self.green, self.blue]

	def __iter__(self):
		for line in self.squares:
			yield line

	def rotate(self, n):
		if (n := n % 4) == 0:
			return self
		else:
			return Quater([[self.squares[j][i].rotate(1) for j in range(7, -1, -1)] for i in range(8)]).rotate(n - 1)

	def __str__(self):
		return '\n'.join('\n'.join(''.join(str(square)[6*i: 6*i+5] for square in line) for i in range(3)) for line in self.squares)


class Square:
	"""Documentation"""
	def __init__(self, walls, figure=None, colour=' ', pos=None):
		self.walls 	= [item for item in walls]
		self.north 	= 'north' 	in walls
		self.west 	= 'west' 	in walls
		self.south 	= 'south' 	in walls
		self.east 	= 'east' 	in walls
		self.figure = figure
		self.colour = colour
		self.pos = pos


	def enter(self, direction):
		if self.figure is not None:
			return False
		if direction == 'north':
			return not self.south
		elif direction == 'east':
			return not self.west
		elif direction == 'south':
			return not self.north
		elif direction == 'west':
			return not self.east
		else:
			raise Exception(direction)

	def leave(self, direction):
		if direction == 'north':
			return not self.north
		elif direction == 'east':
			return not self.east
		elif direction == 'south':
			return not self.south
		elif direction == 'west':
			return not self.west
		else:
			raise Exception(direction)

	def rotate(self, n=0):

		def clockwise(wall):
			clock = ['north', 'east', 'south', 'west']
			return clock[(clock.index(wall) + 1) % 4]

		if (n := n % 4) == 0:
			return Square(self.walls, self.figure, self.colour)
		else:
			return Square([clockwise(wall) for wall in self.walls], self.figure, self.colour).rotate(n - 1)

	def __str__(self):
		if self.north and self.west:
			A = '┏'
		elif self.north and not self.west:
			A = '━' # '╺'
		elif not self.north and self.west:
			A = '┃' # '╻'
		elif not self.north and not self.west:
			A = ' '

		if self.north:
			B = '━━━'
		else:
			B = '   '

		if self.north and self.east:
			C = '┓'
		elif self.north and not self.east:
			C = '━' # '╸'
		elif not self.north and self.east:
			C = '┃' # '╻'
		elif not self.north and not self.east:
			C = ' '

		if self.west:
			D = '┃'
		else:
			D = ' '

		E = f"{self.colour[0].upper() if self.colour is not None else ' '} {self.figure.colour[0] if self.figure is not None else ' '}" # ▐█▌

		if self.east:
			F = '┃'
		else:
			F = ' '

		if self.south and self.west:
			G = '┗'
		elif self.south and not self.west:
			G = '━' # '╺'
		elif not self.south and self.west:
			G = '┃' # '╹'
		elif not self.south and not self.west:
			G = ' '

		if self.south:
			H = '━━━'
		else:
			H = '   '

		if self.south and self.east:
			I = '┛'
		elif self.south and not self.east:
			I = '━' # '╸'
		elif not self.south and self.east:
			I = '┃' # '╹'
		elif not self.south and not self.east:
			I = ' '

		return f"""{A}{B}{C}
{D}{E}{F}
{G}{H}{I}"""


class Figure:
	def __init__(self, colour, position, grid):
		self.colour = colour
		self.position = self.i, self.j = position
		self.grid = grid
		self.square = grid[position]
		self.square.figure = self


	def actions(self):
		if not self.square.north:
			i = 0
			while not (square := grid[self.i + i, self.j]).south and square.figure is not None:
				i += 1
			if i:
				yield self.i + i, self.j
		if not self.square.east:
			j = 0
			while not (square := grid[self.i, self.j + j]).west and square.figure is not None:
				j += 1
			if i:
				yield self.i, self.j + j
		if not self.square.south:
			i = 0
			while not (square := grid[self.i + i, self.j]).north and square.figure is not None:
				i -= 1
			if i:
				yield self.i + i, self.j
		if not self.square.west:
			j = 0
			while not (square := grid[self.i, self.j + j]).east and square.figure is not None:
				j -= 1
			if i:
				yield self.i, self.j + j
		




if __name__ == '__main__':
	print('#####')
	print(Square([], ''))
	for square in [Square(['north'], ''), Square(['north', 'east'], ''), Square(['north', 'south'], ''), Square(['north', 'east', 'south'], '')]:
		for i in range(4):
			print('#####')
			print(square.rotate(i))
	print('#####')
	print(Square(['north', 'east', 'south', 'west'], ''))
	print('#####')