from socket import inet_aton
from struct import unpack

def validate_ip_address(ip):
	try:
		inet_aton(ip)
		return True
	except:
		return False

def get_network_in_cidr(ip, netmask):
	ipaddr = ip.split('.')
	netmask = netmask.split('.')
	net_start = [str(int(ipaddr[x]) & int(netmask[x])) for x in range(0,4)]
	return '.'.join(net_start) + '/' + get_network_size(netmask)

def get_network_size(netmask):
    binary_str = ''
    for octet in netmask:
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))

def address_in_network(ip, cidr_net):
    ipaddr = unpack('=L', inet_aton(ip))[0]
    netaddr, bits = cidr_net.split('/')
    netmask = unpack('=L', inet_aton(calculate_dotted_netmask(int(bits))))[0]
    network = unpack('=L', inet_aton(netaddr))[0] & netmask
    return (ipaddr & netmask) == (network & netmask)

def calculate_dotted_netmask(mask):
    bits = 0
    for i in range(32 - mask, 32):
        bits |= (1 << i)
    return "%d.%d.%d.%d" % ((bits & 0xff000000) >> 24, (bits & 0xff0000) >> 16, (bits & 0xff00) >> 8 , (bits & 0xff))
