import ssl
import sys
import json
import random
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime

def on_connect(client, userdata, flags, rc):
	print('conectado publicador')

def main():
	client = paho.mqtt.client.Client()
	client.qos = 0
	client.connect("broker.hivemq.com",1883,60)
	meanEntrada = 1000 #Clientes Hora
	stdEntrada = 100
	cantCamaras = 4

	stdEntrada= 1/((stdEntrada+meanEntrada)/(60*60))
	meanEntrada = 1/(meanEntrada/(60*60))
	stdEntrada = meanEntrada-stdEntrada

	print (meanEntrada)
	print (stdEntrada)

	while(True):
		hora = datetime.datetime.now()				
		camara = int(np.random.uniform(1, cantCamaras))
		mac_add = ""
		age = "0"
		gender = ""

		if bool(int(np.random.uniform(0, 2))):
			mac_add = MACprettyprint(randomMAC())
		
		if bool(int(np.random.uniform(0, 2))):
			age = randomAGE()
			gender = randomGENDER()
		
		

		payload = {
			"DATE": str(hora),
			"CAM_ID": str(camara),
			"MAC_ADD": mac_add,
			"GENDER": gender,
			"AGE": age,
			"TYPE": "ENTRADA",

		}
		client.publish('unimet/acceso/cc',json.dumps(payload),qos=0)		

		print(payload)
		time.sleep(int(np.random.normal(meanEntrada, stdEntrada)))


def randomGENDER():
	if bool(int(np.random.uniform(0, 2))):
		return "F"
	else:
		return "M"

def randomAGE():
	return abs(int(np.random.normal(40, 10)))

def randomMAC():
    return [ 0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]

def MACprettyprint(mac):
    return ':'.join(map(lambda x: "%02x" % x, mac))

if __name__ == '__main__':
	main()
	sys.exit(0)


