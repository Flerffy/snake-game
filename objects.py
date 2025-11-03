import random
import pygame
from constants import *


class Point:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return isinstance(other, Point) and self.x == other.x and self.y == other.y


class Snake:
	def __init__(self, length=INITIAL_SNAKE_LENGTH):
		# start in the center of the play area, aligned to the grid
		cols = GAME_WIDTH // CELL_SIZE
		rows = GAME_HEIGHT // CELL_SIZE
		center_col = cols // 2
		center_row = rows // 2
		start_x = BORDER_SIZE + center_col * CELL_SIZE
		start_y = BORDER_SIZE + center_row * CELL_SIZE

		self.segments = [Point(start_x - i * CELL_SIZE, start_y) for i in range(length)]
		# initial movement to the right
		self.direction = DIRECTIONS['RIGHT']
		self.grow_flag = False

	@property
	def head(self):
		return self.segments[0]

	def change_direction(self, new_dir):
		# prevent reversing into itself
		if (new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]):
			return
		self.direction = new_dir

	def move(self):
		new_x = self.head.x + self.direction[0] * CELL_SIZE
		new_y = self.head.y + self.direction[1] * CELL_SIZE
		new_head = Point(new_x, new_y)
		self.segments.insert(0, new_head)
		if self.grow_flag:
			self.grow_flag = False
		else:
			self.segments.pop()

	def grow(self):
		self.grow_flag = True

	def check_self_collision(self):
		head = self.head
		return any(seg.x == head.x and seg.y == head.y for seg in self.segments[1:])


class Food:
	def __init__(self):
		self.position = None
		self.respawn([])

	def respawn(self, occupied_segments):
		cols = GAME_WIDTH // CELL_SIZE
		rows = GAME_HEIGHT // CELL_SIZE
		max_attempts = cols * rows
		attempts = 0
		while attempts < max_attempts:
			c = random.randrange(cols)
			r = random.randrange(rows)
			x = BORDER_SIZE + c * CELL_SIZE
			y = BORDER_SIZE + r * CELL_SIZE
			p = Point(x, y)
			if not any(p == s for s in occupied_segments):
				self.position = p
				return
			attempts += 1
		# fallback: place at center
		self.position = Point(BORDER_SIZE + (cols // 2) * CELL_SIZE, BORDER_SIZE + (rows // 2) * CELL_SIZE)