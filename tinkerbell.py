import os, sys, re, time, json, urllib, urllib2
import xml.dom.minidom

from Tinkerbell.common.out import _log
from Tinkerbell.core.m163 import m163
from Tinkerbell.core.appchina import appchina
from Tinkerbell.core.baidu import baidu
from Tinkerbell.core.dcn import dcn
from Tinkerbell.core.slideme import slideme

#---------------------------------------------------
# List of supported 3rd Party Unofficial Android Marketplaces
#---------------------------------------------------
MarketList = ["m.163.com", "appchina.com", "as.baidu.com", "d.cn", "slideme.org"]

def main(market):
    if market=="m.163.com":
        _log("[+] Downloading from %s in progress" % market)
        d = m163()
        d._download('http://m.163.com/android/category/allapp/index.html', 'http://m.163.com/android/category/allapp/all-download-')
        d._download('http://m.163.com/android/game/allgame/index.html', 'http://m.163.com/android/category/allgame/all-download-')
    elif market=="appchina.com":
        _log("[+] Downloading from %s in progress" % market)
        mappings = ["411", "413", "415", "416", "418","423"]
        for k in mappings:
            path = "http://www.appchina.com/category/" + k + ".html"
            download_url = "http://www.appchina.com/category/" + k + "/1_1_"
            d = appchina()
            d._download(path, download_url)
    elif market=="as.baidu.com":
        print("[+] Downloading from %s in progress" % market)
        mappings = {"software":"101", "asgame":"102"}
        download_url = "http://as.baidu.com/a/item?docid="
        for k, v in mappings.items():
            path = "http://as.baidu.com/a/" + k + "?cid=" + v + "&s=1"
            d = baidu()
            d._download(path, download_url)
    elif market=="d.cn":
        print("[+] Downloading from %s in progress" % market)
        mappings = [ "software","game" ]
        for k in mappings:
            path = "http://android.d.cn/" + k + "/"
            download_url = "http://android.d.cn/" + k + "/1/-1/-1/"
            d = dcn()
            d._download(path, download_url)
    elif market=="slideme.org":
        print("[+] Downloading from %s in progress" % market)
        d = slideme()
        d._download("http://slideme.org/", "http://slideme.org")
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        _log("[+] Usage: %s [marketplace]" % sys.argv[0])
        _log("[+] Some of the unofficial Android marketplace:")
        for market in MarketList:
            _log("    %s" % market)
        sys.exit(0)
    else:
        market = sys.argv[1]
        main(market)