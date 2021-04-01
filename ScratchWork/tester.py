import time
import requests

url = "http://127.0.0.1:5000/"
requests.put(url + "add", json = {"test":"init"})
tick = 0
while True:
    requests.post(url + "update", json = {"test":tick})
    tick = tick + 1
    time.sleep(1)

