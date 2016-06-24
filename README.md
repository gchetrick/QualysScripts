ExcludeFindings.rb
This script is designed to take findings and exclude them by managing the ticket created in qualys. It will take one IP, one QID and one Comment. If you want to close a batch of them, then you can loop it at the command line with a file full of IPs

for i in `cat ips.txt`;do;./ExcludeFindings.rb -i $i -q 12345 -c "Ticket #1234";done

QualysAssetGroups.py
This script is designed to pull the assets that are defined in an asset group and compare them to what has actually been scanned giving a list of IPS that are not being scanned, this is only useful if you are defining a static list of IPs to scan instead of just scanning a range.

QualysScan.py
This script is desinged to quickly re-scan a singe asset. I used this a lot when a team was working on patching and wanted me to rescan one device to see if it had been fixed.

In the script a default scanner will need to be defined if you don't define one at the command line. Line 15

Also need to enter a scan template number at line 34

Enjoy!
