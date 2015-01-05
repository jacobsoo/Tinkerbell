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
        found = re.findall('<li class="dis_writebg_a"><a href="/category/(.+?).html">', download_html, re.DOTALL|re.UNICODE)
        _num = found[6][4:]
        #_number_pages = d._mid(found.group(1), "/category/411/1_1_", "_1")
        number = _num.split('_')
        _number_pages = number[0]
        try:
            os.makedirs('./Tinkerbell/downloads/appchina')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/appchina")
        for i in range(1, int(_number_pages)+1):
            download_url = self.download_url + str(i) + "_1_1_3_0_0_0.html"
            _log("Downloading from %s" %download_url)
            filename, download_html = d._curl(download_url)
            found = re.findall('查看详情</a>.*?<a href="(.+?)" class=', download_html, re.DOTALL|re.UNICODE)
            name_found = re.findall('meta-packagename="(.+?)" meta-appid=', download_html, re.DOTALL|re.UNICODE)
            for _apk_link, _download_name in zip(found, name_found):
                _download_name = _download_name + ".apk"
                d._download_appchinaapk(_apk_link, _download_name)
        os.chdir('../../../')