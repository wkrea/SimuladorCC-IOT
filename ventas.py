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
	meanEntrada = 200 #Clientes Hora
	stdEntrada = 50
	cantMonto = 1000

	stdEntrada= 1/((stdEntrada+meanEntrada)/(60*60))
	meanEntrada = 1/(meanEntrada/(60*60))
	stdEntrada = meanEntrada-stdEntrada

	print (meanEntrada)
	print (stdEntrada)



	while(True):
		hora = datetime.datetime.now()	
		monto = int(np.random.uniform(1, cantMonto))
		cursor = conn.cursor()
		postgreSQL_select_Query = "select * from log_tienda where out=0"
		cursor.execute(postgreSQL_select_Query)
		mobile_records = cursor.fetchall()
		
		
		if len(mobile_records) >= 1:
			persona_en_tienda =mobile_records[int(np.random.uniform(0, len(mobile_records)))]
			print("Id Comprando= ", persona_en_tienda[0], )
	

			payload = {
				"DATE": str(hora),
				"MONTO": str(monto),
				"MAC_ADD": persona_en_tienda[2],
				"ID_TIENDA": persona_en_tienda[1],


			}
			client.publish('unimet/ventas',json.dumps(payload),qos=0)		

			print(payload)



		time.sleep(int(np.random.normal(meanEntrada, stdEntrada)))



if __name__ == '__main__':
	main()
	sys.exit(0)


