import json
import urllib
import urllib.request
import requests
import time
from urllib.error import HTTPError

__bpapicache = {
}
__userinfo = {
    "key" : "",
    "caching" : True
}
cacheRefresh = 30

def __RaiseError(errortype, reason=None):
    if errortype is "404":
        print("\n\nForbidden! Did you try settng your key?\nError Raised: " + reason)
    if errortype is "invalidarg":
        print("\n\nInvalid Argument!\nError Raised: " + reason)
    if errortype is "invalidsession":
        print("\n\nSession is invalid! Error raised: " + reason)
def bpinit(keytext, enableCache=True):
    # Setting enableCash to false is not recommended because it increases latency.
    __userinfo["key"] = keytext
    __userinfo["caching"] = enableCache
 
def allcurrencies(itemtype=None):
    global cacheRefresh
    global __bpapicache     
    if __userinfo["caching"] == True:
        if 'allcurrencies' in __bpapicache:
            ts = time.time()
            if ts - __bpapicache['allcurrencies']['timestamp'] <= cacheRefresh:
                return __bpapicache['allcurrencies']
    try:
        with urllib.request.urlopen(f'https://backpack.tf/api/IGetCurrencies/v1?key={__userinfo["key"]}') as f:
            returnstring = json.load(f)
            ts = time.time()
            if __userinfo["caching"] == True:
                if 'allcurrencies' not in __bpapicache:
                    __bpapicache['allcurrencies'] = returnstring
                    __bpapicache['allcurrencies']['timestamp'] = ts
                    return __bpapicache['allcurrencies']
                elif __bpapicache['allcurrencies']['timestamp'] > cacheRefresh:
                    __bpapicache['allcurrencies'] = returnstring
                    __bpapicache['allcurrencies']['timestamp'] = ts
                    return __bpapicache['allcurrencies']
            elif __userinfo["caching"] == False:
                return returnstring
    except HTTPError:
        __RaiseError("404", "allCurrencies() retrieved a 404.")
        return
def metalValue():
    global cacheRefresh
    global __bpapicache
    if __userinfo["caching"] == True:
        if 'Refined Metal' in __bpapicache:
            ts = time.time()
            if ts - __bpapicache["Refined Metal"]["timestamp"] <= cacheRefresh:
                return __bpapicache["Refined Metal"]
    try:
        with urllib.request.urlopen(f'https://backpack.tf/api/IGetCurrencies/v1?key={__userinfo["key"]}') as f:
            ts = time.time()
            returnstring = json.load(f)
            returndict = {
                "name" : returnstring["response"]["currencies"]["metal"]["name"],
                "value" : returnstring["response"]["currencies"]["metal"]["price"]["value"],
                "currency" : "usd"
            }
            if __userinfo["caching"] == True:
                if returndict["name"] not in __bpapicache:
                    __bpapicache[returndict["name"]] = {
                        "name" : returnstring["response"]["currencies"]["metal"]["name"],
                        "value" : returnstring["response"]["currencies"]["metal"]["price"]["value"],
                        "currency" : "usd",
                        "timestamp" : ts
                    }
                elif ts - __bpapicache[returndict["name"]]["timestamp"] > cacheRefresh:
                    __bpapicache[returndict["name"]] = {
                        "name" : returnstring["response"]["currencies"]["metal"]["name"],
                        "value" : returnstring["response"]["currencies"]["metal"]["price"]["value"],
                        "currency" : "usd",
                        "timestamp" : ts
                    }
            return returndict
    except HTTPError:
        __RaiseError("404", "metalValue() retrieved a 404.")
        return
def keyValue():
    # The name 'Mann Co. Supply Crate Key' has been shorten down to "Mann Co. Key" for simplicity
    global cacheRefresh
    if __userinfo["caching"] == True:
        if "Mann Co. Key" in __bpapicache:
            ts = time.time()
            if ts - __bpapicache["Mann Co. Key"]["timestamp"] <= 30:
                return __bpapicache["Mann Co. Key"] 
    try:
        with urllib.request.urlopen(f'https://backpack.tf/api/IGetCurrencies/v1?key={__userinfo["key"]}') as f:
            returnstring = json.load(f)
            returndict = {
                "name" : returnstring["response"]["currencies"]["keys"]["name"],
                "value" : returnstring["response"]["currencies"]["keys"]["price"]["value"],
                "currency" : returnstring["response"]["currencies"]["keys"]["price"]["currency"]
            }
            if __userinfo["caching"] == True:
                ts = time.time()
                if "Mann Co. Key" not in __bpapicache:
                    __bpapicache["Mann Co. Key"] = {
                        "name" : returnstring["response"]["currencies"]["keys"]["name"],
                        "value" : returnstring["response"]["currencies"]["keys"]["price"]["value"],
                        "currency" : returnstring["response"]["currencies"]["keys"]["price"]["currency"],
                        "timestamp" : ts
                    }
                elif ts - __bpapicache["Mann Co. Key"]["timestamp"] > 30:
                    __bpapicache["Mann Co. Key"] = {
                        "name" : returnstring["response"]["currencies"]["keys"]["name"],
                        "value" : returnstring["response"]["currencies"]["keys"]["price"]["value"],
                        "currency" : returnstring["response"]["currencies"]["keys"]["price"]["currency"],
                        "timestamp" : ts
                    }
            return returndict
    except HTTPError:
        __RaiseError("404", "keyValue() retrieved a 404.")
        return
def getUser (id=None):
    if id is None:
        return __RaiseError("invalidarg", "getUser() is missing required fields")
    with urllib.request.urlopen(f'https://backpack.tf/api/users/info/v1?steamids={id}&key={__userinfo["key"]}') as f:
        returndict = json.load(f)
        return returndict
def scrap (amount):
    scrapdict = {}
    scrapdict['weapons'] = amount*2
    scrapdict['reclaimed'] = round(amount/3, 2)
    scrapdict['refined'] = round(amount/9, 2)
    return scrapdict
def reclaimed(amount):
    recdict = {}
    recdict['weapons'] = amount*3*2
    recdict['scrap'] = amount*3
    recdict['refined'] = round(amount/3, 2)
    return recdict
def refined(amount):
    refdict = {}
    refdict['weapons'] = amount*3*3*2
    refdict['scrap'] = amount*3*3
    refdict['reclaimed'] = amount*3
    return refdict
def cacheDump (typethingy=None):
    if typethingy is None:
        typethingy = 'keys'
    if typethingy is 'raw':
        return __bpapicache
    elif typethingy is 'keys':
        keylist = []
        for i in __bpapicache.keys():
            keylist.append(i)
        return keylist