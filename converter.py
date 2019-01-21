import json
import urllib2
import paho.mqtt.client as mqttClient
from SPARQLWrapper import SPARQLWrapper, JSON
import datetime
import time
import re
import math

Connected = False #global variable for the state of the connection

#The token to access to the Mir AGV API
#TODO fill the api access token
api_token = ""

Temperature = 0
Sound = 0
Humidity = 0
Luminosity = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
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

def to_lat_long(posX, posY):
    #Paramètres
    a1 = -0.42 # D1 : y = a1 x + b1
    a2 = 2.7 # D2 : y = a2 x + b2
    b1 = 5895038.9
    b2 = 4365515.5
    alpha1 = -0.4
    alpha2 = 1.21
    beta2 = 1.57-1.21

    XL1 = 490231.9 - 1.5 * (posX-10) * math.cos(alpha1)
    YL1 = a1 * XL1 + b1
    
    bd2 = YL1 - a2 * XL1

    YL2 = 5689141.6 - 1.5 * (posY-10) * math.cos(beta2)
    XL2 = (YL2 - b2)/a2
    
    bd1 = YL2 - a1 * XL2

    postransfx = (bd2-bd1)/(a1-a2)
    postransfy = a1 * postransfx + bd1

    return postransfx, postransfy

def get_formated_time():
    return str(datetime.datetime.now()).replace(' ', 'T')[:-7]

def send_update_request():
    #url_info = 'http://192.168.42.253/api/v2.0.0/status' 
    url_info = 'http://localhost:8080/api/location'

    nbre = re.sub(r"\D", "",str(datetime.datetime.now()))

    posX, posY = get_position(url_info)
    posX, posY = 11.3, 19.4
    lat, long = to_lat_long(posX, posY)

    stringQuery = '''  BASE     <http://localhost:3030>
                PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#> 
                PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#> 
                PREFIX sosa:    <http://www.w3.org/ns/sosa/> 
                PREFIX cdt:     <http://w3id.org/lindt/custom_datatypes#> 
                PREFIX geo:     <http://www.w3.org/2003/01/geo/wgs84_pos#> 
                PREFIX geom:  <http://data.ign.fr/def/geometrie/> 

                INSERT DATA 
                { 
                <observation/''' + nbre + '''T> a 	sosa:Observation ; 
                    sosa:observedProperty <temperature> ; 
                    sosa:hasFeatureOfInterest 
                    [ 
                        geo:lat ''' + str(lat) + ''' ; 
                        geo:long ''' + str(long) + ''' ; 
                        geom:x ''' + str(posX) + ''' ;
                        geom:y ''' + str(posY) + '''
                    ] ; 
                    sosa:madeBySensor <sensor/mobile1/TEMP> ; 
                    sosa:hasSimpleResult "''' + str(Temperature) + ''' Cel"^^cdt:temperature ; 
                    sosa:resultTime "''' + get_formated_time() + '''"^^xsd:dateTime .

                <observation/''' + nbre + '''H> a 	sosa:Observation ; 
                    sosa:observedProperty <humidity> ; 
                    sosa:hasFeatureOfInterest 
                    [ 
                        geo:lat ''' + str(lat) + ''' ; 
                        geo:long ''' + str(long) + ''' ; 
                        geom:x ''' + str(posX) + ''' ;
                        geom:y ''' + str(posY) + '''
                    ] ; 
                    sosa:madeBySensor <sensor/mobile1/HMDT> ; 
                    sosa:hasSimpleResult "''' + str(Humidity) + ''' %"^^cdt:dimensionless ; 
                    sosa:resultTime "''' + get_formated_time() + '''"^^xsd:dateTime .

                <observation/''' + nbre + '''S> a 	sosa:Observation ; 
                    sosa:observedProperty <sound> ; 
                    sosa:hasFeatureOfInterest 
                    [ 
                        geo:lat ''' + str(lat) + ''' ; 
                        geo:long ''' + str(long) + ''' ; 
                        geom:x ''' + str(posX) + ''' ;
                        geom:y ''' + str(posY) + '''
                    ] ; 
                    sosa:madeBySensor <sensor/mobile1/SND> ; 
                    sosa:hasSimpleResult "''' + str(Sound) + '''" ; 
                    sosa:resultTime "''' + get_formated_time() + '''"^^xsd:dateTime .
                
                <observation/''' + nbre + '''L> a 	sosa:Observation ; 
                    sosa:observedProperty <luminosity> ; 
                    sosa:hasFeatureOfInterest 
                    [ 
                        geo:lat ''' + str(lat) + ''' ; 
                        geo:long ''' + str(long) + ''' ; 
                        geom:x ''' + str(posX) + ''' ;
                        geom:y ''' + str(posY) + '''
                    ] ; 
                    sosa:madeBySensor <sensor/mobile1/LUMI> ; 
                    sosa:hasSimpleResult "''' + str(Luminosity) + '''" ; 
                    sosa:resultTime "''' + get_formated_time() + '''"^^xsd:dateTime .
                } '''

    sparql = SPARQLWrapper("http://localhost:3030/mesures/update")
    sparql.setQuery(stringQuery)
    sparql.setMethod('POST')
    results = sparql.query().convert()
        
    print(results)
                
def on_message(client, userdata, message): 
    print(message.topic + " " + str(message.payload))

    global Temperature, Humidity, Sound, Luminosity

    if (message.topic == 'emse/fayol/Mobile1/sensors/d1d7e6d4-db84-4a7c-a5e0-5bbddc9f130b/metrics/TEMP'
        or message.topic == 'emse/fayol/Mobile1/CPS2/test/metrics/TEMP'):
        Temperature = message.payload
        if Temperature > 55:
            go_home()

    elif (message.topic == 'emse/fayol/Mobile1/sensors/d1d7e6d4-db84-4a7c-a5e0-5bbddc9f130b/metrics/HMDT'
        or message.topic == 'emse/fayol/Mobile1/CPS2/test/metrics/HMDT'):
        Humidity = message.payload

    elif (message.topic == 'emse/fayol/Mobile1/sensors/d1d7e6d4-db84-4a7c-a5e0-5bbddc9f130b/metrics/SND'
        or message.topic == 'emse/fayol/Mobile1/CPS2/test/metrics/SND'):
        Sound = message.payload

    elif (message.topic == 'emse/fayol/Mobile1/sensors/d1d7e6d4-db84-4a7c-a5e0-5bbddc9f130b/metrics/LUMI'
        or message.topic == 'emse/fayol/Mobile1/CPS2/test/metrics/LUMI'):
        Luminosity = message.payload

    send_update_request()


def go_home():
    print('Alert ! Returning Home')
    api_queue_url = "mir.com:8080/v2.0.0/mission_queue"

    delete_request = urllib2.Request(api_queue_url)
    delete_request.add_header('Authorization', api_token)
    delete_request.get_method = lambda: 'DELETE'

    try:
        urllib2.urlopen(delete_request)
    except Exception, e:
        print(e.code)
        print(e.read())

    #TODO fill what data do we have to give to the mission_queue (ie the mission id)
    data = {}
    go_home_request = urllib2.Request(api_queue_url, json.dumps(data))
    go_home_request.add_header('Authorization', api_token)
    go_home_request.add_header('Content-Type', 'application/json')
    go_home_request.get_method = lambda: 'DELETE'

    try:
        urllib2.urlopen(go_home_request)
    except Exception, e:
        print(e.code)
        print(e.read())



def get_position(urllink):
    try:
        url = urllib2.urlopen(urllink)
        print('Connection to mir100')
        response = json.loads(url.read())
        url.close()

        for key, value in response.items():
            if (key == 'position'):
                pos = value
                for key1, value1 in pos.items():
                    if (key1 == 'x'):
                        posX = value1
                    elif (key1 == 'y'):
                        posY = value1

        print('MiR connection closed')

    except urllib2.URLError:
        print('Waiting for MiR connection')
        time.sleep(10)

    return posX, posY


def connectMQQT():
    #broker_address= "193.49.165.40"
    #broker_port = 1883    
    brokeraddress = 'localhost'
    brokerport = 1884

    client = mqttClient.Client("mir-converter")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect(brokeraddress, brokerport, 60)

    client.subscribe('emse/fayol/Mobile1/sensors/d1d7e6d4-db84-4a7c-a5e0-5bbddc9f130b/metrics/#')
    client.subscribe('emse/fayol/Mobile1/CPS2/test/metrics/#')

    client.loop_start()
    return client

def disconnectMQTT(clientMQQT):
   clientMQQT.disconnect()

def main():
    while True:
        while not Connected:
            print('Broker MQQT connection')
            client = connectMQQT()
            time.sleep(10)
        while Connected:
            send_update_request()
            time.sleep(3)
    disconnectMQTT(client)
        
        
if __name__ == "__main__":
    main()

