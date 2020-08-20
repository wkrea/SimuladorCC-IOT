import ssl
import sys
import json
import random
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime
import psycopg2

conn = psycopg2.connect(host = 'raja.db.elephantsql.com', user= 'oxgcstiv', password ='FlbrCdQbjb3asidam45INxN8PHORoroc', dbname= 'oxgcstiv')


def on_connect(client, userdata, flags, rc):
	print('conectado publicador')

def main():
	client = paho.mqtt.client.Client()
	client.qos = 0
	client.connect("broker.hivemq.com",1883,60)
	meanEntrada = 500 
	stdEntrada = 50
	cantCamaras = 7

	stdEntrada= 1/((stdEntrada+meanEntrada)/(60*60))
	meanEntrada = 1/(meanEntrada/(60*60))
	stdEntrada = meanEntrada-stdEntrada

	print (meanEntrada)
	print (stdEntrada)



	while(True):
		saltar = False
		hora = datetime.datetime.now()	
		camara = int(np.random.uniform(1, cantCamaras))
		cursor = conn.cursor()
		postgreSQL_select_Query = "select * from log_cc where out=0 and mac_add != '' "
		cursor.execute(postgreSQL_select_Query)
		mobile_records = cursor.fetchall()
		
		
		if len(mobile_records) >= 1:
			persona_saliente =mobile_records[int(np.random.uniform(0, len(mobile_records)))]
			print("Id Detectado= ", persona_saliente[0], )

			mac_id = persona_saliente[3]
			postgreSQL_select_Query = "select sum(count) as libre from log_tienda where mac_add = '"+mac_id+"'" 
			cursor.execute(postgreSQL_select_Query)
			libre = cursor.fetchall()
			if libre[0] == 1:
				saltar = True
	
			if saltar == False:
				payload = {
					"DATE": str(hora),
					"BEACON_ID": str(camara),
					"MAC_ADD": persona_saliente[3],

				}
				client.publish('unimet/beacon',json.dumps(payload),qos=0)		

				print(payload)


		if saltar == False:
			time.sleep(int(np.random.normal(meanEntrada, stdEntrada)))



if __name__ == '__main__':
	main()
	sys.exit(0)


