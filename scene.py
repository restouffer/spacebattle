from sceneobject import SceneObject
import curses

class Scene:
	def __init__(self, width, height):
		self.win = curses.newpad(height, width)
		self.width = width
		self.height = height
		self.max_x = width - 1
		self.max_y = height - 1
		self.generate_background()
		self.auto_refresh = True
		self.visible = False
		self.objects = []


	def display(self, x, y, width=None, height=None, offset_x=0, offset_y=0):
		if height == None:
			height = self.height - offset_y

		if height > curses.LINES - y:
			height = curses.LINES - y

		if width == None:
			width = self.width - offset_x

		if width > curses.COLS - x:
			width = curses.COLS - x


		self.win_height = height
		self.win_width = width
		self.position_y = y
		self.position_x = x
		self.offset_y = offset_y
		self.offset_x = offset_x

		if len(self.objects) == 0:
			self.background_fill()

		self.visible = True
		self.refresh()


	def refresh(self):
		if not self.visible:
			return

		self.win.refresh(
			self.offset_y,
			self.offset_x,
			self.position_y,
			self.position_x,
			self.position_y + self.win_height - 1,
			self.position_x + self.win_width - 1
		)
		self.win.move(self.max_y, self.max_x)


	def pan(self, x=0, y=0):
		self.offset_y += y
		self.offset_x += x

		if self.offset_y < 0:
			self.offset_y = 0
		elif self.offset_y > self.height - self.win_height:
			self.offset_y = self.height - self.win_height

		if self.offset_x < 0:
			self.offset_x = 0
		elif self.offset_x > self.width - self.win_width:
			self.offset_x = self.width - self.win_width

		if self.auto_refresh:
			self.refresh()


	def generate_background(self):
		self.background = []
		for i in range(0, self.height):
			self.background.append([' '] * self.width)


	def add_object(self, object, x, y):
		object.stacking_order = len(self.objects)
		if object.stacking_order == 0:
			self.background_fill()

		self.objects.append(SceneObject(self, object))
		self.objects[-1].show_at(x, y)

		self.request_refresh(object)


	def move_relative(self, object, x=0, y=0):
		self.objects[object.stacking_order].x1 += x
		self.objects[object.stacking_order].x2 += x
		self.objects[object.stacking_order].y1 += y
		self.objects[object.stacking_order].y2 += y

		if self.objects[object.stacking_order].visible == False:
			return

		self.request_refresh(object)


	def move_to(self, object, x=None, y=None):
		view = self.objects[object.stacking_order]
		diff_x = view.x2 - view.x1
		diff_y = view.y2 - view.y1

		if x != None:
			view.x1 = x
			view.x2 = x + diff_x

		if y != None:
			view.y1 = y
			view.y2 = y + diff_y

		if view.visible == False:
			return

		self.request_refresh(object)


	def hide(self, object):
		self.objects[object.stacking_order].visible = False
		self.request_refresh(object)


	def show(self, object):
		self.objects[object.stacking_order].visible = True
		self.request_refresh(object)


	def request_refresh(self, object):
		damage = self.objects[object.stacking_order].generate_damage_map()

		for key in range(object.stacking_order + 1, len(self.objects)):
			damage = self.objects[key].occult(damage)

		for key in range(object.stacking_order, -1, -1):
			damage = self.objects[key].draw_according_to(self, damage)

		self.background_fill(damage)

		if self.auto_refresh:
			self.refresh()


	@staticmethod
	def max_view(x, y):
		return (curses.COLS - x - 1, curses.LINES - y - 1)


	def modify_background(self, content, x=0, y=0):
		if isinstance(content, str):
			content = content.split('\n')

		x_offset = x
		for line in content:
			x = x_offset
			for char in line:
				self.background[y][x] = char
				x += 1
			y += 1


	def write(self, x, y, char, attrs=None):
		if x < 0 or y < 0:
			return

		if x > self.max_x or y > self.max_y:
			return

		if attrs == None:
			attrs = curses.color_pair(0)

		if x == self.max_x and y == self.max_y:
			self.win.insch(y, x, char, attrs)
		else:
			self.win.addch(y, x, char, attrs)


	def background_fill(self, damage_map=None):
		if damage_map == None:
			y = 0
			for line in self.background:
				x = 0
				for char in line:
					self.write(x, y, char)
					x += 1
				y += 1

			return

		if damage_map.blank:
			return

		if damage_map.x1 > self.max_x or damage_map.x2 < 0:
			return
		if damage_map.y1 > self.max_y or damage_map.y2 < 0:
			return

		offset_x = damage_map.x1
		x1 = 0
		if damage_map.x1 < 0:
			x1 = -offset_x
			offset_x = 0
		offset_y = damage_map.y1
		y1 = 0
		if damage_map.y1 < 0:
			y1 = -offset_y
			offet_y = 0
		x2 = damage_map.x2 - damage_map.x1 + 1
		if damage_map.x2 > self.max_x:
			x2 = self.max_x - damage_map.x1 + 1
		y2 = damage_map.y2 - damage_map.y1 + 1
		if damage_map.y2 > self.max_y:
			y2 = self.max_y - damage_map.y1 + 1

		damage_map = damage_map.map[y1:y2]
		y = offset_y
		for line in damage_map:
			x = offset_x
			line = line[x1:x2]
			for char in line:
				if char:
					self.write(x, y, self.background[y][x])
				x += 1
				if x > self.max_x:
					break
			y += 1
			if y > self.max_y:
				break

