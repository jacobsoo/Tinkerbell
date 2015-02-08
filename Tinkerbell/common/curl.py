import urllib, urllib2, time, os, socket
import xml.dom.minidom

from Tinkerbell.common.out import _log

class MyException(Exception):
    pass
    
class curl:
    def __init__(self):
        self.name = None
        self.path = None
        self.cookie = None

    #---------------------------------------------------
    # _curl : Grab the file based on url
    #---------------------------------------------------
    def _curl(self, url, **httpheaders):
        retry = 3
        while retry > 0:
            try:
                return self._do_curl(url, **httpheaders)
            except StandardError:
                _log('[-] Retry...')
            retry = retry - 1
        _log('[-] Failed after retry %d times.' % retry)
        return ("","")
        #raise StandardError('[-] Failed after retry %d times.' % retry)

    #---------------------------------------------------
    # _do_curl : Grab the file contents based on url
    #            Function will return filename and file contents
    #---------------------------------------------------
    def _do_curl(self, url, **httpheaders):
        #' get html text from url. '
        headers = {
                #'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
                'Referer': url
        }
        headers.update(httpheaders)
        req = urllib2.Request(url, None, headers)
        resp = urllib2.urlopen(req)
        self.cookie = resp.headers.get('Set-Cookie')
        content_length = resp.headers.get('Content-Length')
        filename = ""
        if resp.headers.get('Content-Disposition') is None:
            filename = ""
        else:
            filename = _mid(resp.headers.get('Content-Disposition'), 'filename="','"')
        data = resp.read()
        if data is None:
            _log('[*] No download provided.')
            return ''
        return (filename, data)

    #---------------------------------------------------
    # _mid : find substring by start and end.
    #        >>> _mid('some text <h1>header</h1> end...', '<h1>', '</h1>')
    #        It will return 'header'
    #---------------------------------------------------
    def _mid(self, s, start, end):
        n1 = s.find(start)
        if n1 == (-1):
            return u''
        n2 = s.find(end, n1 + len(start))
        if n2 == (-1):
            return u''
        return s[n1 + len(start) : n2]

    #---------------------------------------------------
    # _download_apk : Downloading of .apk file
    #---------------------------------------------------
    def _download_apk(self, url, basename):
        print("[+] Downloading .apk file from %s" % url)
        filename, apk = self._curl(url)
        if filename=="":
            dest_name = basename
        else:
            # the following code is added because of m.163.com
            filename = urllib.unquote(filename).decode('utf8') 
            dest_name = filename
        if apk !="":
            with open(dest_name, 'wb') as fw:
                fw.write(apk)
            _log('[+] Download ok: %s' % basename)
            time.sleep(10)
        else:
            _log('[*] Download failed.')
            
    #---------------------------------------------------
    # _download_apk : Downloading of .apk file
    #---------------------------------------------------
    def _download_gfan_apk(self, url, basename):
        print("[+] Downloading .apk file from %s" % url)
        filename, apk = self._curl(url)
        if filename=="":
            filename = urllib.unquote(basename).decode('utf8') 
            dest_name = filename
        else:
            filename = urllib.unquote(filename).decode('utf8') 
            dest_name = filename
        if apk !="":
            with open(dest_name, 'wb') as fw:
                fw.write(apk)
            _log('[+] Download ok: %s' % basename)
            time.sleep(10)
        else:
            _log('[*] Download failed.')
            
    #---------------------------------------------------
    # _download_apk : Downloading of .apk file from appchina.com
    #---------------------------------------------------
    def _download_appchinaapk(self, url, basename, **httpheaders):
        print("[+] Downloading .apk file from %s" % url)
        tmp = ""
        
        #' get html text from url. '
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
        }
        headers.update(httpheaders)
        req = urllib2.Request(url, None, headers)
        resp = urllib2.urlopen(req)
        content_length = resp.headers.get('Content-Length')
        data = resp.read()
        dest_name = str(basename)
        if data is None:
            _log('[*] No download provided.')
        else:
            with open(dest_name, 'wb') as fw:
                fw.write(data)
            _log('[+] Download ok: %s' % dest_name)
            time.sleep(10)

    #---------------------------------------------------
    # _download_apk : Downloading of .apk file from tgbus.com
    #---------------------------------------------------
    def _download_tgbus_apk(self, url, basename, **httpheaders):
        print("[+] Downloading .apk file from %s" % url)
        
        #' get html text from url. '
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
        }
        headers.update(httpheaders)
        req = urllib2.Request(url, None, headers)
        resp = urllib2.urlopen(req)
        re302 = resp.geturl()
        
        filename = ""
        filename = urllib.unquote(os.path.basename(re302)).decode('utf8')
        dest_name = filename
        data = resp.read()
        
        if data is None:
            _log('[*] No download provided.')
        else:
            with open(dest_name, 'wb') as fw:
                fw.write(data)
            _log('[+] Download ok: %s' % os.path.basename(re302))
            time.sleep(10)

    #---------------------------------------------------
    # _download_apk : Downloading of .apk file from coolapk.com
    #---------------------------------------------------
    def _download_coolapk(self, url, referer, basename, **httpheaders):
        print("[+] Downloading .apk file from %s" % url)
        
        #' get html text from url. '
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
                'Referer': referer,
                'Host': 'www.coolapk.com',
                'cookie': self.cookie,
                'Connection': 'keep-alive'
        }
        headers.update(httpheaders)
        req = urllib2.Request(url, None, headers)
        try:
            resp = urllib2.urlopen(req, timeout = 10)
            content_length = resp.headers.get('Content-Length')
            filename = ""
            if resp.headers.get('Content-Disposition') is None:
                filename = ""
            else:
                tmp = self._mid(resp.headers.get('Content-Disposition'), 'filename="','"')
                filename = urllib.unquote(tmp).decode('utf8') 
            data = resp.read()
            if filename=="":
                dest_name = str(basename)
            else:
                dest_name = filename
            if data is None:
                _log('[*] No download provided.')
            else:
                with open(dest_name, 'wb') as fw:
                    fw.write(data)
                _log('[+] Download ok: %s' % basename)
                time.sleep(10)
        except urllib2.HTTPError, e:
            _log("There was an error: %s" % e)
        