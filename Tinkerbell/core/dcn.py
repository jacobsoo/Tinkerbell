import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class dcn(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        filename, download_html = d._curl(self.path)
        found = re.search('下一页</a><a href="http://android.d.cn/game/1/-1/-1/(.+?)/"', download_html, re.DOTALL|re.UNICODE)
        if found is None:
            found = re.search('下一页</a><a href="http://android.d.cn/software/1/-1/-1/(.+?)/"', download_html, re.DOTALL|re.UNICODE)
        try:
            os.makedirs('./Tinkerbell/downloads/dcn')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/dcn")
        _number_pages = found.group(1)
        for i in range(1, int(_number_pages)+1):
            self.download_url = self.download_url + str(i) + "/"
            _log("Downloading from %s" %self.download_url)
            filename, download_html = d._curl(self.download_url)
            found = re.findall('</p>.*?<a href="(.+?)"', download_html, re.DOTALL)
            for download_url in found:
                if download_url.endswith(".html")==True and download_url.startswith(self.path):
                    filename, download_html = d._curl(download_url)
                    found = re.search('downbtn downbtn1">.*?<a href="(.+?)" class="btn-down"', download_html, re.DOTALL)
                    _apk_link = found.group(1)
                    if _apk_link=="":
                        _log("File from %s not found" % download_url)
                    else:
                        if filename=="":
                            filename = os.path.basename(_apk_link[:-8])
                        d._download_apk(_apk_link, filename)
        os.chdir('../../../')