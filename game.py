from scene import Scene
from drawable import Drawable
from alert import Alert
from outline import Outline
from healthbar import HealthBar
from thruster import Thruster
from laser import Laser
from explosion import Explosion
import curses, time, random

class Game:
	max_health = 10
	ship_space = 15
	screens = 3

	def __init__(self, player, boss):
		self.p1 = player
		self.p2 = boss

		p1_status = Scene(max(len(self.p1.name), self.max_health) + 1, 3)
		p1_status.modify_background(self.p1.name)
		p2_status = Scene(max(len(self.p2.name), self.max_health) + 1, 3)
		p2_status.modify_background(self.p2.name)

		self.p1.health = HealthBar(self.max_health)
		p1_status.add_object(self.p1.health, 0, 2)
		self.p1.status_win = p1_status
		self.p1.thruster = Thruster(self.p1)
		self.p1.thruster.switch_direction()
		self.p1.thruster.set_color(curses.COLOR_CYAN)

		self.p2.health = HealthBar(self.max_health)
		p2_status.add_object(self.p2.health, 0, 2)
		self.p2.status_win = p2_status

		width, height = Scene.max_view(0, 7)
		width *= self.screens
		self.main_win = Scene(width, height)
		self.main_win.modify_background(self.generate_starfield(width, height))

	def intro(self):
		self.midpoint_x = round(
			self.main_win.width * (self.screens - 0.5)/self.screens
		)
		midpoint_y = self.main_win.height // 2
		outline = Outline(self.p2)
		self.main_win.add_object(
			outline,
			self.midpoint_x + self.ship_space - 1,
			midpoint_y - self.p2.height // 2 - 1
		)
		outline = Outline(self.p1)
		self.main_win.add_object(
			outline,
			self.midpoint_x - self.ship_space - self.p1.width,
			midpoint_y - self.p1.height // 2 - 1
		)
		self.main_win.add_object(
			self.p2,
			self.midpoint_x + self.ship_space,
			midpoint_y - self.p2.height // 2
		)
		self.main_win.add_object(
			self.p1,
			4,
			midpoint_y - self.p1.height // 2
		)
		self.main_win.add_object(
			self.p1.thruster,
			2,
			midpoint_y + 1
		)
		self.main_win.display(0, 7)

		self.main_win.auto_refresh = False
		position = self.p1.scene.objects[self.p1.stacking_order]
		distance = self.midpoint_x - self.ship_space - position.x2
		speed = 0.04
		while distance > 0:
			self.main_win.move_relative(self.p1, x=1)
			self.main_win.move_relative(self.p1.thruster, x=1)
			self.p1.thruster.update()
			self.main_win.pan(x=1)
			self.main_win.refresh()
			time.sleep(speed)
			if distance == 40:
				self.main_win.hide(self.p1.thruster)
			if distance < 40:
				speed += 0.005
			distance -= 1

		msg = Alert('!!! WARNING !!!\nENEMY WEAPONS LOCKED')
		msg.show(self.main_win)
		self.main_win.refresh()
		time.sleep(3)
		msg.hide()
		self.main_win.refresh()


	def play(self):
		self.p1.status_win.display(
			curses.COLS // 2 - self.ship_space - self.max_health,
			2
		)
		self.p2.status_win.display(
			curses.COLS // 2 + self.ship_space,
			2
		)

		if self.p1.scene.objects[self.p1.stacking_order].x2 != self.midpoint_x - self.ship_space:
			self.main_win.move_to(self.p1, x=self.midpoint_x - self.ship_space - self.p1.width)
			self.main_win.pan(x=self.main_win.width - self.main_win.win_width)

		laser = Laser(self.p1, self.p2, self.main_win.height // 2)
		self.main_win.add_object(laser, laser.x1, laser.y)

		shield1 = Drawable(')')
		shield1.set_color(curses.COLOR_CYAN)
		shield1.set_attrs(curses.A_BOLD)
		self.main_win.add_object(shield1, laser.x1, laser.y)
		self.main_win.hide(shield1)
		shield2 = Drawable('(')
		shield2.set_color(curses.COLOR_CYAN)
		shield2.set_attrs(curses.A_BOLD)
		self.main_win.add_object(shield2, laser.x2, laser.y)
		self.main_win.hide(shield2)

		self.main_win.refresh()
		self.main_win.auto_refresh = True
		step = 0
		while not self.p1.health.is_empty() and not self.p2.health.is_empty():
			time.sleep(0.5)
			target1 = self.p1.get_target()
			target2 = self.p2.get_target()

			target = None
			successful = True
			if step < 5:
				target = self.p1
				if not self.is_valid_target(target1):
					target1 = 0
				elif not self.is_valid_target(target2) or target1 == target2:
					successful = False
			else:
				target = self.p2
				if not self.is_valid_target(target2):
					target2 = 0
				elif not self.is_valid_target(target1) or target1 == target2:
					successful = False

			self.p1.show_target(target2)
			self.p2.show_target(target1)

			direction = 1

			if target is self.p1:
				direction = -1
			self.main_win.show(laser)
			laser.start(direction)
			time.sleep(0.01)
			while laser.advance():
				time.sleep(0.02)

			if not successful:
				if direction > 0:
					self.main_win.show(shield2)
					time.sleep(0.5)
					self.main_win.hide(shield2)
				else:
					self.main_win.show(shield1)
					time.sleep(0.5)
					self.main_win.hide(shield1)

			self.main_win.hide(laser)

			if successful:
				target.health.decrease()
				target.set_color(curses.COLOR_RED)
				if target.health.is_empty():
					continue
				time.sleep(0.2)
				target.set_color(curses.COLOR_WHITE)

			step = (step + 1) % 10

		explosion = Explosion(target)
		explosion.set_color(curses.COLOR_YELLOW)
		explosion.set_attrs(curses.A_BOLD)
		self.main_win.add_object(explosion, explosion.x, explosion.y)
		explosion.explode()

		self.winner = self.p2
		if target is self.p2:
			self.winner = self.p1


	def outro(self):
		if self.winner is self.p1:
			self.win_animation()
		else:
			self.lose_animation()


	def win_animation(self):
		ship_position = self.main_win.objects[self.p1.stacking_order].x1
		distance = self.main_win.max_x - ship_position + 2

		self.main_win.auto_refresh = False
		self.main_win.show(self.p1.thruster)
		self.p1.thruster.step = 1
		speed = 0.25
		while distance >= 0:
			self.main_win.move_relative(self.p1, x=1)
			self.p1.thruster.update()
			self.main_win.move_relative(self.p1.thruster, x=1)
			self.main_win.refresh()
			time.sleep(speed)
			speed -= 0.005
			if speed < 0.04:
				speed = 0.04

			distance -= 1

		self.main_win.auto_refresh = True
		msg = Alert('!!! CONGRATULATIONS !!!\nTHE GUMMIES HAVE BEEN SAVED')
		msg.show(self.main_win)
		time.sleep(3)
		msg.hide()


	def lose_animation(self):
		msg = Alert('YOUR SHIP HAS BEEN DESTROYED')
		msg.show(self.main_win)
		time.sleep(5)
		msg.hide()


	def generate_starfield(self, width, height):
		starfield = ''
		stars = ['.', '*', '`', '.']
		for y in range(0, height):
			for x in range(0, width):
				if random.randint(0, 30) == 0:
					starfield += random.choice(stars)
				else:
					starfield += ' '

			starfield += '\n'

		return starfield.rstrip()


	@staticmethod
	def is_valid_target(target):
		return target in (1, 2, 3, 4, 5)
