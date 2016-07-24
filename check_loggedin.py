#!/usr/bin/python
# check_logged_in_users
#
# Plugin for Nagios
# Written by A. Shibani (a@shumbashi.io)
# Last Modified: 12-May-2016
#
# Description:
#
# This plugin will check if any users are logged in and report their IP address.
# An 'OK' message is returned if no users are logged in or if the IP address is in the allowed list
# A "CRITICAL' message is returned if a user is logged in from an unknow IP address or if logged in from terminal.
# This plugin does not take any arguments.

from subprocess import PIPE,Popen
import sys

exit_status = 0
output = ''
allowed_list = ['41.74.76.92']

def get_out(output,exit_status):
	print output
	sys.exit(exit_status)

try:
	p1=Popen('who'.split(), stdout=PIPE)
	who_output = p1.communicate()[0]

	if len(who_output) <= 0:
		output = 'Ok: No users logged in'
		get_out(output, exit_status)
	else:
		for item in who_output.split('\n'):
			if len(item) <= 0 : continue
			user_details = list(item.split())
			if 'tty' in user_details[1]: #Terminal Login
				output += 'CRITICAL: User %s logged in from terminal since %s %s\n' % (user_details[0],user_details[2],user_details[3])
				exit_status = 2
			elif 'pts' in user_details[1]: #SSH Login
				ip = user_details[4].strip('(').strip(')')
				if ip not in allowed_list:
					output += 'CRITICAL: User %s logged in from %s since %s %s\n' % (user_details[0],ip,user_details[2],user_details[3])
					exit_status = 2
				else:
					output += 'NOTICE: User %s logged in from %s since %s %s\n' % (user_details[0],ip,user_details[2],user_details[3])
			else:
				output += 'Unable to parse command output'
				exit_status = 1
		get_out(output,exit_status)

except Exception,e:
	print e


