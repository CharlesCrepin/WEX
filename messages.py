from os import linesep
from traceback import format_exc

MESSAGES = ''

def clear_messages():
	global MESSAGES
	MESSAGES = ''

def add_message(str):
	global MESSAGES
	MESSAGES += str.rstrip(linesep) + '<br/>'

def console_error():
	print('')
	print(format_exc())
