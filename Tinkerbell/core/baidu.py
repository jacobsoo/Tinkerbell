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
        found = re.search('data-total=(.*?) data-pn=0', download_html, re.DOTALL|re.UNICODE)
        try:
            os.makedirs('./Tinkerbell/downloads/baidu')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/baidu")
        _number_pages = found.group(1)
        for i in range(1, int(_number_pages)+1):
            self.download_url = self.path + "&page_num=" +str(i)
            _log("Downloading from %s" %self.download_url)
            filename, download_html = d._curl(self.download_url)
            _download_links = re.findall('data_url="(.+?)"', download_html, re.DOTALL)
            _data_package = re.findall('data_package="(.+?)"', download_html, re.DOTALL)
            _data_versionname = re.findall('data_versionname="(.+?)"', download_html, re.DOTALL)
            for i in range(len(_download_links)):
                _download_name = _data_package[i] + "." + _data_versionname[i] + ".apk"
                d._download_apk(_download_links[i], _download_name)
        os.chdir('../../../')