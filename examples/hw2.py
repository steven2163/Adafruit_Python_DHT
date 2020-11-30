#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import http.client as http
import urllib
import json
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)

deviceId = "D6EKC3mV"
deviceKey = "TD7epCSxLAoo7MIN" 

def post_to_mcs(payload): 
        headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
        not_connected = 1 
        while (not_connected):
                try:
                        conn = http.HTTPConnection("api.mediatek.com:80")
                        conn.connect() 
                        not_connected = 0 
                except (http.HTTPException, socket.error) as ex: 
                        print ("Error: %s" % ex)
                        time.sleep(10)
			 # sleep 10 seconds 
        conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
        response = conn.getresponse() 
        print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
        data = response.read() 
        conn.close() 
try:
    while True:
        SwitchStatus = GPIO.input(4)
        if GPIO.input(4)==1:  #按下去就亮
            print("Button pressed")
       # else:                 #其他時候不亮
        payload = {"datapoints":[{"dataChnId":"SwitchStatus","values":{"value":SwitchStatus}}]} 
        post_to_mcs(payload)
        time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
