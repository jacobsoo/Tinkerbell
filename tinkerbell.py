import os, sys, re, time, json, urllib, urllib2
import xml.dom.minidom

from Tinkerbell.common.out import _log
from Tinkerbell.core.m163 import m163
from Tinkerbell.core.mm10086cn import mm10086cn
from Tinkerbell.core.appchina import appchina
from Tinkerbell.core.aptoide import aptoide
from Tinkerbell.core.baidu import baidu
from Tinkerbell.core.dcn import dcn
from Tinkerbell.core.coolapk import coolapk
from Tinkerbell.core.gfan import gfan
from Tinkerbell.core.liqucn import liqucn
from Tinkerbell.core.slideme import slideme
from Tinkerbell.core.tgbus import tgbus

#---------------------------------------------------
# List of supported 3rd Party Unofficial Android Marketplaces
#---------------------------------------------------
MarketList = ["m.163.com", "mm.10086.cn", "appchina.com", "aptoide.com", "as.baidu.com", "d.cn", "coolapk.com", "gfan.com", "liqucn.com", "slideme.org", "tgbus.com"]

def main(market):
    if market=="m.163.com":
        _log("[+] Downloading from %s in progress" % market)
        d = m163()
        d._download('http://m.163.com/android/category/allapp/index.html', 'http://m.163.com/android/category/allapp/all-download-')
        d._download('http://m.163.com/android/game/allgame/index.html', 'http://m.163.com/android/category/allgame/all-download-')
    elif market=="mm.10086.cn":
        _log("[+] Downloading from %s in progress" % market)
        d = mm10086cn()
        d._download('http://mm.10086.cn/android/software/qbrj?pay=1', 'http://mm.10086.cn/android/info/')
        d._download('http://mm.10086.cn/android/game/qbyx?pay=1', 'http://mm.10086.cn/android/info/')
    elif market=="aptoide.com":
        print("[+] Downloading from %s in progress" % market)
        mappings = [ "software","game" ]
        for k in mappings:
            path = "http://m.aptoide.com/phpajax/get_more_apps.php"
            download_url = "http://m.aptoide.com/phpajax/get_more_apps.php"
            d = aptoide()
            d._download(path, download_url)
    elif market=="appchina.com":
        _log("[+] Downloading from %s in progress" % market)
        mappings = ["301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "411", "412", "413", "414", "415", "416", "417", "418", "419", "420", "421", "422", "423", "424"]
        for k in mappings:
            path = "http://www.appchina.com/category/" + k + ".html"
            download_url = "http://www.appchina.com/category/" + k + "/"
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
    elif market=="coolapk.com":
        print("[+] Downloading from %s in progress" % market)
        mappings = [ "apk","game" ]
        for k in mappings:
            path = "http://www.coolapk.com/" + k + "/"
            download_url = "http://www.coolapk.com/" + k + "/?p="
            d = coolapk()
            d._download(path, download_url)
    elif market=="gfan.com":
        print("[+] Downloading from %s in progress" % market)
        mappings = [ "apps_7","games_8" ]
        for k in mappings:
            path = "http://apk.gfan.com/" + k + "_1_1.html"
            download_url = "http://apk.gfan.com/" + k
            d = gfan()
            d._download(path, download_url)
    elif market=="liqucn.com":
        d = liqucn()
        software_path = "http://os-android.liqucn.com/rj/"
        game_path = "http://os-android.liqucn.com/yx/"
        download_url = "index_"
        d._download(software_path, download_url)
    elif market=="slideme.org":
        print("[+] Downloading from %s in progress" % market)
        d = slideme()
        d._download("http://slideme.org/", "http://slideme.org")
    elif market=="tgbus.com":
        print("[+] Downloading from %s in progress" % market)
        mappings = [ "soft","game" ]
        for k in mappings:
            path = "http://a.tgbus.com/" + k + "/"
            download_url = "http://a.tgbus.com/" + k + "/"
            d = tgbus()
            d._download(path, download_url)
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
