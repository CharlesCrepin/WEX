import central as c

def main_menu(active):
	if c.WEBUSER == c.ADMIN:
		items = [[_('Configure'), _('Go to configuration'), '/configure'], [_('Backup/Restore'), _('View configuration file'), '/backup_restore'], [_('Admin'), _('Administration'), '/admin'], [_('Log out'), _('Log out'), '/login']]
	else:
		items = [[_('Configure'), _('Go to configuration'), '/configure'], [_('Backup/Restore'), _('View configuration file'), '/backup_restore'], [_('Log out'), _('Log out'), '/login']]
	html = ''
	first = True
	for item in items:
		if first:
			first = False
			separator = ''
		else:
			separator = ' | '
		if active == item[2]:
			html += separator + '<span class="selected_menu">&nbsp;' + item[0] + '&nbsp;</span>'
		else:
			html += separator + '<a class="white_link" href="' + item[2] + '" title="' + item[1] + '">&nbsp;' + item[0] + '&nbsp;</a>'
	return html
