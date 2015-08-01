from copy import deepcopy
from damagemap import DamageMap
import sys

class SceneObject:
	def __init__(self, scene, object):
		self.drawable = object
		self.visible = False
		self.x1 = None
		self.x2 = None
		self.y1 = None
		self.y2 = None
		self.damage_map = None

		object.scene = scene


	def show_at(self, x, y):
		self.x1 = x
		self.x2 = x + self.drawable.width - 1
		self.y1 = y
		self.y2 = y + self.drawable.height - 1
		self.visible = True


	def generate_damage_map(self):
		new_damage_map = DamageMap(self)
		old_damage_map = self.damage_map
		self.damage_map = deepcopy(new_damage_map)

		if old_damage_map:
			new_damage_map.merge_map(old_damage_map)

		return new_damage_map


	def occult(self, damage_map):
		if not self.intersects(damage_map):
			return damage_map

		damage_map.subtract(self.x1, self.y1, self.drawable.shadow)
		return damage_map


	def draw_according_to(self, win, damage_map):
		if not self.intersects(damage_map):
			return damage_map

		blank = True
		shadow = self.drawable.get_shadow()
		shadow_offset_y = damage_map.y1 - self.y1
		shadow_offset_x = damage_map.x1 - self.x1
		y = shadow_offset_y
		for line in damage_map:
			if any(line):
				blank = False
			if y < 0:
				y += 1
				continue
			x = shadow_offset_x
			for char in line:
				if x < 0:
					x += 1
					continue
				if char:
					try:
						if not shadow[y][x]:
							x += 1
							continue
					except IndexError:
						x += 1
						continue

					win.write(
						x + self.x1,
						y + self.y1,
						self.drawable.art[y][x],
						self.drawable.get_attrs()
					)
					damage_map.clear_damage(
						x - shadow_offset_x,
						y - shadow_offset_y
					)

				x += 1
			y += 1

		damage_map.blank = blank

		return damage_map



	def intersects(self, damage_map):
		if self.visible == False:
			return False

		if self.x2 < damage_map.x1:
			return False
		if self.x1 > damage_map.x2:
			return False
		if self.y2 < damage_map.y1:
			return False
		if self.y1 > damage_map.y2:
			return False

		return True