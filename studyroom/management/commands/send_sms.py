import hashlib, hmac, base64, requests, time, json

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

url = "https://sens.apigw.ntruss.com"
requesturl = "/sms/v2/services/"
requesturl2 = "/messages"
serviceId = "ncp:sms:kr:280111225336:kizacademy"
access_key = "u7iWiSot4GroFoDFlRO9"

uri = requesturl + serviceId + requesturl2
apiurl = url + uri

def	make_signature(uri, access_key):
    secret_key = "CUTZCnwo0BG636w69wFgD60Jwd9kBUXjC683SXHn"				# secret key (from portal or Sub Account)
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n"	+ access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

messages = {"to":"01020307777"}
body = {
    "type" : "SMS",
    "contentType" : "COMM",
    "from" : "01020307777",
    "subject" : "subject",
    "content" : "문자 발송 테스트",
    "messages" : [messages]
}

body2 = json.dumps(body)
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "x-ncp-apigw-timestamp": timestamp,
    "x-ncp-iam-access-key": access_key,
    "x-ncp-apigw-signature-v2": make_signature(uri, access_key)
}

res = requests.post(apiurl, headers=headers, data = body2)

print(res.text)