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

def connectMQQT(brokeraddress, brokerport):
    client = mqttClient.Client("client-mir100")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(brokeraddress, brokerport, 60)
    client.loop_start();
    return client

def disconnectMQTT(clientMQQT):
   clientMQQT.disconnect()

def requestURL(urllink,clientmqtt):
    try:
        url = urllib2.urlopen(urllink)
        print('Connection to mir100')
        response = json.loads(url.read())
        #print(response)
        url.close()
        for key, value in response.items():    
            if( key == 'battery_percentage'):
                batt = value
            elif( key == 'position'):
                pos = value
                for key1, value1 in pos.items():
                    if( key1 == 'x'):
                        posX = value1
                    elif( key1 == 'y'):
                        posY = value1
        clientmqtt.publish("emse/fayol/CPS2/Mir/metrics/BATT", batt)
        clientmqtt.publish("emse/fayol/CPS2/Mir/metrics/LATI", posX)
        clientmqtt.publish("emse/fayol/CPS2/Mir/metrics/LONG", posY) 
        print('MiR connection closed')
    except urllib2.URLError:
        print('Waiting for MiR connection')
        time.sleep(10)

def main():
    broker_address= "193.49.165.40"
    broker_port = 1883
    url_info = 'http://192.168.42.253/api/v2.0.0/status'    
    while True:
        while not Connected:
            print('Broker MQQT connection')
            client = connectMQQT(broker_address, broker_port)
            time.sleep(10)    
        while Connected:
            print('Info Mir')
            requestURL(url_info,client)
            time.sleep(5)
    disconnectMQTT(client)
        
        
if __name__ == "__main__":
    main()

