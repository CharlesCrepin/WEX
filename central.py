from os import linesep
from files import open_xml_file, open_file

APP_VERSION = '1.0.0'
ADMIN = 'wem_administrator'
ADMIN_PASSWORD = 'rbqrld'
WEBUSER = 'Anonymous'
APP_CONFIG_FILE = 'app_config.xml'
CONFIG_FILE = 'config.dat'
TEMP_CONFIG_FILE = 'config.tmp'
ALLOWED_FILENAMES_FILE = 'allowed_fw_filenames.dat'
TIME_ZONES_FILE	= 'time_zones.xml'
CR = '\n'

def read_app_config_value(parameter):
	tree = open_xml_file(APP_CONFIG_FILE)
	if tree is not None:
		for child in tree.getroot():
			if child.tag == parameter:
				return child.attrib.get('value')
	return ''

def read_config_value(parameter):
	output = ''
	f = open_file(CONFIG_FILE, 'r')
	if f is not None:
		for line in f:
			line = line.rstrip(linesep)
			if line[:len(parameter)+1] == parameter + '=':
				output = line[len(parameter)+1:len(line)]
				break
		f.close()
	return output
