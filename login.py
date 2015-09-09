import central as c
import messages as m
from html_template import html_template_start, html_template_end
from components import select_row
import languages as l

def is_user_logged(user):
	if user == "Anonymous":
		m.add_message(_('Login required.'))
		return False
	return True

def check_security(username, password):
	if username == c.ADMIN and password == c.ADMIN_PASSWORD:
		return True
	if username != '' and username == c.read_app_config_value('username') and password != '' and password == c.read_app_config_value('password'):
		return True
	return False

def login_html():
	html = html_template_start('/login', c.read_app_config_value('title'), c.read_config_value('firmware_version'), _('Identification'))
	html += '<form action="/login_submit" method="post" class="text_align_center">' + c.CR
	html += '<br/><div><input type="text" placeholder="' + _('Username') + '" name="username"/></div><br/>' + c.CR
	html += '<div><input type="password" placeholder="' + _('Password') + '" name="password"/></div>' + c.CR
	html += '<br/>' + c.CR
	html += '<table style="margin:0 auto;">' + select_row(_('Interface language'), 'language', c.read_app_config_value('language'), '', l.LANGUAGES) + '</table>' + c.CR
	html += '<br/>' + c.CR
	html += '<input type="submit" value="' + _('Log in') + '"/>' + c.CR
	html += '</form>' + c.CR
	html += html_template_end()
	return html
