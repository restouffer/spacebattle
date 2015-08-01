from copy import deepcopy

class DamageMap:
	def __init__(self, object):
		self.x1 = object.x1
		self.x2 = object.x2
		self.y1 = object.y1
		self.y2 = object.y2
		self.blank = False

		self.map = deepcopy(object.drawable.get_shadow())


	def merge_map(self, other):
		x1 = min(self.x1, other.x1)
		x2 = max(self.x2, other.x2)
		y1 = min(self.y1, other.y1)
		y2 = max(self.y2, other.y2)

		if x1 != self.x1 or x2 != self.x2 or y1 != self.y1 or y2 != self.y2:
			new_map = self.blank_map(x2 - x1 + 1, y2 - y1 + 1)
			self.map = self.write_onto(
				new_map,
				self.map,
				self.x1 - x1,
				self.y1 - y1
			)

		self.map = self.write_onto(
			self.map,
			other.map,
			other.x1 - x1,
			other.y1 - y1
		)

		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2


	def __iter__(self):
		return iter(self.map)


	def write_onto(self, target, object, offset_x, offset_y):
		y = offset_y
		for line in object:
			x = offset_x
			for char in line:
				if char:
					target[y][x] = True

				x += 1
			y += 1

		return target


	def blank_map(self, width, height):
		new_map = []
		for y in range(0, height):
			new_map.append([False] * width)

		return new_map


	def subtract(self, offset_x, offset_y, shadow):
		min_y = max(0, self.y1 - offset_y)
		max_y = min(len(shadow) - 1, self.y2 - self.y1 - 1)
		shadow = shadow[min_y:max_y]

		min_x = max(0, self.x1 - offset_x)
		max_x = self.x2 - self.x1 - 1

		y = max(0, offset_y - self.y1)
		offset_x = max(0, offset_x - self.x1)

		for line in shadow:
			x = offset_x
			line = line[min_x:max_x]
			for char in line:
				if char:
					self.clear_damage(x, y)
				x += 1
			y += 1


	def is_damaged(self, x, y):
		return self.map[y][x]


	def clear_damage(self, x, y):
		self.map[y][x] = False
