from flask import Flask, redirect
import re
import time
import hashlib
import requests
import json
from datetime import datetime

app = Flask(__name__)

def md5sum(src):
    m = hashlib.md5()
    m.update(src.encode(encoding='utf-8'))
    return m.hexdigest()

def a_auth(uri, key, exp):
    p = re.compile("^(http://|https://)?([^/?]+)(/[^?]*)?(\\?.*)?$")
    if not p:
        return None
    m = p.match(uri)
    scheme, host, path, args = m.groups()
    if not scheme: scheme = "http://"
    if not path: path = "/"
    if not args: args = ""
    rand = "0"
    uid = "0"
    sstring = "%s-%s-%s-%s-%s" %(path, exp, rand, uid, key)
    hashvalue = md5sum(sstring)
    auth_key = "%s-%s-%s-%s" %(exp, rand, uid, hashvalue)
    if args:
        return "%s%s%s%s&auth_key=%s" %(scheme, host, path, args, auth_key)
    else:
        return "%s%s%s%s?auth_key=%s" %(scheme, host, path, args, auth_key)

@app.route('/zonghe')
def zonghe_redirect():
    uri = "http://zhonghe1.cdn.dingtoo.com/AppName/StreamName.m3u8"
    key = "pE2023hNjHc@#DRsp"
    exp = int(time.time()) + 1 * 3600
    authuri = a_auth(uri, key, exp)
    return redirect(authuri, code=302)

@app.route('/gonggong')
def gonggong_redirect():
    uri = "http://gonggong1.cdn.dingtoo.com/AppName/StreamName.m3u8"
    key = "pE2023hNjHc@#DRsp"
    exp = int(time.time()) + 1 * 3600
    authuri = a_auth(uri, key, exp)
    return redirect(authuri, code=302)

@app.route('/hbo_hk')
def now_hbo():
    hbo_url = "https://www.nowe.com/watch/115/HBO?type=channel"
    return redirect(getNoweM3u8(hbo_url), code=302)

@app.route('/now_news')
def now_news():
    url = "https://www.nowe.com/watch/332/Now-NEWS-Channel?type=channel"
    return redirect(getNoweM3u8(url), code=302)

@app.route('/now_business')
def now_business():
    url = "https://www.nowe.com/watch/333/Now-Business-News-Channel?type=channel"
    return redirect(getNoweM3u8(url), code=302)

@app.route('/viu')
def viu_redirect():
    return redirect(getViuM3u8(99), code=302)
    # return getViuM3u8(99)

@app.route('/viu_six')
def viu_six():
    return redirect(getViuM3u8(96), code=302)
    # return getViuM3u8(96)

def getViuM3u8(channel):
    post_json = {
        "callerReferenceNo": "20250228191258",
        "channelno": "096",
        "contentId": "096",
        "contentType": "Channel",
        "mode": "prod",
        "PIN": "password",
        "cookie": "4efee1eb7dda42acb0",
        "deviceId": "4efee1eb7dda42acb0",
        "deviceType": "ANDRIOD_WEB",
        "format": "HLS"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    url = "https://inhouse-stream.viu.tv/api"

    if channel == 96:
        post_json["channelno"] = "096"
        post_json["contentId"] = "096"
        post_json["callerReferenceNo"] = str(datetime.now().strftime('%Y%m%d%H%M%S'))
        response = requests.post(url, headers=headers, json=post_json).text
        response = json.loads(response)
        return response["asset"][0]
    if channel == 99:
        post_json["channelno"] = "099"
        post_json["contentId"] = "099"
        post_json["callerReferenceNo"] = str(datetime.now().strftime('%Y%m%d%H%M%S'))
        response = requests.post(url, headers=headers, json=post_json).text
        response = json.loads(response)
        return response["asset"][0]

def getNoweM3u8(url):
    response = requests.get(url)
    all_lines = response.text.splitlines()
    for line in all_lines:
        if 'index.m3u8' in line:
            m3u = line.lstrip('\t')
            m3u = m3u.replace('\\', '').replace(' ', '')
            url_pattern = r'"(https:\/\/[^\"]+)"'
            urls = re.findall(url_pattern, m3u)
            return urls[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10492)
