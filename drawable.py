import curses

class Drawable:
	'''Base class for things that can appear in a scene'''
	next_color_id = 1

	SHADOW_EXACT = 1
	SHADOW_FILL = 2


	def __init__(self, art, shadow_mode=None):
		self.attrs = 0
		self.color_id = 0
		self.scene = None
		if shadow_mode == None:
			shadow_mode = self.SHADOW_FILL
		self.shadow_mode = shadow_mode

		self.set_art(art)


	def set_color(self, foreground, background=curses.COLOR_BLACK):
		if not curses.has_colors():
			return

		new_color = False
		if self.color_id == 0:
			if foreground != curses.COLOR_WHITE or background != curses.COLOR_BLACK:
				new_color = True

				self.color_id = Drawable.next_color_id
				Drawable.next_color_id += 1

		curses.init_pair(self.color_id, foreground, background)

		if self.scene:
			if new_color:
				self.redraw()
			elif self.scene.auto_refresh:
				self.scene.refresh()


	def set_art(self, art):
		self.height = 0
		self.width = 0
		self.art = []
		self.shadow = None

		at_beginning = True
		art = art.rstrip()
		for line in art.split('\n'):
			line = line.rstrip()
			if at_beginning and line == '':
				continue

			self.height += 1
			if len(line) > self.width:
				self.width = len(line)

			self.art.append(list(line))

		self.redraw()


	def get_shadow(self):
		if self.shadow:
			return self.shadow

		if self.shadow_mode == Drawable.SHADOW_EXACT:
			self.shadow = self.make_exact_shadow()

		if self.shadow_mode == Drawable.SHADOW_FILL:
			self.shadow = self.make_filled_shadow()

		for line in self.shadow:
			line.extend([False] * (self.width - len(line)))

		return self.shadow


	def make_exact_shadow(self):
		self.shadow = []
		for line in self.art:
			shadow_line = ''
			for char in line:
				if char.isspace():
					shadow_line += ' '
				else:
					shadow_line += '-'

			if len(shadow_line) < self.width:
				shadow_line = shadow_line.ljust(self.width)
			self.shadow.append([x=='-' for x in shadow_line])

		return self.shadow


	def make_filled_shadow(self):
		self.shadow = []
		for line in self.art:
			shadow_line = ''
			for char in line:
				if not char.isspace():
					break
				shadow_line += ' '

			shadow_line += ''.ljust(len(line) - len(shadow_line), '-')
			if len(shadow_line) < self.width:
				shadow_line = shadow_line.ljust(self.width)
			self.shadow.append([x=='-' for x in shadow_line])

		return self.shadow


	def redraw(self):
		if self.scene:
			self.scene.request_refresh(self)


	def hide(self):
		if self.scene:
			self.scene.hide(self)


	def get_attrs(self):
		return curses.color_pair(self.color_id) | self.attrs


	def add_attrs(self, attrs):
		self.attrs = self.attrs | attrs


	def set_attrs(self, attrs):
		self.attrs = attrs