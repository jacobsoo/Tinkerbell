import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class coolapk(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        filename, download_html = d._curl(self.path)
        found = re.search('p=2">&gt;</a></li><li><a href="/apk/\?p=(.+?)">最末页', download_html, re.DOTALL)
        if found is None:
            found = re.search('p=2">&gt;</a></li><li><a href="/game/\?p=(.+?)">最末页', download_html, re.DOTALL)
        try:
            os.makedirs('./Tinkerbell/downloads/coolapk')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/coolapk")
        _number_pages = found.group(1)
        print _number_pages
        for i in range(1, int(_number_pages)+1):
            new_download_url = self.download_url + str(i)
            _log("[+] Downloading from %s" % new_download_url)
            filename, download_html = d._curl(new_download_url)
            found = re.findall('<h4 class="media-heading"><a href="(.+?)"', download_html, re.DOTALL)
            for download_url in found:
                if download_url.endswith("/")==False:
                    download_url = "http://coolapk.com" + download_url
                    _log("[+] Downloading from %s" % download_url)
                    filename, download_html = d._curl(download_url)
                    found = re.search('var apkDownloadUrl = "(.+?)";', download_html, re.DOTALL)
                    _apk_link = found.group(1)
                    _download_name = d._mid(_apk_link, "/dl?pn=","&v=") + ".apk"
                    _apk_link = "http://coolapk.com" + _apk_link + '&extra=0:'
                    d._download_coolapk(_apk_link, _apk_link, _download_name)
        os.chdir('../../../')