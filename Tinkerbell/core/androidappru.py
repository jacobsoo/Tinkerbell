import re,os,urllib
from urllib2 import unquote

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class androidappru(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    # Not complete for yx
    def _download(self, path, category, download_url):
        self.path = path
        self.category = category
        self.download_url = download_url
        
        d = curl()
        location = self.path + self.category + "/"
        filename, download_html = d._curl(location)
        szSearch = '"nav_ext">...</span> <a href="'+self.path+ self.category+'/page/(.*?)/">.*?</a></span> <span class="nnext">'
        _number_pages = re.search(szSearch, download_html, re.DOTALL|re.UNICODE)
        _number_pages = int(_number_pages.group(1))
        try:
            os.makedirs('./Tinkerbell/downloads/androidappru')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/androidappru")
        for i in range(1, _number_pages+1):
            page_url = location + "page/" + str(i) + "/"
            filename, download_html = d._curl(page_url)
            _log("[+] Downloading from %s" % unquote(page_url))
            found = re.findall('class="argmore"><a href="(.*?)"><b>', download_html, re.DOTALL|re.UNICODE)
            for _link_num in found:
                _log("[+] Retrieving .apk link from %s" % _link_num)
                filename, download_html = d._curl(_link_num)
                found = re.search('class="attachment"><a href="(.*?)" >', download_html, re.DOTALL|re.UNICODE)
                _download_name = re.search('class="attachment"><a href=".*?" >(.*?)</a> \[', download_html, re.DOTALL|re.UNICODE)
                _download_name = _download_name.group(1)
                if found is None:
                    print("[*] %s probably contained an invalid page." % _app_link)
                else:
                    _log("[+] Downloading from %s" % found.group(1))
                    _apk_link = found.group(1)
                    d._download_appchinaapk(_apk_link, _download_name)
        os.chdir('../../../')
        