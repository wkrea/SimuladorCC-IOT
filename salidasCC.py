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
	meanEntrada = 500 #Clientes Hora
	stdEntrada = 50
	cantCamaras = 4

	stdEntrada= 1/((stdEntrada+meanEntrada)/(60*60))
	meanEntrada = 1/(meanEntrada/(60*60))
	stdEntrada = meanEntrada-stdEntrada

	print (meanEntrada)
	print (stdEntrada)



	while(True):
		hora = datetime.datetime.now()	
		camara = int(np.random.uniform(1, cantCamaras))
		cursor = conn.cursor()
		postgreSQL_select_Query = "select * from log_cc where out=0"
		cursor.execute(postgreSQL_select_Query)
		mobile_records = cursor.fetchall()
		
		
		if len(mobile_records) >= 1:
			persona_saliente =mobile_records[int(np.random.uniform(0, len(mobile_records)))]
			print("Id Saliendo= ", persona_saliente[0], )
			sql_update_query = "Update log_cc set out = %s where id = %s"
			cursor.execute(sql_update_query, (1, persona_saliente[0]))
			conn.commit()

			payload = {
				"DATE": str(hora),
				"CAM_ID": str(camara),
				"MAC_ADD": persona_saliente[3],
				"GENDER": persona_saliente[4],
				"AGE": persona_saliente[5],
				"TYPE": "SALIDA",

			}
			client.publish('unimet/acceso/cc',json.dumps(payload),qos=0)		

			print(payload)



		time.sleep(int(np.random.normal(meanEntrada, stdEntrada)))



if __name__ == '__main__':
	main()
	sys.exit(0)


