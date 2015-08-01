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
				in_shadow = self.over_shadow(x, y)
				if in_shadow:
					if object[y-1][x-1]:
						continue
					if x >= 2:
						if object[y-1][x-2]:
							shadow[y][x] = True
					if x < self.width - 2:
						if object[y-1][x]:
							shadow[y][x] = True
				if y >= 2:
					if x >= 2:
						if object[y-2][x-2]:
							shadow[y][x] = True
					if x < self.width - 2:
						if object[y-2][x]:
							shadow[y][x] = True
					if in_shadow and object[y-2][x-1]:
						shadow[y][x] = True
				if y < self.height - 2:
					if x >= 2:
						if object[y][x-2]:
							shadow[y][x] = True
					if x < self.width - 2:
						if object[y][x]:
							shadow[y][x] = True
					if in_shadow and object[y][x-1]:
						shadow[y][x] = True

		return shadow


	def over_shadow(self, x, y):
		if x < 1 or y < 1:
			return False
		elif x > self.width - 2 or y > self.height - 2:
			return False

		return True