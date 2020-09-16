import paho.mqtt.client as mqtt
import datetime
import json
from pymongo import MongoClient

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), './config/config.env')
load_dotenv(dotenv_path)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc) + "\ntopic : "+ os.getenv('TOPIC') + "\nhost :  "
    +os.getenv('BROKER_HOST') +"\ndatabase : "+os.getenv('MONGO_URL'))
    client.subscribe(os.getenv('TOPIC'))
	

def on_message(client, userdata, msg):
    receiveTime=datetime.datetime.now()
    message=str(msg.payload.decode("utf-8","ignore"))
    jsonMessage=json.loads(message)
    isfloatValue=False
    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue=True
    except:
        isfloatValue=False

    if isfloatValue:
        print(str(receiveTime) + "topic : " + msg.topic + ", message : \n" + str(val))
        post={"time":receiveTime,"value":val}
    else:
        print(str(receiveTime) + " topic : " + msg.topic + ",\nmessage : " + message)
        post={"time":receiveTime,"status":jsonMessage["status"], "location":jsonMessage["location"]}

    collection.insert_one(post)


# Set up client for MongoDB
mongoClient=MongoClient(os.getenv('MONGO_URL'))
db=mongoClient.smartpark
collection=db.records

# Initialize the client that should connect to the Mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# print(os.environ.get('BROKER_HOST'))
client.connect(os.getenv('BROKER_HOST'), os.getenv('PORT'), 60)

# Blocking loop to the Mosquitto broker
client.loop_forever()