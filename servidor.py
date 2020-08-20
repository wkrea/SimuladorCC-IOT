import ssl
import sys
import psycopg2 #conectarte python con postresql
import paho.mqtt.client #pip install paho-mqtt
import json

conn = psycopg2.connect(host = 'raja.db.elephantsql.com', user= 'oxgcstiv', password ='FlbrCdQbjb3asidam45INxN8PHORoroc', dbname= 'oxgcstiv')

    
def on_connect(client, userdata, flags, rc):    
    print('Conectado (%s)' % client._client_id)
    client.subscribe(topic='unimet/#', qos = 0)        

def entradasCC(client, userdata, message):   
    a = json.loads(message.payload) 
    print(a) 
    #print(message.qos)        
    if a["TYPE"] == "ENTRADA":
        cur = conn.cursor()
        sql = '''INSERT INTO log_cc (time_stamp, id_camara, mac_add, gender, age, count) VALUES ( %s, %s, %s, %s, %s, %s);'''
        cur.execute(sql, (a["DATE"],a["CAM_ID"],a["MAC_ADD"],a["GENDER"],a["AGE"],1))
        conn.commit()
        print('NUEVA ENTRADA CC')
    print('------------------------------')   

    if a["TYPE"] == "SALIDA":
        cur = conn.cursor()
        sql = '''INSERT INTO log_cc (time_stamp, id_camara, mac_add, gender, age, count,out) VALUES ( %s, %s, %s, %s, %s, %s,%s);'''
        cur.execute(sql, (a["DATE"],a["CAM_ID"],a["MAC_ADD"],a["GENDER"],a["AGE"],-1,1))
        conn.commit()
        print('NUEVA SALIDA CC')
    print('------------------------------')   


def entradasTIENDA(client, userdata, message):   
    a = json.loads(message.payload) 
    print(a) 
    #print(message.qos)        
    if a["TYPE"] == "ENTRADA":
        cur = conn.cursor()
        sql = '''INSERT INTO log_tienda (time_stamp, id_tienda, mac_add, count) VALUES ( %s, %s, %s, %s);'''
        cur.execute(sql, (a["DATE"],a["TIENDA_ID"],a["MAC_ADD"],1))
        conn.commit()
        print('NUEVA ENTRADA TIENDA')
    print('------------------------------')   

    if a["TYPE"] == "SALIDA":
        cur = conn.cursor()
        sql = '''INSERT INTO log_tienda (time_stamp, id_tienda, mac_add, count,out) VALUES ( %s, %s, %s, %s, %s);'''
        cur.execute(sql, (a["DATE"],a["TIENDA_ID"],a["MAC_ADD"],-1,1))
        conn.commit()
        print('NUEVA SALIDA TIENDA')
    print('------------------------------')   



def beaconCC(client, userdata, message):   
    a = json.loads(message.payload) 
    print(a) 

    cur = conn.cursor()
    sql = '''INSERT INTO beacons_log (time_stamp, id_beacon, mac_add) VALUES ( %s, %s, %s);'''
    cur.execute(sql, (a["DATE"],a["BEACON_ID"],a["MAC_ADD"]))
    conn.commit()
    print('DISPOSITIVO DETECTADO POR BEACON')
    print('------------------------------')   

def ventasTIENDA(client, userdata, message):   
    a = json.loads(message.payload) 
    print(a) 
    cur = conn.cursor()
    sql = '''INSERT INTO ventas (time_stamp, id_tienda, mac_add, monto) VALUES ( %s, %s, %s, %s);'''
    cur.execute(sql, (a["DATE"],a["ID_TIENDA"],a["MAC_ADD"],a["MONTO"]))
    conn.commit()
    print('VENTA EFECTUADA')
    print('------------------------------')   

def mesaFERIA(client, userdata, message):   
    a = json.loads(message.payload) 
    print(a) 
    cur = conn.cursor()
    sql = '''INSERT INTO mesa_log (time_stamp, id_mesa, mac_add, estado) VALUES ( %s, %s, %s, %s);'''
    cur.execute(sql, (a["DATE"],a["MESA_ID"],a["MAC_ADD"],a["ESTADO"]))
    conn.commit()
    print('CAMBIO EN MESA')
    print('------------------------------')   



def main():	
    client = paho.mqtt.client.Client()
    client.on_connect = on_connect
    client.message_callback_add('unimet/acceso/cc', entradasCC)
    client.message_callback_add('unimet/acceso/tienda', entradasTIENDA)
    client.message_callback_add('unimet/ventas', ventasTIENDA)
    client.message_callback_add('unimet/beacon', beaconCC)
    client.message_callback_add('unimet/mesa', mesaFERIA)
    client.connect("broker.hivemq.com",1883,60)
    client.loop_forever()

if __name__ == '__main__':
	main()
	sys.exit(0)



