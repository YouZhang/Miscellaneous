import urllib
import urllib2
import json
def lyl(a):
	url = "http://www.liantu.com/tiaoma/query.php"
	values = {"ean":a}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	s = json.loads(the_page)
	print "code:     " + s.get("ean","null")
	print "name:     " + s.get("name","null")
	print "country:  " + s.get("guobie","null")
	print "price:    " + str(s.get("price","null"))
	print "supplier: " + s.get("supplier","null")
	print "factory:  " + s.get("fac_name","null")
	print "status:   " + s.get("fac_status","null")
	print s["titleSrc"]
	print ""
	
	
lyl("6939354800469")
lyl("6917878002972")
lyl("6925785604585")