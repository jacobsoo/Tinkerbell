import re,os,urllib
from urllib2 import unquote

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class liqucn(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    # Not complete for yx
    def _download(self, path, download_url):
        self.path = path
        
        d = curl()
        filename, download_html = d._curl(self.path)
        _number_pages = re.findall('\.\.\.</a><a href=\'index_(.*?).shtml\'>', download_html, re.DOTALL|re.UNICODE)
        _number_pages = int(_number_pages[0])
        
        try:
            os.makedirs('./Tinkerbell/downloads/liqucn')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/liqucn")
        for i in range(_number_pages, 0, -1):
            page_url = "http://os-android.liqucn.com/rj/index_" + str(i) + ".shtml"
            filename, download_html = d._curl(page_url)
            _log("[+] Downloading from %s" % unquote(page_url))
            #found = re.findall('<li>[\r\n].*?<a href="http://os-android.liqucn.com/rj/(.*?).shtml"  class="pic" target="_blank"', download_html, re.DOTALL|re.UNICODE)
            found = re.findall('<li>\r\n            <a href="/rj/(.*?).shtml" class="pic" target="_blank">', download_html, re.DOTALL|re.UNICODE)
            for _link_num in found:
                _app_link = "http://os-android.liqucn.com/rj/" + _link_num + ".shtml"
                filename, download_html = d._curl(_app_link)
                found = re.search('高速下载</a></li>\r\n					     <li><a href="(.*?)" class="btn_normal"', download_html, re.DOTALL|re.UNICODE)
                if found is None:
                    print("[*] %s probably contained an invalid page." % _app_link)
                else:
                    _download_name = "unsure.apk"
                    _apk_link = found.group(1)
                    d._download_tgbus_apk(_apk_link, _download_name)
        os.chdir('../../../')
        