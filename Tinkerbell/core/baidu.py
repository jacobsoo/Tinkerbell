import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class baidu(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        
        d = curl()
        filename, download_html = d._curl(self.path)
        _number_pages = re.search('上五页.*?&amp;s=1&amp;pn=(.*?)">', download_html, re.DOTALL|re.UNICODE)
        try:
            os.makedirs('./Tinkerbell/downloads/baidu')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/baidu")
        for i in range(1, int(_number_pages.group(1))+1):
            page_html = self.path + "&pn=" + str(i)
            _log("[+] Downloading from " + page_html)
            filename, page_download_html = d._curl(page_html)
            found = re.findall('data-download_url="(.+?)"', page_download_html, re.DOTALL|re.UNICODE)
            package_names = re.findall('data-package="(.+?)"', page_download_html, re.DOTALL|re.UNICODE)
            j = 0
            for _apk_link in found:
                filename = package_names[j] + ".apk"
                _log("[+] Downloading " + _apk_link)
                j += 1
                d._download_apk(_apk_link, filename)
        os.chdir('../../../')