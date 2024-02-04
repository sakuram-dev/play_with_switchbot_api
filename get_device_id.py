import time
import hashlib
import hmac
import base64
import uuid
import requests
import pprint
from dotenv import load_dotenv
import os

URL = "https://api.switch-bot.com/v1.1/devices"

def make_secret(secret_key):
    secret_key = bytes(secret_key, 'utf-8')
    return secret_key

def make_sign(secret_key, t, nonce):
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    sign = base64.b64encode(hmac.new(secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign

def make_t():
    t = int(round(time.time() * 1000))
    return str(t)

def make_nonce():
    nonce = str(uuid.uuid4())
    return nonce

# load .env and get secret_key and token
load_dotenv()
secret_key = os.getenv("SECRET_KEY")
token = os.getenv("TOKEN")

# make secret_key, t, nonce, sign
secret_key = make_secret(secret_key)
t = make_t()
nonce = make_nonce()
sign = make_sign(secret_key, t, nonce)

# make headers
headers = {
    "Authorization": token,
    "sign": sign,
    "t": t,
    "nonce": nonce,
    "Content-Type": "application/json; charset=utf-8"
}

# response
response = requests.get(URL, headers=headers)

pprint.pprint(response.json())
