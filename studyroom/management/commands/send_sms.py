import json
import hashlib
import hmac
import base64
import requests
import time

def	make_signature():
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    access_key = "{zJVQDuaiFBOu1DadNR1e}"				# access key id (from portal or Sub Account)
    secret_key = "{7sYz2qubCqVUGYEFuVSnrH491iayQGBUYT3migaE}"				# secret key (from portal or Sub Account)
    secret_key = bytes(secret_key, 'UTF-8')

    method = "GET"
    uri = "/photos/puppy.jpg?query1=&query2"

    message = method + " " + uri + "\n" + timestamp + "\n"  + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

sid = "ncp:sms:kr:280111225336:kizacademy"

sms_uri = "/sms/v2/services/{}/messages".format(sid)
sms_url = "https://sens.apigw.ntruss.com{}".format(sms_uri)
#sec_key = "{527ddd3e732c41b4a6eab0a249632471}"

acc_key_id = "{zJVQDuaiFBOu1DadNR1e}"
acc_sec_key = b'{7sYz2qubCqVUGYEFuVSnrH491iayQGBUYT3migaE}'

stime = int(float(time.time()) * 1000)

hash_str = "POST {}\n{}\n{}".format(sms_uri, stime, acc_key_id)

digest = hmac.new(acc_sec_key, msg=hash_str.encode('utf-8'), digestmod=hashlib.sha256).digest()
d_hash = base64.b64encode(digest).decode()
print(d_hash, make_signature())

from_no = "01020307777"
to_no = "01020307777"
message = "메세지 테스트"

msg_data = {
    'type': 'SMS',
    'countryCode': '82',
    'from': "{}".format(from_no),
    'contentType': 'COMM',
    'content': "{}".format(message),
    'messages': [{'to': "{}".format(to_no)}]
}

response = requests.post(
    sms_url, data=json.dumps(msg_data),
    headers={"Content-Type": "application/json; charset=utf-8",
             "x-ncp-apigw-timestamp": str(stime),
             "x-ncp-iam-access-key": acc_key_id,
             "x-ncp-apigw-signature-v2": d_hash
             }
)

print(response.text)