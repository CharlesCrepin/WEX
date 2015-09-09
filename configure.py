from os import rename, remove, path, linesep
from time import strftime
import central as c
import messages as m
from files import open_file
import data as data
from html_template import html_template_start, html_template_end
from components import is_checked, concat_ip_cells, display_fieldsets, is_ip_blank
from time_zones import load_time_zones
from firmware import firmware_file_name
from menu import main_menu
from ip_validation import validate_ip_address, address_in_network, get_network_in_cidr

def create_configure_fieldsets():
	row1 = ['input_row', _('Identifier'), 'identifier', 'text', c.read_config_value('identifier')]
	row2 = ['select_row', _('Language(s)'), 'language', c.read_config_value('language'), '', [['', ''], ['English', 'English'], ['English French', 'English - French'], ['French', 'French'], ['French English', 'French - English']]]
	row3 = ['input_row', _('Context'), 'context', 'text', c.read_config_value('context')]
	time_zones = load_time_zones()
	if len(time_zones) < 2:
		m.add_message(_('Time zones file not found or empty.'))
	row4 = ['select_row', _('Time zone'), 'timezone', c.read_config_value('timezone'), '', time_zones]
	row5 = ['button_row', _('Backup firmware'), '', 'button', _('Download'), 'onclick="download_firmware(\'' + firmware_file_name() + '\');"', firmware_file_name()]
	row6 = ['input_row', _('Update firmware'), 'firmware_version', 'file', '', 'accept=".gz"']
	row7 = ['input_row', _('Hostname'), 'hostname', 'text', c.read_config_value('hostname')]
	row8 = ['input_row', _('Domain name'), 'domain_name', 'text', c.read_config_value('domain_name')]
	row9 = ['select_row', _('Connection type'), 'connection_type', c.read_config_value('connection_type'), 'onchange="change_connection_type(this);"', [['dhcp', 'DHCP'], ['static', 'Static']]]
	row10 = ['ip_row', _('IP address'), 'ip', c.read_config_value('ip'), 'connection_type']
	row11 = ['ip_row', _('Subnet mask'), 'subnet', c.read_config_value('subnet'), 'connection_type']
	row12 = ['ip_row', _('Default gateway'), 'gateway', c.read_config_value('gateway'), 'connection_type']
	row13 = ['ip_row', _('Static DNS 1'), 'dns1', c.read_config_value('dns1'), 'connection_type']
	row14 = ['ip_row', _('Static DNS 2'), 'dns2', c.read_config_value('dns2'), 'connection_type']
	row15 = ['input_row', _('Admin access'), 'admin_access', 'checkbox', 'enable', is_checked(c.read_config_value('admin_access'), 'enable'), '', _('Enabled')]
	row16 = ['input_row', _('Utility access'), 'utility_access', 'radio', c.read_config_value('utility_access'), '', [['utility_access_1', 'http'], ['utility_access_2', 'https']]]
	row17 = ['input_row', _('SNMP'), 'SNMP', 'checkbox', 'enable', is_checked(c.read_config_value('SNMP'), 'enable'), '', _('Enabled')]
	row18 = ['input_row', _('Web login name'), 'Web_Login_Name', 'text', c.read_config_value('Web_Login_Name')]
	row19 = ['input_row', _('Web login password'), 'Web_Login_password', 'text', c.read_config_value('Web_Login_password')]
	row20 = ['input_row', _('SSH'), 'SSH', 'checkbox', 'enable', is_checked(c.read_config_value('SSH'), 'enable'), '', _('Enabled')]
	row21 = ['input_row', _('SSH login name'), 'SSH_Login_Name', 'text', c.read_config_value('SSH_Login_Name')]
	row22 = ['input_row', _('SSH login password'), 'SSH_Login_password', 'text', c.read_config_value('SSH_Login_password')]
	row23 = ['input_row', _('Syslog'), 'syslog', 'checkbox', 'enable', is_checked(c.read_config_value('syslog'), 'enable'), '', _('Enabled')]
	row24 = ['input_row', _('Max size'), 'max_size', 'text', c.read_config_value('max_size')]
	row25 = ['input_row', _('Report by mail'), 'report_by_mail', 'checkbox', 'enable', is_checked(c.read_config_value('report_by_mail'), 'enable'), '', _('Enabled')]
	row26 = ['input_row', _('Sender'), 'mail_sender', 'text', c.read_config_value('mail_sender')]
	row27 = ['input_row', _('Receiver'), 'mail_receiver', 'text', c.read_config_value('mail_receiver')]
	row28 = ['input_row', _('Subject'), 'mail_subject', 'text', c.read_config_value('mail_subject')]
	row29 = ['input_row', _('SMTP server'), 'mail_smtp_server', 'text', c.read_config_value('mail_smtp_server')]
	row30 = ['input_row', _('SMTP'), 'SMTP', 'text', c.read_config_value('SMTP')]
	row31 = ['input_row', _('Log count'), 'MAIL_Log_Count', 'text', c.read_config_value('MAIL_Log_Count')]
	row32 = ['input_row', _('Interval'), 'MAIL_Interval', 'text', c.read_config_value('MAIL_Interval')]
	row33 = ['input_row', _('SMTP user'), 'MAIL_Smtp_User', 'text', c.read_config_value('MAIL_Smtp_User')]
	row34 = ['input_row', _('Proxy'), 'proxy', 'text', c.read_config_value('proxy')]
	row35 = ['input_row', _('Outbound proxy'), 'outbound_proxy', 'text', c.read_config_value('outbound_proxy')]
	row36 = ['input_row', _('Registration'), 'registration', 'checkbox', 'enable', is_checked(c.read_config_value('registration'), 'enable'), '', _('Enabled')]
	row37 = ['input_row', _('Registration expires'), 'registration_expires', 'text', c.read_config_value('registration_expires'), 'onkeypress="return integers_only(event);"', '', _('seconds')]
	row38 = ['input_row', _('Use outbound proxy'), 'use_OBP', 'checkbox', 'enable', is_checked(c.read_config_value('use_OBP'), 'enable'), '', _('Enabled')]
	row39 = ['input_row', _('Send calls without registration'), 'send_calls_without_reg', 'checkbox', 'enable', is_checked(c.read_config_value('send_calls_without_reg'), 'enable'), '', _('Enabled')]
	row40 = ['input_row', _('Receive calls without registration'), 'receive_calls_without_reg', 'checkbox', 'enable', is_checked(c.read_config_value('receive_calls_without_reg'), 'enable'), '', _('Enabled')]
	row41 = ['input_row', _('CID'), 'CID', 'text', c.read_config_value('CID')]
	row42 = ['input_row', _('UID'), 'UID', 'text', c.read_config_value('UID')]
	row43 = ['input_row', _('Password'), 'password', 'text', c.read_config_value('password')]
	row44 = ['input_row', _('Dial plan'), 'dialplan', 'text', c.read_config_value('dialplan')]
	return [[_('Identifier'), 'identifier', [row1, row2]], [_('Global'), 'global', [row3, row4, row5, row6]], [_('Network'), 'network', [row7, row8, row9, row10, row11, row12, row13, row14]], [_('Web access'), 'web_access', [row15, row16, row17, row18, row19, row20, row21, row22]], [_('Log'), 'log', [row23, row24, row25, row26, row27, row28, row29, row30, row31, row32, row33]], [_('Proxy and registration'), 'proxy and registration', [row34, row35, row36, row37, row38, row39, row40]], [_('Subscriber'), 'subscriber', [row41, row42, row43, row44]]]

def configure_html():
	html = html_template_start('/configure', c.read_app_config_value('title'), c.read_config_value('firmware_version'), main_menu('/configure'), c.read_config_value('connection_type'))
	html += '<form action="/configure_submit" method="post" enctype="multipart/form-data">' + c.CR
	html += display_fieldsets(data.CONFIG_FIELDSETS)
	html += '<input type="submit" value="' + _('Save configuration') + '" name="submit"/>' + c.CR
	html += '<input type="reset" value="' + _('Cancel all changes') + '" name="cancel" style="margin-top:10px;"/>' + c.CR
	html += '</form>' + c.CR
	html += html_template_end()
	return html

def write_configuration(request, firmware_version):
	if path.exists(c.CONFIG_FILE + '.bak'):
		remove(c.CONFIG_FILE + '.bak')
	if path.exists(c.CONFIG_FILE):
		rename(c.CONFIG_FILE, c.CONFIG_FILE + '.bak')
		m.add_message(_('A copy of your configuration file was saved as: ') + c.CONFIG_FILE + '.bak')
	f = open_file(c.CONFIG_FILE, 'w')
	if f is None:
		m.add_message(_('Unexpected error: could not open configuration file, configuration was not saved.'))
		return
	flag_network_ok = True
	if request.forms.get('connection_type') == 'static':
		if validate_ip_address(concat_ip_cells(request, 'ip')) and validate_ip_address(concat_ip_cells(request, 'subnet')) and validate_ip_address(concat_ip_cells(request, 'gateway')):
			if not address_in_network(concat_ip_cells(request, 'gateway'), get_network_in_cidr(concat_ip_cells(request, 'ip'), concat_ip_cells(request, 'subnet'))):
				m.add_message(_('Invalid combination of ip, subnet and gateway, addresses not saved.'))
				flag_network_ok = False
	num = 1
	for fieldset in data.CONFIG_FIELDSETS:
		if num == 1:
			f.write('[' + fieldset[1] + ']' + c.CR)
		else:
			f.write(c.CR + '[' + fieldset[1] + ']' + c.CR)
		num = 0
		for row in fieldset[2]:
			if row[0] == 'input_row':
				if row[3] == 'text':
					f.write(row[2] + '=' + request.forms.get(row[2]) + c.CR)
				elif row[3] == 'checkbox':
					f.write(write_checkbox(row[2], request.forms.get(row[2]), 'disable') + c.CR)
				elif row[3] == 'radio':
					f.write(write_radio(row[2], request.forms.get(row[2])) + c.CR)
				elif row[3] == 'file':
					f.write(row[2] + '=' + firmware_version + c.CR)
			elif row[0] == 'select_row':
				f.write(write_select(row[2],request.forms.get(row[2])) + c.CR)
			elif row[0] == 'ip_row':
				if row[4] != 'connection_type':
					#for now we write them
					f.write(write_ip(request, row[2], row[1]) + c.CR)
				elif request.forms.get('connection_type') == 'static':
					if flag_network_ok:
						f.write(write_ip(request, row[2], row[1]) + c.CR)
					elif row[2] != 'ip' and row[2] != 'subnet' and row[2] != 'gateway':
						f.write(write_ip(request, row[2], row[1]) + c.CR)
	f.close()
	m.add_message('<font color="#373">' +_('Configuration saved') + ', ' + strftime("%c") + '.</font>')

def write_select(name, component):
	if component is None:
		return name + '='
	return name + '=' + component
	
def write_checkbox(name, component, unchecked):
	if component is None or component == '':
		return name + '=' + unchecked
	return name + '=' + component

def write_radio(name, component):
	if component is None:
		return name + '='
	return name + '=' + component

def write_ip(request, field, label):
	if not is_ip_blank(request, field):
		if not validate_ip_address(concat_ip_cells(request, field)):
			m.add_message(label + _(' was not saved because it was invalid.'))
		else:
			return field + '=' + concat_ip_cells(request, field)
