#!/bin/sh
#
# check_ro_mounts
#
# Plugin for Nagios
# Written by A. Shibani (a@shumbashi.io)
# Last Modified: 12-May-2016
#
# Description:
#
# This plugin will check if any filesystems are mounted as read_only.
# This plugin does not take any arguments.
# set -x
STATE_OK=0
STATE_CRITICAL=2

for i in `grep ' ro,' /proc/mounts | awk '{ print $2 }'`
do
        P1=$(grep $i /etc/fstab)
        if [ -n "$P1" ]; then
                P2=$(grep -q '$i' /etc/fstab | awk '{ print $4 }' | grep 'ro')
                if [ -z "$P2" ]; then
                        MESSAGE="$i $MESSAGE";
                fi
        fi
done

if [ "$MESSAGE" ]
then
        echo "CRITICAL: Read-only filesystem: $MESSAGE"
        exit $STATE_CRITICAL
fi

echo "OK: No Read-Only filesystems"
exit $STATE_OK

