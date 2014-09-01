# -*- coding: utf-8 -*-
import re,os,sys

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class gfan(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        filename, download_html = d._curl(self.path)
        found = re.search('下一页</a></li>.*?<li class="pre"><a href="/apps_7_1_(.*?).html" title="', download_html, re.DOTALL|re.UNICODE)
        if found is None:
            found = re.search('下一页</a></li>.*?<li class="pre"><a href="/games_8_1_(.*?).html" title="', download_html, re.DOTALL|re.UNICODE)
            appType = "2"
        else:
            appType = "1"
        try:
            os.makedirs('./Tinkerbell/downloads/gfan')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/gfan")
        _number_pages = found.group(1)
        for i in range(1, int(_number_pages)+1):
            new_download_url = self.download_url + "_1_" + str(i) + ".html"
            _log("Downloading from %s" % new_download_url)
            filename, download_html = d._curl(new_download_url)
            found = re.findall('apphot-tit"> <a href="(.+?)"', download_html, re.DOTALL)
            for download_url in found:
                if download_url.endswith(".html")==True:
                    download_url = "http://apk.gfan.com" + download_url
                    filename, download_html = d._curl(download_url)
                    found = re.search('http://api.gfan.com/market/api/apk\?(.+?)"', download_html, re.DOTALL|re.UNICODE)
                    _apk_link = found.group(1)
                    _apk_link = "http://api.gfan.com/market/api/apk?" + _apk_link                    
                    found = re.search('<h4 class="curr-tit">(.+?)</h4>', download_html, re.DOTALL|re.UNICODE)
                    _download_name = repr(found.group(1).decode('utf-8')).replace('\'','') + ".apk"
                    _download_name = _download_name.replace('u\\','').replace('\\','')
                    filename, download_html = d._curl(_apk_link)
                    d._download_apk(_apk_link, _download_name)
        os.chdir('../../../')