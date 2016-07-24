#!/usr/bin/python
# check_phish
#
# Plugin for Nagios
# Written by A. Shibani (a@shumbashi.io)
# Last Modified: 2016-07-23
#
# Usage: ./check_phish IP-ADDRESS
#
# Description:
#
# This plugin will check if the supplied IP address is associated with any alive phishing reports on http://clean-mx.de.

import urllib
import xmltodict
from sys import argv

try:
	ip_address = argv[1]
except Exception:
	print 'Missing IP Address to check'
	exit(3)

url = 'http://support.clean-mx.de/clean-mx/xmlphishing.php?response=alive&ip='

def fetch(url):
	try:
		data = urllib.urlopen(url)
		fdata = data.read()
		data_dict = xmltodict.parse(fdata)
	except Exception:
		exit_status=0
		print 'WARNING: Unable to fetch report, assumed OK'
		exit(exit_status)
	return data_dict

data_dict = fetch(url+ip_address)

if data_dict['output']['entries'] != None:
	exit_status=2
	message = 'CRITICAL: The following URLs are phishing sources:\n'
	for e in data_dict['output']['entries']['entry']:
		message += e['url']+'\n'

	print message
	exit(exit_status)

else:
	exit_status=0
	message = 'OK: No URLs reported as phishing sources'
	print message
	exit(exit_status)
