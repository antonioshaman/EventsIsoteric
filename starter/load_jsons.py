from starter.other import load_json

def token():
    cc = load_json()
    token = cc["token"]
    return token

def adminid():
    cc = load_json()
    adminid = cc["adminid"]
    return adminid

def mpchannel():
    cc = load_json()
    private_key = cc["mpchannel"]
    return private_key

