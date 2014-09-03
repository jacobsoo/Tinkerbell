# -*- coding: utf-8 -*-
import re,os,sys,urllib, urllib2

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class aptoide(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None
        
    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        try:
            os.makedirs('./Tinkerbell/downloads/aptoide')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/aptoide")
        for offset in xrange(30,3000,30):
            values = {'type' : 'latest', 
                      'mature' : '0',
                      'offset' : offset }
            data = urllib.urlencode(values)
            req = urllib2.Request(self.path, data)
            response = urllib2.urlopen(req)
            download_html = response.read()
            if download_html:
                found = re.findall('<a class="item app" href="(.*?)">', download_html, re.DOTALL|re.UNICODE)
                for download_url in found:
                    _log("[+] Downloading from %s" % download_url)
                    szTokenize = download_url.split('/')
                    _apkID = szTokenize[len(szTokenize)-2]
                    download_url = "https://www.aptoide.com/webservices/2/getApkInfo/id:" + _apkID + "/json"
                    _log("[+] JSON file found in %s" % download_url)
                    filename, download_html = d._curl(download_url)
                    found = re.search('"path":"(.*?)","', download_html, re.DOTALL|re.UNICODE)
                    _apk_link = found.group(1)
                    szTokenize = _apk_link.split('/')
                    _download_name = szTokenize[len(szTokenize)-1]
                    d._download_apk(_apk_link, _download_name)
        os.chdir('../../../')