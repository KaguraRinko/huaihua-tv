from flask import Flask, redirect
import re
import time
import hashlib

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10492)
