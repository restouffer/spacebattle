from drawable import Drawable
import curses

class Laser(Drawable):
	def __init__(self, target1, target2, position):
		t1_shadow = target1.get_shadow()
		t2_shadow = target2.get_shadow()

		x1 = target1.scene.objects[target1.stacking_order].x2 + 1
		x2 = target2.scene.objects[target2.stacking_order].x1 - 1

		y = target1.scene.objects[target1.stacking_order].y1
		for line in t1_shadow:
			if y == position:
				for x in range(len(line) - 1, 0, -1):
					if not line[x]:
						x1 -= 1
					else:
						break
				break
			y += 1

		y = target2.scene.objects[target2.stacking_order].y1
		for line in t2_shadow:
			if y == position:
				for x in range(0, len(line) - 1):
					if not line[x]:
						x2 += 1
					else:
						break
				break
			y += 1

		Drawable.__init__(self, ''.ljust(x2 - x1 + 1, '-'))
		self.x_position = None
		self.speed = None
		self.x1 = x1
		self.x2 = x2
		self.y = position

		self.set_color(curses.COLOR_RED, curses.COLOR_BLACK)
		self.set_attrs(curses.A_BOLD)

	def start(self, speed=1):
		self.x_position = self.x1
		if speed < 0:
			self.x_position = self.x2

		self.speed = speed
		self.redraw()


	def advance(self):
		self.x_position += self.speed
		self.redraw()

		if self.x_position <= self.x1:
			return False
		if self.x_position >= self.x2:
			return False

		return True

	def get_shadow(self):
		shadow = [False] * (self.x2 - self.x1 + 1)
		if self.x_position:
			shadow[self.x_position - self.x1] = True

		return [shadow]