import re,os

from Tinkerbell.common.out import _log
from Tinkerbell.common.curl import curl

class slideme(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        self.download_url = download_url
        
        d = curl()
        try:
            os.makedirs('./Tinkerbell/downloads/slideme')
        except OSError:
            pass
        os.chdir("./Tinkerbell/downloads/slideme")
        for i in range(1, 9248141):
            download_url = self.path + "sam6.apk?adl=" + str(i)
            d._download_apk(download_url, i)
        os.chdir('../../../')