# coding = utf-8

import urllib2
import urllib
import cookielib
import zlib

cookie_file = './cookie.dat';
class PI(object):

    def __init__(self):
        self.infoUrl = "http://myteams/sites/srdbios/Web%20Stuff/AGESA-CIMX-BU%20Roadmaps.htm"
        self.loginUrl = "http://myteams/sites/srdbios"
        self.header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip,deflate,sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Authorization": "Negotiate TlRMTVNTUAADAAAAGAAYAH4AAAAeAR4BlgAAAAAAAABYAAAAEAAQAFgAAAAWABYAaAAAABAAEAC0AQAAFYKI4gYBsR0AAAAPmHUmLS2gfqXKh3dmxqTIm3kAbwB1AHoAaABhAG4AZwBZAE8AVQBaAEgAQQBOAEcALQBQAEMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFVasSFpp0ffthJSHFJ+pZQEBAAAAAAAAfU3rFmeczwHbCqIjz9xiVQAAAAACAAYAQQBNAEQAAQAYAEEAVQBTAE8AUwBTAEkARgBFAFAAMQAxAAQADgBhAG0AZAAuAGMAbwBtAAMAKABhAHUAcwBvAHMAcwBpAGYAZQBwADEAMQAuAGEAbQBkAC4AYwBvAG0ABQAOAGEAbQBkAC4AYwBvAG0ACAAwADAAAAAAAAAAAAAAAAAwAACJR23Dr5j/eJlehOgF5512YGUaxolONpTYP8spM3LRywoAEAAAAAAAAAAAAAAAAAAAAAAACQAoAEgAVABUAFAALwBtAHkAdABlAGEAbQBzAC4AYQBtAGQALgBjAG8AbQAAAAAAAAAAAFXhI/lSu5Fx8mTIv8Mrwzc=",
            "Connection": "keep-alive",
            'Host':"myteams",
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
        }
        self.cookie = cookielib.LWPCookieJar();
        cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
        opener = urllib2.build_opener (cookie_support)
        urllib2.install_opener (opener)

    def loginBIOS(self):
        data = {}
        try:
            req = urllib2.Request(self.loginUrl,'',self.header)
            PIReleasePag = urllib2.urlopen(req).read()
        except urllib2.HTTPError as http_error:
            print zlib.decompress(http_error.read(),30)
        return PIReleasePag


    def getPIReleasePage(self):
        PIReleasePage = urllib.urlopen(self.url).read()
        return PIReleasePage


    def getPIReleaseInfo(self, PIReleasePage):
        pass


    def sendMail(self, PIInfo):
        pass


if __name__ == "__main__":
    myPI = PI()
    myPI.loginBIOS()
    PIReleasePage = myPI.getPIReleasePage()
    PIInfo = myPI.getPIReleaseInfo(PIReleasePage)
    PI.sendMail(PIInfo)