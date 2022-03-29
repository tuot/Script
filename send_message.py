

def console_log(msg):
    import requests
    try:
        url = "http://maker.ifttt.com/trigger/info/json/with/key/bycqDZ5Su_-VIDYHrAmxNG"
        resp = requests.post(url, timeout=10, json={"date": msg})
        print(resp.text)
    except:
        pass

import datetime
console_log(datetime.datetime.now().isoformat())
