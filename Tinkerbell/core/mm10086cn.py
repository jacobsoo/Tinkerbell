import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class mm10086cn(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        filename, download_html = d._curl(self.path)
        
        found = re.search('总共：(.*?)</span>', download_html, re.DOTALL|re.UNICODE)
        try:
            os.makedirs('./Tinkerbell/downloads/mm10086cn')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/mm10086cn")
        _number_pages = found.group(1)
        for i in range(1, int(_number_pages)+1):
            for j in range(1,3):
                page_url = path + '&p=' + str(i) + '&screen=' + str(j)
                _log("[+] Scraping from %s" % page_url)
                filename, download_html = d._curl(page_url)
                found = re.findall('href="/download/android/(.*?)" target="', download_html, re.DOTALL|re.UNICODE)
                for new_download_url in found:
                    _apk_link = "http://mm.10086.cn/download/android/" + new_download_url
                    _download_name = "unsure.apk"
                    _log("[+] Downloading from %s" % _apk_link)
                    d._download_tgbus_apk(_apk_link, _download_name)
        os.chdir('../../../')