from drawable import Drawable
import random, curses

class Thruster(Drawable):
	def __init__(self, ship):
		self.direction = 1
		self.step = 1
		self.stages = [
			'. ',
			'` ',
			': ',
			':.',
			':`',
			'::'
		]
		Drawable.__init__(self, self.get_art())
		self.width = 3
		self.set_color(curses.COLOR_YELLOW)
		self.set_attrs(curses.A_BOLD)


	def switch_direction(self):
		self.direction *= -1


	def update(self):
		if self.step == 0:
			self.step = 1
		elif self.step == len(self.stages) - 1:
			self.step = len(self.stages) - 2
		else:
			self.step += random.choice([-1, 1])

		self.set_art(self.get_art())
		self.width = 3

		self.redraw()


	def get_art(self):
		art = self.stages[self.step]

		return art[::self.direction]