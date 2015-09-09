from traceback import format_exc
from xml.etree import ElementTree
from shutil import copytree

def copy_directory(source, destination):
	try:
		copytree(source, destination)
	except:
		console_error()

def open_file(file, mode):
	try:
		f = open(file, mode)
		return f
	except:
		console_error()
		return None

def open_xml_file(file):
	try:
		return ElementTree.parse(file)
	except:
		console_error()
		return None

def console_error():
	print('')
	print(format_exc())
