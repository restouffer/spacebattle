from drawable import Drawable
import random, time

class Explosion(Drawable):
	def __init__(self, ship):
		self.ship = ship
		view = ship.scene.objects[ship.stacking_order]
		self.x = view.x1
		self.y = view.y1

		Drawable.__init__(self, '', Drawable.SHADOW_EXACT)

		self.height = max(ship.height, 5)
		self.width = max(ship.width, 5)

		self.clear_art()

		self.y_offset = 0
		if ship.height < 5:
			self.y_offset = (5 - ship.height) // 2
			self.y -= self.y_offset

		self.x_offset = 0
		if ship.width < 5:
			self.x_offset = (5 - ship.width) // 2
			self.x -= self.x_offset


	def clear_art(self):
		art = []
		for y in range(0, self.height):
			art.append([' '] * self.width)

		self.art = art


	def explode(self):
		shadow = self.ship.get_shadow()
		self.get_shadow()

		for i in range(0, 4):
			for y in range(0, self.height):
				for x in range(0, self.width):
					if shadow[self.y_offset + y][self.x_offset + x]:
						if random.randint(0, 3) == 0:
							self.art[y][x] = '*'
							self.shadow[y][x] = True

			self.redraw()
			time.sleep(0.2)
			self.clear_art()

		self.scene.hide(self.ship)

		center_x = self.width // 2
		center_y = self.height // 2

		self.shadow = None
		self.art[center_y][center_x] = 'o'
		self.art[center_y + 2][center_x] = '|'
		self.art[center_y + 1][center_x] = '|'
		self.art[center_y - 1][center_x] = '|'
		self.art[center_y - 2][center_x] = '|'
		self.art[center_y][center_x - 2] = '-'
		self.art[center_y][center_x - 1] = '-'
		self.art[center_y][center_x + 1] = '-'
		self.art[center_y][center_x + 2] = '-'
		self.art[center_y + 1][center_x + 1] = '\\'
		self.art[center_y - 1][center_x - 1] = '\\'
		self.art[center_y + 1][center_x - 1] = '/'
		self.art[center_y - 1][center_x + 1] = '/'

		self.redraw()
		time.sleep(0.2)

		self.clear_art()
		self.art[center_y][center_x] = 'o'
		self.art[center_y + 1][center_x] = '|'
		self.art[center_y - 1][center_x] = '|'
		self.art[center_y][center_x - 1] = '-'
		self.art[center_y][center_x + 1] = '-'
		self.art[center_y + 1][center_x + 1] = '\\'
		self.art[center_y - 1][center_x - 1] = '\\'
		self.art[center_y + 1][center_x - 1] = '/'
		self.art[center_y - 1][center_x + 1] = '/'

		self.redraw()
		time.sleep(0.1)

		self.clear_art()
		self.art[center_y][center_x] = 'o'

		self.redraw()
		time.sleep(0.1)

		self.clear_art()
		self.art[center_y][center_x] = '.'

		self.redraw()
		time.sleep(0.2)

		self.scene.hide(self)




