from os import pardir
import requests, json, time, datetime, io, hashlib
from random import randint
from datetime import datetime
from urllib.request import urlopen
import urllib3

urllib3.disable_warnings()
# Define pseudo constants
SCRIPT_NAME = 'vesync.py'
SCRIPT_VERSION = '1.0'
#requests.packages.urllib3.disable_warnings()
BASE_URL = "https://smartapi.vesync.com"
ts = time.time()
st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#Creates empty token and accountid variables which are automatically filled when script runs as long as username and password entered above.
token = ""
accountID = ""
import logging

logging.basicConfig(
    filename='vesync.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)


class VesyncApi:
    def __init__(self, username, password):
        global token
        global accountID

        payload = json.dumps({
            "account":
            username,
            "devToken":
            "",
            "password":
            hashlib.md5(password.encode('utf-8')).hexdigest()
        })
        account = requests.post(BASE_URL + "/vold/user/login",
                                verify=False,
                                data=payload).json()
        if "error" in account:
            raise RuntimeError("Invalid username or password")
        else:
            self._account = account
            #logging.info (account)
            token = account['tk']
            #logging.info (token)
            accountID = account['accountID']
            #logging.info (accountID)
            logging.info('Account Connection Successful')

        self._devices = []

    def get_detail(self, id):
        global token
        global accountID
        payload = {
            "acceptLanguage": "en",
            "accountID": accountID,
            "appVersion": "VeSync 3.1.54 build10",
            "cid": id,
            "configModule": "WFON_AHM_LUH-A602S-WUS_US",
            "deviceRegion": "US",
            "method": "bypassV2",
            "payload": {
                "data": {},
                "method": "getHumidifierStatus",
                "source": "APP"
            },
            "phoneBrand": "iPhone",
            "phoneOS": "iOS 15.1.1",
            "timeZone": "America/New_York",
            "token": token,
            "traceId": "1639257589508",
            "userCountryCode": "US"
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.post(BASE_URL + '/cloud/v2/deviceManaged/bypassV2',
                          headers=headers,
                          json=payload)
        return r

    def get_devices(self, id):
        global token
        global accountID
        payload = {
            "acceptLanguage": "en",
            "accountID": accountID,
            "appVersion": "VeSync 3.1.54 build10",
            "cid": id,
            "method": "deviceInfo",
            "phoneBrand": "iPhone",
            "phoneOS": "iOS 15.1.1",
            "subDeviceNo": 0,
            "timeZone": "America/New_York",
            "token": token,
            "traceId": "1639257579506",
            "userCountryCode": "US"
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.post(BASE_URL + '/cloud/v1/deviceManaged/deviceInfo',
                          headers=headers,
                          json=payload)
        return r

    def turn_off(self, id):
        payload = {
            "acceptLanguage": "en",
            "accountID": accountID,
            "appVersion": "VeSync 3.1.54 build10",
            "cid": id,
            "configModule": "WFON_AHM_LUH-A602S-WUS_US",
            "debugMode": False,
            "deviceRegion": "US",
            "method": "bypassV2",
            "payload": {
                "data": {
                    "enabled": False,
                    "id": 0
                },
                "method": "setSwitch",
                "source": "APP"
            },
            "phoneBrand": "iPhone",
            "phoneOS": "iOS 15.1.1",
            "timeZone": "America/New_York",
            "token": token,
            "traceId": "1639267601802",
            "userCountryCode": "US"
        }
        headers = {
            'Content-Type':
            'application/json',
            'Accept':
            '*/*',
            'user-agent':
            'VeSync/3.1.54 (com.etekcity.vesyncPlatform; build:10; iOS 15.1.1) Alamofire/5.2.1'
        }
        r = requests.put(BASE_URL + '/cloud/v2/deviceManaged/bypassV2',
                         headers=headers,
                         json=payload)
        logging.info(r.text)

    def turn_on(self, id):
        payload = {
            "acceptLanguage": "en",
            "accountID": accountID,
            "appVersion": "VeSync 3.1.54 build10",
            "cid": id,
            "configModule": "WFON_AHM_LUH-A602S-WUS_US",
            "debugMode": False,
            "deviceRegion": "US",
            "method": "bypassV2",
            "payload": {
                "data": {
                    "enabled": True,
                    "id": 0
                },
                "method": "setSwitch",
                "source": "APP"
            },
            "phoneBrand": "iPhone",
            "phoneOS": "iOS 15.1.1",
            "timeZone": "America/New_York",
            "token": token,
            "traceId": "1639267601802",
            "userCountryCode": "US"
        }
        headers = {
            'Content-Type':
            'application/json',
            'Accept':
            '*/*',
            'user-agent':
            'VeSync/3.1.54 (com.etekcity.vesyncPlatform; build:10; iOS 15.1.1) Alamofire/5.2.1'
        }
        r = requests.put(BASE_URL + '/cloud/v2/deviceManaged/bypassV2',
                         headers=headers,
                         json=payload)
        logging.info(r.text)
