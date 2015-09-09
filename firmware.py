from os import path, rename, remove, linesep, makedirs
import central as c
import messages as m

ALLOWED_FILENAMES = []
ALLOWED_REVISION_CHARS = ['?', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
NOT_FOUND = '-NotFound-'

def read_allowed_file():
	try:
		del ALLOWED_FILENAMES[:]
		f = open(c.ALLOWED_FILENAMES_FILE, 'r')
		for pattern in f.readlines():
			if pattern.rstrip(linesep) != '':
				ALLOWED_FILENAMES.append([version_part(pattern.rstrip(linesep)), filename_part(pattern.rstrip(linesep))])
		f.close()
		return True
	except:
		m.console_error()
		return False

def filename_part(pattern):
	return pattern[len(version_part(pattern)):]

def version_part(pattern):
	version = ''
	for char in pattern:
		if is_char_allowed(char, ALLOWED_REVISION_CHARS):
			version += char
		else:
			return version
	return version

def is_char_allowed(char, allowed_chars):
	for allowed in allowed_chars:
		if char == allowed:
			return True
	return False

def firmware_file_path():
	for pattern in ALLOWED_FILENAMES:
		if path.exists('firmware/' + c.read_config_value('firmware_version') + pattern[1]):
			return 'firmware/' + c.read_config_value('firmware_version') + pattern[1]
	return NOT_FOUND

def firmware_file_name():
	if not read_allowed_file():
		return NOT_FOUND
	for pattern in ALLOWED_FILENAMES:
		if path.exists('firmware/' + c.read_config_value('firmware_version') + pattern[1]):
			return c.read_config_value('firmware_version') + pattern[1]
	return NOT_FOUND

def is_a_valid_filename(filename):
	for pattern in ALLOWED_FILENAMES:
		if len(version_part(filename)) == len(pattern[0]) and filename_part(filename) == pattern[1]:
			return True
	return False

def is_version_higher(file_version, configuration_version):
	try:
		fv = float(file_version)
		sv = float(configuration_version)
		if fv <= sv:
			return False
		else:
			return True
	except:
		m.console_error()
		return False

def save_firmware(firmware):
	version = c.read_config_value('firmware_version')
	if not read_allowed_file():
		m.add_message(_('Could not open allowed firmware filenames file, firmware not saved.'))
		return version
	else:
		if not is_a_valid_filename(firmware.filename):
			m.add_message(_('Firmware not saved, only filenames of the following formats are allowed:'))
			for pattern in ALLOWED_FILENAMES:
				m.add_message('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + pattern[0] + pattern[1])
			m.add_message(_('where ?.?? is the firmware version, example: 1.00.'))
			return version
		else:
			if version != '' and not is_version_higher(version_part(firmware.filename), version):
				if firmware_file_path() != NOT_FOUND:
					if path.exists(firmware_file_path() + '.bak'):
						remove(firmware_file_path() + '.bak')
					m.add_message(_('The uploaded firmware version is not higher than the one previously installed.'))
					m.add_message(_('A backup of the old firmware was saved') + ': ' + firmware_file_path() + '.bak')
					rename(firmware_file_path(), firmware_file_path() + '.bak')
				else:
					m.add_message(_('Could not find the previously installed firmware file.'))
			elif version != '' and firmware_file_path() != NOT_FOUND:
				remove(firmware_file_path())
			if not path.exists('firmware'):
				makedirs('firmware')
			firmware.save('firmware', True)
			return version_part(firmware.filename)
