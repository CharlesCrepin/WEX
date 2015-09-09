from bottle import route, request, static_file, redirect
from os import path
import central as c
import messages as m
from languages import load_app_config_languages, set_interface_language
import data as data
from admin import admin_html, write_app_config, update_app_config_value, create_admin_fieldsets
from backup_restore import backup_restore_html, restore
from configure import create_configure_fieldsets, write_configuration, configure_html
from firmware import save_firmware
from login import is_user_logged, check_security, login_html
from service import configure_and_start_service

load_app_config_languages()
set_interface_language('en')

@route('/<filename>')
def root_files(filename):
	return static_file(filename, root='', download=filename)

@route('/static/<filename>')
def static_files(filename):
	return static_file(filename, root='static/')

@route('/firmware/<filename>')
def firmware_files(filename):
	return static_file(filename, root='firmware/', download=filename)

@route('/', method='GET')
@route('/login', method='GET')
def login():
	set_interface_language(c.read_app_config_value('language'))
	c.WEBUSER = "Anonymous"
	return login_html()

@route('/login_submit', method='POST')
def login_submit():
	set_interface_language(request.forms.get('language'))
	update_app_config_value('language', request.forms.get('language'))
	if check_security(request.forms.get('username'), request.forms.get('password')):
		c.WEBUSER = request.forms.get('username')
		redirect('/configure')
	m.add_message(_('The credentials supplied are not valid.'))
	redirect('/login')

@route('/configure', method='GET')
def configure():
	if not is_user_logged(c.WEBUSER):
		redirect('/login')
	if not path.exists(c.CONFIG_FILE):
		m.add_message(_('Configuration file not found.'))
	data.CONFIG_FIELDSETS = create_configure_fieldsets()
	return configure_html()

@route('/configure_submit', method='POST')
def configure_submit():
	firmware_version = c.read_config_value('firmware_version')
	firmware = request.files.get('firmware_version')
	if firmware is not None:
		firmware_version = save_firmware(firmware)
	write_configuration(request, firmware_version)
	redirect('/configure')

@route('/backup_restore', method='GET')
def backup_restore():
	if not is_user_logged(c.WEBUSER):
		redirect('/login')
	return backup_restore_html()

@route('/backup_restore_submit', method='POST')
def backup_restore_submit():
	uploaded_file = request.files.get('uploaded_file')
	if uploaded_file is not None:
		restore(uploaded_file)
	else:
		m.add_message(_('Nothing was uploaded, choose a file first.'))
	redirect('/backup_restore')

@route('/admin', method='GET')
def admin():
	if not is_user_logged(c.WEBUSER):
		redirect('/login')
	if c.WEBUSER != c.ADMIN:
		redirect('/login')
	data.ADMIN_FIELDSETS = create_admin_fieldsets()
	return admin_html()

@route('/admin_submit', method='POST')
def admin_submit():
	write_app_config(request, c.read_app_config_value('language'))
	redirect('/admin')

configure_and_start_service()
