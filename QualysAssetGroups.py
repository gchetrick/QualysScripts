#!/usr/bin/python
#This is designed to take the name of an asset group, then compare it to the assets actually scanned by that gropu and give a list of the assets that are being missed.

import urllib2
import urllib
import base64
import getpass
import re
from bs4 import BeautifulSoup as Soup
from optparse import OptionParser

def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []

   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))

   return ip_range

def fetchresults(uri,options,auth):
        headers = {'X-Requested-With':'QualysAPIConnect'}
        req = urllib2.Request(uri,options,headers)
        req.add_header("Authorization", "Basic %s" % auth)

        result = urllib2.urlopen(req)
        xmlfetch = Soup(result.read(), features="xml")

        return xmlfetch


parser = OptionParser()
parser.add_option("-a", "--assetgroup", dest="assetgroup", help="Name of the assetgroup to fetch" )
parser.add_option("-u", "--username", dest="username", help="QualysGuard Username will be prompted for password")

(opts, args) = parser.parse_args()
if not opts.assetgroup:
        parser.print_help()
        parser.error('Asset Group not defined')
elif not opts.username:
	parser.print_help()
	parser.error('Username not defined')

password = getpass.getpass()
base64string = base64.encodestring('%s:%s' % (opts.username, password))[:-1]

encodedassetgroup = urllib.quote_plus(opts.assetgroup)
GroupOptions = 'action=list&ag_titles=%s&truncation_limit=0 ' %(encodedassetgroup)
v1GroupOptions = 'title=%s' %(encodedassetgroup)
#liveassets are the assets that have been scanned
liveassets = fetchresults('https://qualysapi.qualys.com//api/2.0/fo/asset/host/',GroupOptions,base64string)
#fixed assets are a list of the raw assets defined in the asset group provided.
fixedassets = fetchresults('https://qualysapi.qualys.com/msp/asset_group_list.php',v1GroupOptions,base64string)
excludedassets = fetchresults('https://qualysapi.qualys.com//api/2.0/fo/asset/excluded_ip/','action=list',base64string)

scannedassets = set()
definedassets = set()
excludedset = set()
missingips = set()
for host in liveassets.find_all('HOST'):
        #print host.IP.string + "," + host.DNS.string
        print host.IP.string
        scannedassets.add(host.IP.string)

for ips in fixedassets.find_all('IP'):
        pattern = re.search('-',ips.string)
        if pattern is not None:
                #print ips.string
                startip,endip = ips.string.split('-')
                fulliplist = ipRange(startip,endip)
                for ip in fulliplist:
                        definedassets.add(ip)
                        print ip
        else:
                        definedassets.add(ips.string)
for ip in excludedassets.find_all('IP'):
        excludedset.add(ip)
for range in excludedassets.find_all('IP_RANGE'):
        startip,endip = range.string.split('-')
        iplist = ipRange(startip,endip)
        for ip in iplist:
                excludedset.add(ip)
#compare the sets
for missing in (definedassets - scannedassets):
        missingips.add(missing)
        print missing

