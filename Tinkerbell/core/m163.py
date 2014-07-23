import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class m163(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        
        d = curl()
        filename, download_html = d._curl(self.path)
        _number_pages = re.search('yui3-appsview-page-ellipsis">.*?</span>.*?<a  title="第(.+?)页"', download_html, re.DOTALL)
        try:
            os.makedirs('./Tinkerbell/downloads/m163')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/m163")
        for i in range(1, int(_number_pages.group(1))+1):
            self.download_url = download_url + str(i) + ".html"
            _log("Downloading from %s" %self.download_url)
            filename, download_html = d._curl(self.download_url)
            found = re.findall('m-t5">.*?<a href="(.+?)"', download_html, re.DOTALL)
            for _apk_link in found:
                filename = os.path.basename(_apk_link)
                #_log(_apk_link)
                filename = re.findall('%2Ffile.m.163.com%2Fapp%2Ffree%2F.*?%2F.*?%2F(.+?).apk', filename, re.DOTALL)
                _download_name = filename[0] + ".apk"
                d._download_apk(_apk_link,_download_name)
        os.chdir('../../../')