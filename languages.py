from gettext import translation
import central as c
import messages as m
from files import open_xml_file

LANGUAGES = [['en', 'English']]

def set_interface_language(language):
	try:
		if language != '':
			translation("wem", localedir='locale', languages=[language]).install()
	except:
		m.console_error()

def load_app_config_languages():
	tree = open_xml_file(c.APP_CONFIG_FILE)
	if tree is not None:
		global LANGUAGES
		LANGUAGES = [['en', 'English']]
		for child in tree.getroot():
			if child.tag == 'languages':
				for lang in child:
					if lang.attrib.get('value') != 'en':
						LANGUAGES.append([lang.attrib.get('value'), lang.attrib.get('label')])
