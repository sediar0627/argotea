import hashlib
import json

def md5(hash):
    return hashlib.md5(hash.encode('utf-8')).hexdigest()

def leer_json(url):
    json_response = {}
    with open(url) as file: 
        json_response = json.load(file)
    return json_response