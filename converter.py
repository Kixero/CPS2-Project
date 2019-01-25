import datetime
import json
import math
import paho.mqtt.client as mqttClient
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import time
import urllib2


"""
This Python script receives the values sent by the sensors in the IT'M from the MQTT 
broker and then fetches the AGV's position. 
It then creates a SPARQL query with this data to update an Apache Jena Server with an
RDF database.
"""

# Global variable for the state of the connection
Connected = False 

# Global variable to enable Test_Mode to use with the AGV emulator
# (see randomPublisher.py)
Test_Mode = True

# TODO Fill this
# The token to access to the Mir AGV API
Api_Token = ""

# Global variables for the measures values as they are only sent by the sensors
# when the value changes
Temperature = 0
Sound = 0
Humidity = 0
Luminosity = 0

# Global variables for the AGV's position only used in Test_Mode
posX = 0
posY = 0

# URL for the queries into the 'mesures' dataset onthe Jena server
jena_url = "http://localhost:3030/mesures/update"

# URL to the AGV's API to retrieve its status
url_info = 'http://192.168.42.253/api/v2.0.0/status' 

# MQTT topic for the sensor on the AGV
sensor_topic = 'emse/fayol/Mobile1/sensors/d1d7e6d4-db84-4a7c-a5e0-5bbddc9f130b/metrics/'

# A made up topic used for tests
test_topic = 'emse/fayol/Mobile1/CPS2/test/metrics/'

# URL for the AGV's API endpoint for the queue mission
api_queue_url = "http://mir.com:8080/v2.0.0/mission_queue"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0: 
        print("Connected to broker") 
        global Connected 
        Connected = True 
    else: 
        print("Connection failed")


def on_publish(client,userdata,result):
    #create function for callback
    print("data published " + str(result))
    pass

# Converts the x,y coordinates from the internal positioning system of
# the AGV into latitude and longitude coordinates.
# The formula was provided by Mireille Batton-Hubert
def to_lat_long(posX, posY):
    # Parameters
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

# Retrieves current time and set it to the write format for the RDF syntax
def get_formated_time():
    return str(datetime.datetime.now()).replace(' ', 'T')[:-7]

# Sends the SPARQL request to update the database
def send_update_request():
    nbre = re.sub(r"\D", "",str(datetime.datetime.now()))

    # Fetch for the AGV's position with its API if not in Test_Mode
    if (Test_Mode):
        global posX, posY
    else:
        posX, posY = get_position(url_info)

    # Convert positions to latitude and longitude
    lat, long = to_lat_long(posX, posY)

    # The (very long) SPARQL request to update the database with a new entry 
    # of 4 observations
    stringQuery = '''  BASE     <http://www.example.org>
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

    # Send the request and print the result
    sparql = SPARQLWrapper(jena_url)
    sparql.setQuery(stringQuery)
    sparql.setMethod('POST')
    results = sparql.query().convert()

    print(posX, posY, Temperature)
        
    print(results)

# Updates the globla variables when receiving a MQTT message and initiate a new request for the datatbase
def on_message(client, userdata, message): 
    print(message.topic + " " + str(message.payload))

    global Temperature, Humidity, Sound, Luminosity

    if (Test_Mode):
        global posX, posY

    if (message.topic == sensor_topic + 'TEMP'
        or message.topic == test_topic + 'TEMP'):
        Temperature = message.payload

        # If the temperature gets to high sed the AGV back to safety
        if int(Temperature) > 55:
            go_home()

    elif (message.topic == sensor_topic + 'HMDT'
        or message.topic == test_topic + 'HMDT'):
        Humidity = message.payload

    elif (message.topic == sensor_topic + 'SND'
        or message.topic == test_topic + 'SND'):
        Sound = message.payload

    elif (message.topic == sensor_topic + 'LUMI'
        or message.topic == test_topic + 'LUMI'):
        Luminosity = message.payload

    elif (message.topic == sensor_topic + 'POSX'
        or message.topic == test_topic + 'POSX'):
        posX = float(message.payload)

    elif (message.topic == sensor_topic + 'POSY'
        or message.topic == test_topic + 'POSY'):
        posY = float(message.payload)

    # Initiates the request
    send_update_request()
    

# Orders the AGV to go to a safe spot defined 
def go_home():
    print('Alert ! Returning Home')

    # Create a request to flush the mission queue and send it
    delete_request = urllib2.Request(api_queue_url)
    delete_request.add_header('Authorization', Api_Token)
    delete_request.get_method = lambda: 'DELETE'

    try:
        urllib2.urlopen(delete_request)

    except urllib2.URLError:
        print('Waiting for MiR connection')
        time.sleep(10)

    # TODO fill what data do we have to give to the mission_queue (ie the mission id)
    # Create a request to add the mission to go to the point named 'Home' and send it
    data = {}
    go_home_request = urllib2.Request(api_queue_url, json.dumps(data))
    go_home_request.add_header('Authorization', Api_Token)
    go_home_request.add_header('Content-Type', 'application/json')
    go_home_request.get_method = lambda: 'DELETE'

    try:
        urllib2.urlopen(go_home_request)

    except urllib2.URLError:
        print('Waiting for MiR connection')
        time.sleep(10)


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
    if (Test_Mode):
        brokeraddress = 'localhost'
        brokerport = 1884
    else:
        # Adress of the MQTT broker at EMSE
        brokeraddress= "193.49.165.40"
        brokerport = 1883

    # Setting callback functions
    client = mqttClient.Client("mir-converter")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect(brokeraddress, brokerport, 60)

    # Subscribing to snesor and test topics
    client.subscribe(sensor_topic + '#')
    client.subscribe(test_topic + '#')

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
            # Create new points even if no new measurment was received
            send_update_request()
            time.sleep(5)

    disconnectMQTT(client)
        
        
if __name__ == "__main__":
    main()

