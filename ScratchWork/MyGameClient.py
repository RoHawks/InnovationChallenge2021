import requests
host = True
username = ""
host_url = "https://rohawks.com/PostHostJoints"
user_url = "https://rohawks.com/PostUserJoints"
from SkeletonGrabber import Control

cam = Control()
if host == True:
    while True:
        joints = cam.getangles()
        payload = {"Joints": joints}
        requests.post(host_url, payload)
else:
    while True:
        joints = cam.getangles()
        payload = {"Username": username,
                   "Joints": joints}
        requests.post(user_url, payload)