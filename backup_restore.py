from os import path, linesep, remove, rename
from time import strftime
import central as c
import messages as m
from files import open_file
import data as data
from components import button_row, input_row
from html_template import html_template_start, html_template_end, open_fieldset, close_fieldset
from menu import main_menu

def backup_restore_html():
	html = html_template_start('/backup_restore', c.read_app_config_value('title'), c.read_config_value('firmware_version'), main_menu('/backup_restore'))
	html += '<form action="/backup_restore_submit" method="post" enctype="multipart/form-data">' + c.CR
	html += open_fieldset(_('Download/Upload'))
	html += button_row(_('Backup'), '', 'button', _('Download a copy'), 'onclick="download_configuration(\'' + get_config_file_name() + '\');"') + c.CR
	html += input_row(_('Restore'), 'uploaded_file', 'file') + c.CR
	html += '<tr><td><input type="submit" value="' + _('Upload') + '" name="submit"/></td><td></td></tr>' + c.CR
	html += close_fieldset() + '<br/>'
	html += open_fieldset(_('File content'))
	html += '<tr><td class="display_file">'
	html += display_config_file()
	html += '</td></tr>'
	html += close_fieldset()
	html += '</form>' + c.CR
	html += html_template_end()
	return html

def get_config_file_name():
	if path.exists(c.CONFIG_FILE):
		return c.CONFIG_FILE
	return '-NotFoundForJavascript-'

def display_config_file():
	html = ''
	f = open_file(c.CONFIG_FILE, 'r')
	if f is None:
		html += '<font color="#c60">' + _('The configuration file can not be viewed, file not found.') + '</font><br/>'
	else:
		for line in f.readlines():
			html += line + '<br>'
		f.close()
	return html

def restore(uploaded_file):
	try:
		uploaded_file.save(c.TEMP_CONFIG_FILE, True)
		f1 = open_file(c.TEMP_CONFIG_FILE, 'r')
		if f1 is None:
			m.add_message(_('Unexpected error: could not open temporary configuration file, file not uploaded.'))
			return
		output = ''
		for line in f1.readlines():
			line = line.rstrip(linesep)
			if line != '' and '=' in line:
				param, value = line.split('=')
				if param != '':
					for fieldset in data.CONFIG_FIELDSETS:
						found = False
						for row in fieldset[2]:
							if row[2] == param:
								output += param + '=' + value + c.CR
								found = True
								break
						if found:
							break
		f1.close()
		if path.exists(c.TEMP_CONFIG_FILE):
			remove(c.TEMP_CONFIG_FILE)
		if len(output) < 2:
			m.add_message(_('No relevant data in uploaded file, file not uploaded.'))
			return
		if path.exists(c.CONFIG_FILE):
			if path.exists(c.CONFIG_FILE + '.bak'):
				remove(c.CONFIG_FILE + '.bak')
			rename(c.CONFIG_FILE, c.CONFIG_FILE + '.bak')
			m.add_message(_('A copy of your configuration file was saved as: ') + c.CONFIG_FILE + '.bak')
		f2 = open_file(c.CONFIG_FILE, 'w')
		if f2 is None:
			m.add_message(_('Unexpected error: could not open configuration file, file not uploaded.'))
			return
		f2.write(output)
		f2.close()
		m.add_message('<font color="#373">' + _('Configuration file uploaded') + ', ' + strftime("%c") + '.</font>')
	except:
		m.add_message(_('Invalid file format, file not uploaded.'))
		try:
			f1.close()
			f2.close()
			if path.exists(c.TEMP_CONFIG_FILE):
				remove(c.TEMP_CONFIG_FILE)
		except:
			return
