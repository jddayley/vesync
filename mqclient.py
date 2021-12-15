import paho.mqtt.client as mqtt
from random import randint
import json
from vesync import VesyncApi
import paho.mqtt.client as mqtt
import logging
#Passwords stored in seperate file
from secrets import *
logging.basicConfig(filename='vesync.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

class VesyncMQ:
    def connect(self,id, qname):
        client = mqtt.Client("Humidifier_%s" % randint(1000,9999))  # Create instance of client with client ID “digi_mqtt_test”
        # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
        client.username_pw_set(MQNAME,MQPASSWORD)
        client.connect(MQSERVER, MQPORT)
        api = VesyncApi(USERNAME, PASSWORD)
        logging.info("Client %s" % id)
        r = api.get_detail(id)
        message = r.json()['result']['result']
        logging.info("Publish %s" % json.dumps(message))
        client.publish(qname, json.dumps(message))
    def main(self):
        client = VesyncMQ()
        client.connect('vsaq7588f6f84290868639af8c171175', "home/humidifier/state/basement")
        client.connect('vsaq7de16d3b4db2bae840277b436b61', "home/humidifier/state/upstairs")

if __name__ == '__main__':    
    client = VesyncMQ()
    client.main()
 
