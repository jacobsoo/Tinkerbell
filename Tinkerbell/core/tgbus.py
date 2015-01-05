import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class tgbus(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        filename, download_html = d._curl(self.path)
        found = re.search('下页</a><a href="http://a.tgbus.com/soft/(.+?)/"', download_html, re.DOTALL)
        if found is None:
            found = re.search('下页</a><a href="http://a.tgbus.com/game/(.+?)/"', download_html, re.DOTALL)
        try:
            os.makedirs('./Tinkerbell/downloads/tgbus')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/tgbus")
        _number_pages = found.group(1)
        for i in range(1, int(_number_pages)+1):
            new_download_url = self.download_url + str(i) + "/"
            _log("[+] Downloading from %s" % new_download_url)
            filename, download_html = d._curl(new_download_url)
            found = re.findall('<b><a href="http://a.tgbus.com/soft/item-(.+?)/"', download_html, re.DOTALL)
            for download_url in found:
                download_url_link = "http://a.tgbus.com/soft/item-" + download_url
                _log("[+] Downloading from %s" % download_url_link)
                filename, download_html = d._curl(download_url_link)
                query = 'http://a.tgbus.com/download/' + download_url + '/(.+?)" target="_blank" title="'
                found = re.search(query, download_html, re.DOTALL)
                _apk_link = 'http://a.tgbus.com/download/' + download_url + "/" + found.group(1)
                found = re.search('您当前正在：<b>(.+?)</b></div>', download_html, re.DOTALL)
                _download_name = download_url + ".apk"
                d._download_tgbus_apk(_apk_link, _download_name)
        os.chdir('../../../')