from drawable import Drawable
import curses

class Alert(Drawable):
	def __init__(self, msg):
		width = 0
		msg = msg.split('\n')
		height = len(msg) + 2

		for line in msg:
			line = line.strip()
			if len(line) > width:
				width = len(line)

		Drawable.__init__(self, '')

		width += 2
		self.art = [[' '] * width]
		for line in msg:
			line = line.strip()
			diff = width - len(line)
			art = [' '] * (diff // 2)
			for char in line:
				art.append(char)

			diff = width - len(art)
			art.extend([' '] * diff)

			self.art.append(art)

		self.art.append([' '] * width)

		self.shadow = []
		for y in range(0, height):
			self.shadow.append([True] * width)

		self.width = width
		self.height = height

		self.set_attrs(curses.A_DIM)
		self.set_color(curses.COLOR_RED, curses.COLOR_WHITE)

	def show(self, scene):
		center_y = scene.offset_y + scene.win_height // 2
		center_x = scene.offset_x + scene.win_width // 2

		scene.add_object(
			self,
			center_x - self.width // 2,
			center_y - self.height // 2
		)
