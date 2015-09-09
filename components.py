import central as c
from html_template import open_fieldset, close_fieldset

def button_row(row_label, button_name, button_type, button_value='', attributes='', help_text=''):
	html = '<tr>'
	html += '<td><label>' + row_label + ': </label></td>'
	html += '<td><button type="' + button_type + '" name="' + button_name + '" ' + attributes + '>' + button_value + '</button>'
	html += '<label class="radio_text">' + help_text + '</label></td>'
	html += '</tr>'
	return html

def span_row(span_value, attributes=''):
	return '<tr><td colspan="2"><span ' + attributes + '>' + span_value + '</span></td></tr>'

def input_row(row_label, input_name, input_type, input_value='', input_attributes='', options='', help_text=''):
	html = '<tr>'
	html += '<td><label>' + row_label + ': </label></td>'
	if input_type == 'radio':
		html += '<td>'
		for data in options:
			selected = ''
			if data[1] == input_value:
				selected = ' checked="checked"'
			html += '<input type="' + input_type + '" name="' + input_name + '" ' + input_attributes + ' id="' + data[0] + '" value="' + data[1] + '"' + selected + '>'
			html += '<label for="' + data[0] + '" class="radio_text">' + data[1]  + '</label>' + c.CR
		html += '<td>'
	else:
		html += '<td><input type="' + input_type + '" name="' + input_name + '" id="' + input_name + '" value="' + input_value + '" ' + input_attributes + '>'
		html += '<label for="' + input_name + '" class="radio_text">' + help_text + '</label></td>'
	html += '</tr>'
	return html

def select_row(row_label, select_name, select_value='', select_attributes='', select_options='', help_text=''):
	html = '<tr>'
	html += '<td><label>' + row_label + ': </label></td>'
	html += '<td><select name="' + select_name + '" ' + select_attributes + '>'
	for option in select_options:
		html += '<option value="' + option[0] + '"'
		if select_value == option[0]:
			html += ' selected="selected"'
		html += '>' + option[1] + '</option>'
	html += '</select>'
	html += '<label class="radio_text">' + help_text + '</label></td>'
	html += '</tr>'
	return html

def ip_row(row_label, input_name, input_value):
	html = '<tr>'
	html += '<td><label>' + row_label + ': </label></td>'
	html += '<td><div class="ip_div">' + c.CR
	for num in range(1, 5):
		if num == 1 and input_name != "subnet":
			html += '<input name="' + input_name + '_' + str(num) +'" type="text" maxlength="3" class="onlythree" onkeyup="ip_key_up(this);" onkeypress="return integers_only(event);" onblur="validate_ip_cell(this, 1);" value="'
			if input_value != '' and len(input_value.split('.')) == 4:
				html += input_value.split('.')[num-1]
			html += '">' + c.CR
		else:
			html += '<input name="' + input_name + '_' + str(num) +'" type="text" maxlength="3" class="onlythree" onkeyup="ip_key_up(this);" onkeypress="return integers_only(event);" onblur="validate_ip_cell(this, 0);" value="'
			if input_value != '' and len(input_value.split('.')) == 4:
				html += input_value.split('.')[num-1]
			html += '">' + c.CR
		if num < 4:
			html += ' . '
	html += '</div></td>'
	html += '</tr>'
	return html

def is_checked(setting, component_value):
	if setting == component_value:
		return 'checked="checked"'
	return ''

def is_ip_blank(request, input_name):
	if request.forms.get(input_name + '_1') == '' and request.forms.get(input_name + '_2') == '' and request.forms.get(input_name + '_3') == '' and request.forms.get(input_name + '_4') == '':
		return True
	else:
		return False

def concat_ip_cells(request, input_name):
	return request.forms.get(input_name + '_1') + '.' + request.forms.get(input_name + '_2') + '.' + request.forms.get(input_name + '_3') + '.' + request.forms.get(input_name + '_4')

def display_fieldsets(fieldsets):
	html = ''
	for fieldset in fieldsets:
		html += open_fieldset(fieldset[0])
		for row in fieldset[2]:
			if gv(row, 0) == 'span_row':
				html += span_row(gv(row, 1), gv(row, 2)) + c.CR
			if gv(row, 0) == 'input_row':
				html += input_row(gv(row, 1), gv(row, 2), gv(row, 3), gv(row, 4), gv(row, 5), gv(row, 6), gv(row, 7)) + c.CR
			elif gv(row, 0) == 'select_row':
				html += select_row(gv(row, 1), gv(row, 2), gv(row, 3), gv(row, 4), gv(row, 5), gv(row, 6)) + c.CR
			elif gv(row, 0) == 'button_row':
				html += button_row(gv(row, 1), gv(row, 2), gv(row, 3), gv(row, 4), gv(row, 5), gv(row, 6)) + c.CR
			elif gv(row, 0) == 'ip_row':
				html += ip_row(gv(row, 1), gv(row, 2), gv(row, 3)) + c.CR
		html += close_fieldset() + '<br/>' + c.CR
	return html

def gv(row, index):
	try:
		return row[index]
	except:
		return ''
