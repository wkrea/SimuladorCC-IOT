
CREATE OR REPLACE FUNCTION nueva_persona()\
RETURNS TRIGGER AS $$\
\
BEGIN\
INSERT INTO persona (mac_add)\
VALUES (NEW.mac_add) ON CONFLICT DO NOTHING;\
return NEW;\
END\
\
$$ LANGUAGE 'plpgsql'\
\
CREATE TRIGGER nuevo_ingreso_cc\
BEFORE INSERT ON log_cc\
FOR EACH ROW\
EXECUTE PROCEDURE nueva_persona();\
\
\
\
\
\
\
\
\
\
\
\
\
TRIGGER VALIDAR CLIENTE DENTRO DEL CC ANTES DE REGISTRAR VENTA\
\
CREATE OR REPLACE FUNCTION validar_venta()\
RETURNS TRIGGER AS $$\
\
DECLARE\
    ni int;\
BEGIN\
	IF NEW.mac_add != '' THEN\
	    SELECT sum(count) INTO ni FROM log_cc where mac_add = NEW.mac_add;\
	    IF NOT FOUND THEN\
	    	RAISE EXCEPTION 'No existe ese cliente';\
	    END IF;\
	    IF NI > 0 THEN\
	    	return NEW;	\
	    ELSE \
	    	RAISE EXCEPTION 'Cliente no esta presente en el cc';\
	    END IF;\
	ELSE\
		return NEW;\
	END IF;\
END\
\
\
$$ LANGUAGE 'plpgsql'\
\
CREATE TRIGGER venta_valida\
BEFORE INSERT ON ventas\
FOR EACH ROW\
EXECUTE PROCEDURE validar_venta();\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
TRIGGER MARCAR MESA COMO USADA LUEGO DE LIBERARSE\
\
CREATE OR REPLACE FUNCTION mesa_sucia()\
RETURNS TRIGGER AS $$\
\
BEGIN\
IF NEW.estado = 0 THEN\
	UPDATE mesa SET limpiar = 1\
	WHERE id = NEW.id_mesa;\
END IF;\
return NEW;\
END\
\
$$ LANGUAGE 'plpgsql'\
\
CREATE TRIGGER mesa_usada\
BEFORE INSERT ON mesa_log\
FOR EACH ROW\
EXECUTE PROCEDURE mesa_sucia();\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
PA CALCULAR EL PAGO DE ALQUILER DE CADA LOCAL COMO EL 10% DE SUS VENTAS\
\
CREATE OR REPLACE FUNCTION pago_alquiler(integer) RETURNS integer AS $$\
DECLARE\
	local_id ALIAS FOR $1;\
	resultado INTEGER;\
	ni int;\
BEGIN\
	SELECT \
\pard\pardeftab577\li720\fi720\ri0\partightenfactor0
\cf0 sum(monto) \
\pard\pardeftab577\li720\ri0\partightenfactor0
\cf0 INTO \
\pard\pardeftab577\li720\fi720\ri0\partightenfactor0
\cf0 ni \
\pard\pardeftab577\li720\ri0\partightenfactor0
\cf0 FROM\
\pard\pardeftab577\li720\fi720\ri0\partightenfactor0
\cf0 ventas \
\pard\pardeftab577\li720\ri0\partightenfactor0
\cf0 WHERE \
\pard\pardeftab577\li720\fi720\ri0\partightenfactor0
\cf0 id_tienda = local_id AND ventas.time_stamp > (CURRENT_DATE - '1 mon'::interval);\
\
\pard\pardeftab577\ri0\partightenfactor0
\cf0 	resultado := ni*0.1;\
\
 	RETURN resultado;\
END;\
$$ LANGUAGE plpgsql;\
\
\
Ejemplo:\
SELECT pago_alquiler(tienda_id);\
\
\
\
\
\
\
\
\
\
\
\
\
\
PA EVALUAR SI TODAS LAS MESAS ESTAN SUCIAS PARA ENVIAR PERSONAL DE LIMPIEZA\
\
\
CREATE OR REPLACE FUNCTION getLimpiarMesas() RETURNS integer AS $$\
DECLARE\
    ni int;\
BEGIN\
	    select count(limpiar) INTO ni from mesa where limpiar = 0;\
	    \
	    IF NOT FOUND THEN\
	    	RETURN 1;\
	    END IF;\
	    IF NI > 0 THEN\
	    	RETURN 0;\
	    ELSE \
	    	RETURN 1;\
	    END IF;\
\
\
END;\
$$ LANGUAGE plpgsql;\
\
\
Ejemplo:\
SELECT getLimpiarMesas();\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
PA LIMPIAR TODAS LAS MESAS\
\
CREATE OR REPLACE FUNCTION LimpiarMesas() RETURNS integer AS $$\
\
BEGIN\
\
UPDATE mesa SET limpiar = 0;\
\
return 1;\
\
END;\
$$ LANGUAGE plpgsql;\
\
\
Ejemplo:\
SELECT LimpiarMesas();\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
PA ALMACENAR HORA DE ENTRADA CC EN VENTA\
\
CREATE OR REPLACE FUNCTION nueva_compra(integer,integer,integer) RETURNS text AS $$\
DECLARE\
	tienda_id_e ALIAS FOR $1;\
	cedula_e ALIAS FOR $2;\
	monto_e ALIAS FOR $3;\
	resultado INTEGER;\
	n2 TEXT;\
	n3 timestamp;\
	\
BEGIN\
	select mac_add INTO n2 from persona where cedula = cedula_e;\
	select time_stamp INTO n3 from log_cc WHERE mac_add = n2 and count = 1 ORDER BY ID DESC LIMIT 1;\
	INSERT INTO ventas (id_tienda,monto,mac_add,hora_entrada) VALUES (tienda_id_e, monto_e, n2, n3);\
	RETURN n2;\
	\
END;\
$$ LANGUAGE plpgsql;\
\
\
Ejemplo\
select nueva_compra(1,21291715,300)
\fs24 \
}