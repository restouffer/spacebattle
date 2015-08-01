#! /usr/bin/env python

import subprocess, curses, sys, os, time
from ship import Ship
from scene import Scene
from alert import Alert
from game import Game
from docopt import docopt
USAGE_MSG = """Usage: %s PROG1 PROG2

Pit two programs against each other in an epic space battle. The first program
is the attacker and the second will defend.

Arguments:
	PROG1    The path to the attacking executable
	PROG2    The path to the defending executable

Options:
  -h --help
""" % sys.argv[0]

sys.stdout = sys.stderr

boss_ship = '''
                 <=====]
           _____    )  ]
      _.--`   \\\\'-,/__/
 ___//_@/.-----,||~\_]
<|||]~ BOB RULZ || (_]
    \\\\   '-----`||_/_]
   -)=='--,___//.-`\\  \\
                    )  ]
                 <=====]
'''

player_ship = '''
__
| \\
=[_|K)--._____
=[+--,-------'
 [|_/""
'''

def is_valid_target(target):
	return target in (1, 2, 3, 4, 5)

def get_target(program):
	target = ''
	while True:
		character = program.stdout.read(1).decode()
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

def show_health(win, health, id):
	attr = curses.color_pair(id)
	if health == 1:
		attr = attr | curses.A_BLINK
		curses.init_pair(id, curses.COLOR_WHITE, curses.COLOR_RED)
	elif health <= 3:
		curses.init_pair(id, curses.COLOR_WHITE, curses.COLOR_YELLOW)
	else:
		curses.init_pair(id, curses.COLOR_WHITE, curses.COLOR_GREEN)

	win.addstr(2, 0, ''.ljust(win.getmaxyx()[1] - 1), curses.color_pair(0))
	win.addstr(2, 0, ''.ljust(health), curses.color_pair(id))

	win.refresh()

def get_dimensions(art):
	height = 0;
	width = 0;
	for line in art.strip().split('\n'):
		height += 1
		if len(line) > width:
			width = len(line)

	return (height, width)

def draw_object(win, obj, x, y, attr=None):
	printed = False
	first_col = x
	for line in obj.split('\n'):
		for char in line:
			if not char.isspace():
				try:
					win.addch(y, x, char, attr)
					printed = True
				except curses.error:
					print('Could not write %s at %d,%d' % (char, x, y), file=sys.stderr)
			x += 1
		if printed:
			y += 1
		x = first_col

def show_attack(win, ship, blocked=False):
	y, x = win.getmaxyx()


def space_battle(screen, prog1, prog2):
	boss = Ship('Bob Empire', boss_ship)
	boss.set_program(prog1)

	player = Ship('Kryptonians', player_ship)
	player.set_program(prog2)

	game = Game(player, boss)
	game.intro()
	game.play()
	game.outro()
	time.sleep(0.5)


def test_drawing():
	scene = Scene(200, 200)
	scene.display(0, 0)
	alert = Alert('Hello')
	alert.show(scene)
	time.sleep(1)


if __name__ == "__main__":
	inputs = docopt(USAGE_MSG)

	try:
		screen = curses.initscr()
		screen.clear()
		curses.noecho()
		try:
			curses.curs_set(0)
		except curses.error:
			pass
		curses.start_color()
		#test_drawing()
		space_battle(screen, inputs['PROG1'], inputs['PROG2'])
	finally:
		curses.echo()
		curses.endwin()
