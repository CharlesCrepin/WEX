from bottle import run
from central import read_app_config_value

def configure_and_start_service():
	host = '0.0.0.0'
	port = 80
	debug = False
	reloader = False
	if read_app_config_value('host') != '':
		host = read_app_config_value('host')
	if read_app_config_value('port') != '':
		port = read_app_config_value('port')
	if read_app_config_value('debug') == 'enabled':
		debug = True
	if read_app_config_value('reloader') == 'enabled':
		reloader = True
	run(host=host, port=port, reloader=reloader, debug=debug)
