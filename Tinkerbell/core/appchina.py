import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class appchina(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        filename, download_html = d._curl(self.path)
        found = re.search('last"><a href="(.+?)" title="尾页', download_html, re.DOTALL)
        _number_pages = d._mid(found.group(1), "/category/411/1_1_", "_1")
        try:
            os.makedirs('./Tinkerbell/downloads/appchina')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/appchina")
        for i in range(1, int(_number_pages)+1):
            download_url = self.download_url + str(i) + "_1_0_0_0.html"
            _log("Downloading from %s" %download_url)
            filename, download_html = d._curl(download_url)
            found = re.findall("更多详情</a>.*?<a href='(.+?)' class=", download_html, re.DOTALL)
            for _apk_link in found:
                filename = os.path.basename(_apk_link)
                _download_name = filename.split("?", 1)
                d._download_apk(_apk_link, _download_name[0])
        os.chdir('../../../')