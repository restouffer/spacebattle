from drawable import Drawable
import curses

class HealthBar(Drawable):
	def __init__(self, health):
		Drawable.__init__(self, '.'.rjust(health + 1))
		self.health = health
		self.width = health

		self.set_color(curses.COLOR_WHITE, curses.COLOR_GREEN)

	def decrease(self):
		self.health -= 1
		self.shadow = None

		if self.health <= 3:
			self.set_color(curses.COLOR_WHITE, curses.COLOR_RED)
			if self.health == 1:
				self.set_art('!'.ljust(self.width) + '.')
				self.add_attrs(curses.A_BLINK | curses.A_BOLD)

		elif self.health <= 7:
			self.set_color(curses.COLOR_WHITE, curses.COLOR_YELLOW)

		self.redraw()


	def get_shadow(self):
		shadow = ([True] * self.health)
		shadow.extend([False] * (self.width - self.health))
		return [shadow]


	def is_empty(self):
		return self.health <= 0