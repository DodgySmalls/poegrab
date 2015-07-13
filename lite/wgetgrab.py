from urllib2 import Request, urlopen, URLError, HTTPError, HTTPBasicAuthHandler, build_opener, install opener
import subprocess

url = ["http://pathofexile.com/item-data/weapon", "http://pathofexile.com/item-data/armour"]
data = ""

page = url[0]

try:
	f = urlopen(Request(page))
	data = f.read()
	f.close

except HTTPError, e:
	print "HTTP Error:", e.code, url
except URLError, e:
	print "URL Error:", e.reason, url

raw = "-source"
