# coding = utf-8

import urllib2
import re
import os


emailToolPath = "C:\\Users\\youzhang\\Documents\\GitHub\\Miscellaneous\\tool\\sendEmail.exe"

programUpdateState = {
    "KV":0,
    "CZ":0,
    "KB":0,
    "ML":0,
    "NL":0,
    "AM":0
}


isDebug = 0

def traceLog(info,isDebug):
    if( isDebug ):
        print info

def sendMail(message):
    command = emailToolPath + " -s aussmtp.amd.com -f BVM_SYSTEM_SERVICE@amd.com"
    command += " -t you.zhang@amd.com"
    command += " -u \"BKDG update Info\" "
    command += " -m \"{0}\"".format(message)
    status = os.system(command)
    return status

def getLastVersion():
    lastUpdateDate = {}
    try:
        fd = open("LastUpdate.txt","r")
    except:
        traceLog("cannot open the file",isDebug)
        exit(1)
    content = fd.read()[0:-1]
    content = content.replace("\n"," : ")
    result = content.split(" : ")
    for i in range(0,len(result),2):
        lastUpdateDate[result[i]] = result[i+1]
    fd.close()
    os.system("del LastUpdate.txt")
    newLastUpdate = open("LastUpdate.txt","w")
    newLastUpdate.close()
    return lastUpdateDate


class BKDGPage(object):

    def __init__(self,program):
        self.url = "http://twiki.amd.com/twiki/bin/view/SIG/BKDG"
        self.programFeature = '{0}_bkdg_int.pdf" target="_top">Latest '.format(program)
        self.patten = re.compile(self.programFeature + '(.*)</a>' )

    #return web info
    def getPage(self):
        content = urllib2.urlopen(self.url).read()
        return content

    # return version updated
    def getBKDGState(self,content):
        startPos = content.index(self.programFeature)
        matchedItem = self.patten.match(content,startPos,startPos+100)
        presentUpdatedDate = matchedItem.groups()[0]
        return presentUpdatedDate

    def compareVersion(self,presentUpdatedDate,lastUpdateDate):
        if(presentUpdatedDate != lastUpdateDate[program]):
            return '1'
        else:
            return '0'

    def writeUpdateState(self,program,presentUpdatedDate):
        info = program + " : " + presentUpdatedDate + "\n"
        fd = open("LastUpdate.txt","a")
        fd.write(info)
        fd.close()


if __name__ == "__main__":
    message = ''
    lastUpdateDate = getLastVersion()
    myBKDGPage = BKDGPage('init')
    content = myBKDGPage.getPage()
    for program in programUpdateState.keys():
        myBKDGPage = BKDGPage(program)
        presentUpdatedDate = myBKDGPage.getBKDGState(content)
        isUpdated = myBKDGPage.compareVersion(presentUpdatedDate,lastUpdateDate)
        myBKDGPage.writeUpdateState(program,presentUpdatedDate)
        message = message + program + " : " + presentUpdatedDate + " : " + isUpdated + "\t"
    status = sendMail(message)
    print status



