#
# Regular cron jobs for the openvpnathome package
#
0 4	* * *	root	[ -x /usr/bin/openvpnathome_maintenance ] && /usr/bin/openvpnathome_maintenance
