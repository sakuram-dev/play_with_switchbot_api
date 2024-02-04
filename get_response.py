import time
import hashlib
import hmac
import base64
import uuid
import sys
import requests
from dotenv import load_dotenv
import os

def make_secret(secret_key):
    secret_key = bytes(secret_key, 'utf-8')
    return secret_key

def make_sign(secret_key, t, nonce):
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    sign = base64.b64encode(hmac.new(secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign

def make_t():
    return str(int(round(time.time() * 1000)))

def make_nonce():
    return str(uuid.uuid4())

def get_key():
    return sys.argv[1]

def get_device_id():
    return sys.argv[2]

def get_value(response, key):
    if response.status_code == 200:
        data = response.json()
        value = data["body"].get(key)
        if value is not None:
            if key in ["voltage", "weight", "electricCurrent", "temperature"]:
                value = float(value)
            elif key in ["electricityOfDay", "battery", "humidity"]:
                value = int(value)
            else:
                value = str(value)
        else:
            value = 0
        return value
    else:
        return 0

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
token = os.getenv("TOKEN")

key = get_key()
device_id = get_device_id()

secret_key = make_secret(secret_key)
t = make_t()
nonce = make_nonce()
sign = make_sign(secret_key, t, nonce)

url = "https://api.switch-bot.com/v1.1/devices/{}/status".format(device_id)

headers = {
    "Authorization": token,
    "sign": sign,
    "t": t,
    "nonce": nonce,
    "Content-Type": "application/json; charset=utf-8"
}

response = requests.get(url, headers=headers)

print(get_value(response, key))
