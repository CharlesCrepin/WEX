import central as c
from files import open_xml_file

def load_time_zones():
	time_zones = []
	tree = open_xml_file(c.TIME_ZONES_FILE)
	if tree is not None:
		time_zones.append(['', ''])
		for child in tree.getroot():
			time_zones.append([child.attrib.get('value'), child.attrib.get('label')])
	return time_zones
