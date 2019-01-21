import json
import urllib2
import paho.mqtt.client as mqttClient
import time
import random as rd
import numpy as np

Connected = False  # global variable for the state of the connection


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")


def on_publish(client, userdata, result):
    # create function for callback
    print("data published " + str(result))
    pass


def on_message(client, userdata, message):
    pass


def connectMQQT(brokeraddress, brokerport):
    client = mqttClient.Client("mir-converter")
    client.username_pw_set('test2', '')
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect(brokeraddress, brokerport, 60)
    client.loop_start();
    return client


def disconnectMQTT(clientMQQT):
    clientMQQT.disconnect()

def random_position(x, y, sigma):
    # return (x,y)
    return round(rd.gauss(x, sigma), 3), round(rd.gauss(y, sigma), 3)


def random_positions(xmin, xmax, ymin, ymax, sigma, n):
    """ Return n positions on each side of a rectangle, with a normal repartition along the line """

    topline =[]
    rightline = []
    bottomline = []
    leftline = []

    positions = []


    hor_positions = np.linspace(xmin, xmax, n)
    ver_positions = np.linspace(xmin, xmax, n)

    # TopLine
    for k in range(n):
        bottomline.append(random_position(hor_positions[k], ymin, sigma))
        rightline.append(random_position(xmax, ver_positions[k], sigma))
        topline.append(random_position(hor_positions[n-1-k], ymax, sigma))
        leftline.append(random_position(xmin, ver_positions[n-1-k], sigma))

    positions = bottomline + rightline + topline + leftline

    return positions

def random_values(vmin, vmax, n):
    return np.random.normal((vmin + vmax)/2, (vmax - vmin)/2, n)

def main():
    rd.seed(12)
    n = 20
    broker_address = "localhost"
    broker_port = 1884
    positions = random_positions(10, 24, 12, 20, 0.5, n)
    temperatures = random_values(19, 21, n*4)

    while True:
        while not Connected:
            print('Broker MQQT connection')
            client = connectMQQT(broker_address, broker_port)
            time.sleep(10)
                #ret = client.publish("emse/fayol/Mobile1/CPS2/test/metrics/POS",str(positions[k]))
                ret = client.publish("emse/fayol/Mobile1/CPS2/test/metrics/TEMP",str(temperatures[k]))
                print (ret)
                time.sleep(3)
    disconnectMQTT(client)



if __name__ == "__main__":
    main()

