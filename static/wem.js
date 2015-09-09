function select_all_options(elementId) {
	try {
		element = document.getElementById(elementId);
		for (var i=0; i<element.options.length; i++) {
			element.options[i].selected = true;
		}
	}
	catch (err) {
		window.alert("Javascript error in select_all_options(): " + err);
	}
}

function remove_from_select(elementId) {
	try {
		element = document.getElementById(elementId);
		if (element.selectedIndex == 0) alert("English can not be removed.");
		else if (element.selectedIndex != -1) element.remove(element.selectedIndex);
	}
	catch (err) {
		window.alert("Javascript error in remove_from_select(): " + err);
	}
}

function download_firmware(filename) {
	try {
		if (filename == "-NotFound-") {
			window.alert("No firmware file was found.");
		}
		else window.location.href = "/firmware/" + filename;
	}
	catch (err) {
		window.alert("Javascript error in download_firmware(): " + err);
	}
}

function download_configuration(filename) {
	try {
		if (filename == "-NotFoundForJavascript-") {
			window.alert("No configuration file was found.");
		}
		else window.location.href = "/" + filename;
	}
	catch (err) {
		window.alert("Javascript error in download_configuration(): " + err);
	}
}

function collapse_element(elementId) {
	try {
		if (document.getElementById(elementId).style.display == "none")
			document.getElementById(elementId).style.display = "block";
		else
			document.getElementById(elementId).style.display = "none";
	}
	catch (err) {
		window.alert("Javascript error in collapse_element(): " + err);
	}
}

function setup_configuration_form(connection_type) {
	try {
		if (connection_type == "dhcp" || connection_type == "") disable_static_info();
		else enable_static_info();
	}
	catch (err) {
		window.alert("Javascript error in setup_configuration_form(): " + err);
	}
}

function change_connection_type(element) {
	try {
		if (element.value == "dhcp" || element.value == "") disable_static_info();
		else enable_static_info();
	}
	catch (err) {
		window.alert("Javascript error in change_connection_type(): " + err);
	}
}

function disable_element(elements) {
	try {
		if (elements[0] != undefined) {
			elements[0].disabled = true;
			elements[0].style.background = "#eee";
		}
	}
	catch (err) {
		window.alert("Javascript error in disable_element(): " + err);
	}
}

function enable_element(elements) {
	try {
		if (elements[0] != undefined) {
			elements[0].disabled = false;
			elements[0].style.background = "#fff";
		}
	}
	catch (err) {
		window.alert("Javascript error in enable_element(): " + err);
	}
}

function disable_static_info() {
	try {
		for (i = 1; i < 5; i++) {
			disable_element(document.getElementsByName("ip_" + i));
			disable_element(document.getElementsByName("subnet_" + i));
			disable_element(document.getElementsByName("gateway_" + i));
			disable_element(document.getElementsByName("dns1_" + i));
			disable_element(document.getElementsByName("dns2_" + i));
		}
	}
	catch (err) {
		window.alert("Javascript error in disable_static_info(): " + err);
	}
}

function enable_static_info() {
	try {
		for (i = 1; i < 5; i++) { 
			enable_element(document.getElementsByName("ip_" + i));
			enable_element(document.getElementsByName("subnet_" + i));
			enable_element(document.getElementsByName("gateway_" + i));
			enable_element(document.getElementsByName("dns1_" + i));
			enable_element(document.getElementsByName("dns2_" + i));
		}
	}
	catch (err) {
		window.alert("Javascript error in enable_static_info(): " + err);
	}
}

function integers_only(e) {
	try {
		//alert(e.keyCode);
		var keyCode = e.keyCode == 0 ? e.charCode : e.keyCode;
		var allowed = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57];
		if (allowed.indexOf(keyCode) == -1) {
			return false;
		}
		return true;
	}
	catch (err) {
		window.alert("Javascript error in integers_only(): " + err);
	}
}

function ip_keys_only(e) {
	try {
		//alert(e.keyCode);
		var keyCode = e.keyCode == 0 ? e.charCode : e.keyCode;
		var allowed = [46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 110, 190];
		if (allowed.indexOf(keyCode) == -1) {
			return false;
		}
		return true;
	}
	catch (err) {
		window.alert("Javascript error in ip_keys_only(): " + err);
	}
}

function ip_key_up(who) {
	try {
		if (who.value.length == 3 && who.nextSibling.nextSibling != undefined && who.nextSibling.nextSibling.nodeName == 'INPUT') {
			who.nextSibling.nextSibling.focus();
			who.nextSibling.nextSibling.setSelectionRange(0, who.nextSibling.nextSibling.value.length);
		}
	}
	catch (err) {
		window.alert("Javascript error in ip_key_up(): " + err);
	}
}

function validate_ip_cell(ip_cell, is_first_cell) {
	try {
		ip_cell.style.background = "#fff";
		ip_cell.title = "";
		if (ip_cell.value.length == 0) {
			return false;
		}
		if (is_first_cell == 1) {
			if (ip_cell.value < 1 || ip_cell.value > 223) {
				ip_cell.title = "Must be a number between 1 and 223 included";
				ip_cell.style.background = "#fc3";
				//ip_cell.value = "223";
				return false;
			}
		}
		else {
			if (ip_cell.value < 0 || ip_cell.value > 255) {
				ip_cell.title = "Must be a number between 0 and 255 included";
				ip_cell.style.background = "#fc3";
				//ip_cell.value = "255";
				return false;
			}
		}		
	}
	catch (err) {
		window.alert("Javascript error in validate_ip_cell(): " + err);
	}
}
