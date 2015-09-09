from os import rename, remove, path
from time import strftime
import central as c
from files import open_file, open_xml_file
import messages as m
from files import copy_directory
import data as data
from components import is_checked, display_fieldsets
from html_template import html_template_start, html_template_end
from menu import main_menu
import languages as l

def create_admin_fieldsets():
	row1 = ['input_row', _('Username'), 'username', 'text', c.read_app_config_value('username')]
	row2 = ['input_row', _('Password'), 'password', 'text', c.read_app_config_value('password')]
	row3 = ['select_row', _('Languages'), 'languages', '', 'multiple="multiple" id="languages"', l.LANGUAGES]
	row4 = ['button_row', _('Remove selected language'), '', 'button', _('Remove'), 'onclick="remove_from_select(\'languages\');"']
	row5 = ['span_row', _('Install a new language'), 'class="sub_title"']
	row6 = ['input_row', _('Code'), 'code', 'text', '', '', '', 'Example: en']
	row7 = ['input_row', _('Label'), 'label', 'text', '', '', '', 'Example: English']
	row8 = ['input_row', _('Title'), 'title', 'text', c.read_app_config_value('title'), 'size="40"']
	row9 = ['input_row', _('Host'), 'host', 'text', c.read_app_config_value('host'), 'onkeypress="return ip_keys_only(event);" placeholder="0.0.0.0"', '', 'Default is 0.0.0.0 to listen to all interfaces.']
	row10 = ['input_row', _('Port'), 'port', 'text', c.read_app_config_value('port'), 'onkeypress="return integers_only(event);" placeholder="80"', '', 'Default is 80.']
	row11 = ['input_row', _('Debug'), 'debug', 'checkbox', 'enabled', is_checked(c.read_app_config_value('debug'), 'enabled'), '', _('Enabled')]
	row12 = ['input_row', _('Reloader'), 'reloader', 'checkbox', 'enabled', is_checked(c.read_app_config_value('reloader'), 'enabled'), '', _('Enabled')]
	row13 = ['span_row', '<br/>' + _('Debug and Reloader should be disabled in production mode.') + '<br/>' + _('A restart of the service is needed to activate changes made in this section.'), 'class="note"']
	return [[_('Security'), 'security', [row1, row2]], [_('Interface'), 'interface', [row8, row3, row4, row5, row6, row7]], [_('Service'), 'service', [row9, row10, row11, row12, row13]]]

def admin_html():
	html = html_template_start('/admin', c.read_app_config_value('title'), c.read_config_value('firmware_version'), main_menu('/admin'))
	html += '<form action="/admin_submit" method="post" onsubmit="select_all_options(\'languages\');">' + c.CR
	html += display_fieldsets(data.ADMIN_FIELDSETS)
	html += '<input type="submit" value="' + _('Save') + '" name="submit"/>' + c.CR
	html += '<input type="reset" value="' + _('Cancel changes') + '" name="cancel" style="margin-top:10px;"/>' + c.CR
	html += '</form>' + c.CR
	html += html_template_end()
	return html

def update_app_config_value(element_name, element_value):
	tree = open_xml_file(c.APP_CONFIG_FILE)
	if tree is not None:
		root = tree.getroot()
		for child in root:
			if child.tag == element_name:
				child.set('value', element_value)
				break
		tree.write(c.APP_CONFIG_FILE, encoding='utf-8', xml_declaration=True)

def write_app_config(request, language):
	if path.exists(c.APP_CONFIG_FILE + '.bak'):
		remove(c.APP_CONFIG_FILE + '.bak')
	if path.exists(c.APP_CONFIG_FILE):
		rename(c.APP_CONFIG_FILE, c.APP_CONFIG_FILE + '.bak')
		m.add_message(_('A copy of your configuration file was saved as: ') + c.APP_CONFIG_FILE + '.bak')
	f = open_file(c.APP_CONFIG_FILE, 'w')
	if f is None:
		m.add_message(_('Unexpected error: could not open configuration file, configuration was not saved.'))
		return
	f.write ('<?xml version=\'1.0\' encoding=\'utf-8\'?>' + c.CR + '<settings>' + c.CR)
	f.write('\t<languages>' + c.CR)
	while len(request.forms.getall('languages')) < len(l.LANGUAGES):
		index = -1
		found = False
		for lang in l.LANGUAGES:
			index += 1
			if lang[0] != 'en':
				found = False
				for select_language in request.forms.getall('languages'):
					if lang[0] == select_language:
						found = True
						break
				if not found:
					break
		if not found:
			del l.LANGUAGES[index]
	if request.forms.get('code') != '' and request.forms.get('label') != '':
		l.LANGUAGES.append([request.forms.get('code'), request.forms.get('label')])
		if not path.exists('locale/' + request.forms.get('code')):
			copy_directory('locale/en', 'locale/' + request.forms.get('code'))
			m.add_message(_('A new folder was created: locale/') + request.forms.get('code'))
			m.add_message(_('Fill the msgstr fields in LC_MESSAGES/wem.pot with translations in ') + request.forms.get('label') + (', then run create_mo_from_po.sh'))
			m.add_message(_('Finally, restart the service.'))
	for lang in l.LANGUAGES:
		f.write('\t\t<language value="' + lang[0] + '" label="' + lang[1] + '"/>' + c.CR)
	f.write('\t</languages>' + c.CR)
	f.write('\t<language value="' + language + '"/>' + c.CR)
	for fieldset in data.ADMIN_FIELDSETS:
		for row in fieldset[2]:
			if row[0] == 'input_row':
				if row[3] == 'text' and row[2] != 'code' and row[2] != 'label':
						f.write('\t<' + row[2] + ' value="' + request.forms.get(row[2]) + '"/>' + c.CR)
				elif row[3] == 'checkbox':
					write_checkbox_for_admin(f, row[2], request.forms.get(row[2]), 'disabled')
			elif row[0] == 'select_row' and row[2] != 'languages':
				f.write('\t<' + row[2] + ' value="' + request.forms.get(row[2]) + '"/>' + c.CR)
	f.write('</settings>' + c.CR)
	f.close()
	m.add_message('<font color="#373">' +_('Application configuration saved') + ', ' + strftime("%c") + '.</font>')

def write_checkbox_for_admin(f, name, component, unchecked):
	if component is None or component == '':
		f.write('\t<' + name + ' value="' + unchecked + '"/>' + c.CR)
	else:
		f.write('\t<' + name + ' value="' + component + '"/>' + c.CR)
