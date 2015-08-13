from drawable import Drawable

class Outline(Drawable):
	def __init__(self, object):
		self.width = object.width + 2
		self.height = object.height + 2
		self.color_id = 0
		self.attrs = 0

		self.art = [[' '] * self.width] * self.height
		self.shadow = self.get_outline(object)


	def get_outline(self, object):
		obj_width = object.width
		object = object.get_shadow()

		shadow = []
		for y in range(0, self.height):
			shadow.append([False] * self.width)
			for x in range(0, self.width):
				if self.is_shadow(x, y, object):
					continue
				if self.touching_shadow(x, y, object):
					shadow[y][x] = True

		return shadow


	def is_border(self, x, y):
		if x <= 0 or y <= 0:
			return True
		if x >= self.width - 1 or y >= self.height - 1:
			return True

		return False


	def is_shadow(self, x, y, shadow):
		if self.is_border(x, y):
			return False

		return shadow[y-1][x-1]


	def touching_shadow(self, x, y, shadow):
		if self.is_shadow(x-1, y-1, shadow):
			return True
		if self.is_shadow(x, y-1, shadow):
			return True
		if self.is_shadow(x+1, y-1, shadow):
			return True
		if self.is_shadow(x-1, y, shadow):
			return True
		if self.is_shadow(x+1, y, shadow):
			return True
		if self.is_shadow(x-1, y+1, shadow):
			return True
		if self.is_shadow(x, y+1, shadow):
			return True
		return self.is_shadow(x+1, y+1, shadow)
