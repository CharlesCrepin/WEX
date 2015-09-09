import central as c
import messages as m

def html_template_start(route, page_title, firmware_version, menu, body_onload_param=''):
	html = '<!DOCTYPE html>' + c.CR
	html += '<html>' + c.CR
	html += '<head>' + c.CR
	html += '<meta charset="utf-8"/>' + c.CR
	html += '<title>Webb Exchange Module</title>' + c.CR
	html += '<link type="text/css" href="/static/wem.css" rel="stylesheet">' + c.CR
	html += '<script type="text/javascript" src="/static/wem.js"></script>' + c.CR
	html += '</head>' + c.CR
	html += '<body'
	if route == '/configure':
		html += ' onload="setup_configuration_form(\'' + body_onload_param + '\');"'
	html += '>' + c.CR
	if m.MESSAGES != '':
		html += '<div class="messages">' + m.MESSAGES + '</div><br/>' + c.CR
		m.clear_messages()
	html += '<div id="main_div">' + c.CR
	if firmware_version == '':
		firmware_version = 'not set'
	html += '<div class="logo"><img src="/static/logo.png" alt="Logo"/><div class="firmware_info">' + _('Firmware version') + ': ' + firmware_version + '<br/>' + _('Software version') + ': ' + c.APP_VERSION + '</div></div>' + c.CR
	html += '<div class="page_title">' + page_title + '</div>' + c.CR
	html += '<div id="triangle_up"></div>' + c.CR
	html += '<div class="section_title">' + menu + '</div>' + c.CR
	return html

def html_template_end():
	return '</div>' + c.CR + '</body>' + c.CR + '</html>' + c.CR

def open_fieldset(legend):
	html = '<fieldset><legend>' + legend + '</legend>' + c.CR
	html += '<table class="in_fieldset">' + c.CR
	return html

def close_fieldset():
	html = '</table>' + c.CR
	html += '</fieldset>' + c.CR
	return html
