

def console_log(msg):
    import requests
    try:
        url = "http://maker.ifttt.com/trigger/info/with/key/bivMZhzWma1qDVu6HlnQ54"
        resp = requests.post(url, timeout=10, json={"value1": msg})
        print(resp.text)
    except:
        pass

import datetime
console_log(datetime.datetime.now().isoformat())
