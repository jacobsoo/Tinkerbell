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
        mappings = {"501","502","503","504","505","506","507","508","509","510"}
        download_url = "http://shouji.baidu.com/software/list?cid="
        for k in mappings:
            path = "http://shouji.baidu.com/software/list?cid=" + k
            d = baidu()
            d._download(path, download_url)
        game_mappings = {"401","402","403","404","405","406","407","408"}
        game_download_url = "http://shouji.baidu.com/game/list?cid="
        for k in game_mappings:
            path = "http://shouji.baidu.com/game/list?cid=" + k
            d = baidu()
            d._download(path, game_download_url)
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