import json
import urllib2
import paho.mqtt.client as mqttClient
import time

Connected = False #global variable for the state of the connection

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if rc == 0: 
        print("Connected to broker") 
        global Connected                #Use global variable
        Connected = True                #Signal connection  
    else: 
        print("Connection failed")

def on_publish(client,userdata,result):
    #create function for callback
    print("data published " + str(result))
    pass

def on_message(client, userdata, message):
    pass


def connectMQQT(brokeraddress, brokerport):
    client = mqttClient.Client("mir-converter")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect(brokeraddress, brokerport, 60)
    client.loop_start();
    return client

def disconnectMQTT(clientMQQT):
   clientMQQT.disconnect()

def main():
    broker_address= "192.168.1.14"
    broker_port = 1883
    while True:
        while not Connected:
            print('Broker MQQT connection')
            client = connectMQQT(broker_address, broker_port)
            time.sleep(10)    
        while Connected:
            time.sleep(5)
    disconnectMQTT(client)
        
        
if __name__ == "__main__":
    main()

