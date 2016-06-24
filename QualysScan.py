#!/usr/bin/python
#This is designed to scan a single IP address for remediation check, 
#Need to update the default scanner in the parser options if you choose
#Need to updated the defaultOptions variable with the ID of the scan template use.


import urllib2
import urllib
import base64
import getpass
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--target", dest="target", help="Target to scan (IP Address)" )
parser.add_option("-s", "--scanner", dest="scanner", default="ENTER DEFAULT SCANNER NAME", help="Scanner to use, default is ?")
parser.add_option("-n", "--name", dest="scanname", help="Name of the scan to run")
parser.add_option("-u", "--username", dest="username", help="QualysGuard Username will be prompted for password")

(opts, args) = parser.parse_args()
if not opts.target:
	parser.print_help()
	parser.error('Target IP address not provided')
elif not opts.scanname:
	parser.print_help()
	parser.error('Scan Name not provided')
elif not opts.username:
	parser.print_help()
	parser.error('Username not provided')

password = getpass.getpass()
base64string = base64.encodestring('%s:%s' % (opts.username, password))[:-1]

#update with scan template ID.
defaultOptions=ENTER SCAN TEMPLATE NUMBER
encodetitle = urllib.quote(opts.scanname)
uri = 'https://qualysapi.qualys.com/api/2.0/fo/scan/'
ScanOptions = 'action=launch&scan_title=%s&ip=%s&option_id=%s&iscanner_name=%s' %(encodetitle,opts.target,defaultOptions,opts.scanner)
encodedArgs = urllib.quote(ScanOptions)
headers = {'X-Requested-With':'QualysAPIConnect'}
req = urllib2.Request(uri,ScanOptions,headers)
req.add_header("Authorization", "Basic %s" % base64string)

print "Scan Options: Initial Options (Default) %d" %defaultOptions
try:
	result = urllib2.urlopen(req)
	print result.getcode()
except:
	print "Request Failed -- you did something wrong." 

