# printer.py

from termcolor import colored

def area(area, coord):
	coord = ', '.join(coord) if coord else 'no location'
	print(colored(area, 'red'), colored(coord, 'white'))

def route(info):
	displayInfo = (info["grade"][info["primaryGrade"]]["string"], ", ".join(info["style"]), info["pitches"])
	print(colored('{0[0]:<20}{0[1]:<20}{0[2]!s:<20}'.format(displayInfo), 'cyan'))

def error(action, culprit):
	print(colored("There was an error {}. Culprit: {}".format(action, culprit), 'magenta'))
