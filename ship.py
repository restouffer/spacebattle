from drawable import Drawable
from threading import Timer
import curses, subprocess, os, random

class Ship(Drawable):
	'''All of the relevant information about a space battle ship'''
	delay = 0

	def __init__(self, name, art):
		Drawable.__init__(self, art)
		self.add_attrs(curses.A_BOLD)

		self.name = name
		self.program = None


	def set_program(self, path):
		t = Timer(Ship.delay, self._set_program, args=[path])
		t.start()
		Ship.delay += 1


	def _set_program(self, path):
		self.program = subprocess.Popen(
			'%s/%s' % (os.getcwd(), path),
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE
		)


	def get_target(self):
		target = ''
		while True:
			character = self.program.stdout.read(1).decode()
			if character == '':
				break
			elif character == '\n':
				break
			else:
				target += character

		try:
			return int(target.strip())
		except ValueError:
			return 0


	def show_target(self, target):
		self.program.poll()
		if self.program.returncode is None:
			self.program.stdin.write(("%d\n" % target).encode())
			self.program.stdin.flush()


	def shutdown_program(self):
		self.program.poll()
		if self.program.returncode is None:
			self.program.terminate()

