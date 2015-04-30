import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class mumayi(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.category = None

    def _download(self, path, category, download_url):
        self.path = path
        self.category = category
        self.download_url = download_url
        
        d = curl()
        filename, download_html = d._curl(self.path)
        szSearchString = '下一页</a><a href="http://www.mumayi.com/android/'+self.category+'/list_(.*?).html">末页</a>'
        found = re.search(szSearchString, download_html, re.DOTALL|re.UNICODE)
        _number_pages = found.group(1).split('_')
        
        try:
            os.makedirs('./Tinkerbell/downloads/mumayi')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/mumayi")
        
        #_log(int(_number_pages[1]))
        for i in range(1, int(_number_pages[1])+1):
            new_download_url = self.path + "/list_" + _number_pages[0] + "_" + str(i) + ".html"
            _log("[+] Downloading from %s" % new_download_url)
            filename, download_html = d._curl(new_download_url)
            
            found = re.findall('<i></i></a><a href="http://www.mumayi.com/android-(.*?).html" title="', download_html, re.DOTALL|re.UNICODE)
            for download_url in found:
                #_log("[+] Downloading from %s.html" % download_url)
                app_url = "http://www.mumayi.com/android-" + download_url + ".html"
                filename, download_html = d._curl(app_url)
                found = re.search('iappname hidden fl" >(.*?) </h1>', download_html, re.DOTALL)
                _apk_link = "http://down.mumayi.com/" + download_url
                _download_name = "unsure.apk"
                d._download_tgbus_apk(_apk_link, _download_name)
        os.chdir('../../../')