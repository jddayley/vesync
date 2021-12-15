import paho.mqtt.client as mqtt
from random import randint
import json
from vesync import VesyncApi
from mqclient import VesyncMQ
import logging
import re
USERNAME = ""
PASSWORD = ""

logging.basicConfig(filename='/usr/src/app/mq.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Starting Application")


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    logging.info("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("home/humidifier/command/#") 
def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    # Trigger the on or off
    found = 'skip'
    logging.info("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    #payload = msg.payload
    payload = msg.payload.decode("utf-8")
    logging.info(msg.topic+" "+str(payload))
    try:
        found = re.search('home/humidifier/command/(.*)', msg.topic).group(1)
        logging.info(found)
    except AttributeError:
        pass
    if 'on' in payload:
       logging.info("Turning ON")
       api = VesyncApi(USERNAME, PASSWORD)
       api.turn_on(found)
    elif 'off' in payload:
       logging.info("Turning OFF")
       api = VesyncApi(USERNAME, PASSWORD)
       api.turn_off(found)
    client = VesyncMQ()
    client.main()
client = mqtt.Client("Humidifier_%s" % randint(1000,9999))  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.username_pw_set('jddayley','java')
client.connect('192.168.0.116', 1883)
client.loop_forever()  # Start networking daemon