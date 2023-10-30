from tkinter import * 
from tkinter import messagebox as MessageBox
import os
import random
import socket
import re
import time
import threading

global serie_r1_atras; global serie_r2_atras; global serie_r3_atras; global serie_r4_atras; global serie_r5_atras;
global serie_r6_atras;  global serie_r7_atras;  global serie_r8_atras; global serie_r9_atras; global historico
global control_atras; global liquida_total; global series_liquidacion_atras_r1; global control_parpadeo_inicial;
global cliente; global hilo; global total

valor1 = 0; valor2 = 0; valor3 = 0; valor4 = 0; valor5 = 0; valor6 = 0; valor7 = 0; valor8 = 0; valor9 = 0;
totalCar_2 = 0; totalCar_liquidacion = 0; pico_salid_2 = 0; bandera = 0; series_liquidacion_atras_r1 = 0;
serie_r1_atras = 0; control_parpadeo_inicial = 0; historico = 1; de = 0; al = 0; precio = 0; vendidos = 0;
prima = 0; pextra = 0; linea = 0; bingo = 0; total = 0

raiz = Tk()
raiz.title("CAJA MESA CARBI-93")
raiz.attributes('-fullscreen', True)
raiz.config(bg="#000099")

#Comprueba que en el carton de salida no se supere los 1800 y no pongas letras
def validar_entrada(P):
	if P == "":
		return True
	try:
		valor = int(P)
		if valor < 1801:
			return True
		else:
			return False
	except ValueError:
		return False

def establecer_conexion_con_servidor():
	#direccion_pruebas = '127.0.0.1'
	direccion_ballena = '192.168.1.160'
	direccion_auditorio = '192.168.3.160'
	#puerto_prueba = 12345
	puerto_bingo = 1001
	while True:
		try:
			cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cliente.settimeout(2)
			cliente.connect((direccion_ballena, puerto_bingo))
			marca_conexion.config(bg="green", text="CONECTADO")
			return cliente
		except ConnectionRefuseError:
			try:
				cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				cliente.settimeout(2)
				cliente.connect((direccion_auditorio, puerto_bingo))
				marca_conexion.config(bg="green", text="CONECTADO")
				print("conexión auditorio establecida")
				return cliente
			except ConnectionRefuseError:#socket.error as e
				# try:
				# 	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				# 	cliente.settimeout(2)
				# 	cliente.connect((direccion_pruebas, puerto_prueba))
				# 	marca_conexion.config(bg="green", text="CONECTADO")
				# 	print("conexión local establecida")
				# 	return cliente
				# except ConnectionRefuseError:
				cliente.close()
				marca_conexion.config(bg="red", text="SIN CONEXIÓN")
				valor=MessageBox.askquestion("Atención", "Se ha perdido la conexión con la Mesa de Control, espere a que arranque la Mesa de Control y pulse SI para continuar, o pulse NO si quiere salir de la aplicación.")			
				if valor=="yes":
					time.sleep(2)
				else:
					salir()			
			
def comprueba_conexion(cliente):
	while not detener_hilo.is_set():
		#print("No hay datos")
		try:
			#datos = cliente.recv(1024)
			# if not datos:
			# 	raise Exception("Se ha perdido la conexióooon con el servidor.")
			# 	print("No hay datos uno")
			# else:
			#print("No hay datos dos")
			#cliente = establecer_conexion_con_servidor()
			actualizar_datos(cliente)
			time.sleep(2)
		except Exception as e:
			if detener_hilo.is_set():
				break
			time.sleep(1)
			cliente = establecer_conexion_con_servidor()

def actualizar_datos(cliente):
	global linea; global bingo; global prima; global pextra;
	global precio; global de; global al; global vendidos;
	global impresos; global informaticos; global caja; global total

	try:
		elementos = cliente.recv(1024).decode('utf-8')
		#-----------------Linea--------------------
		datos = re.findall(r"R([\d.,]+)", elementos)
		if datos:
			valor_despues_R = datos[-1]

		if "," in valor_despues_R:
			valor_final = valor_despues_R.replace(",", ".")
			linea.set(valor_final)
		else:
			linea.set(valor_despues_R)

		#--------------------Bingo--------------------
		datos = re.findall(r"S([\d.,]+)", elementos)
		if datos:
			valor_despues_S = datos[-1]

		if "," in valor_despues_S:
			valor_final = valor_despues_S.replace(",", ".")
			bingo.set(valor_final)
		else:
			bingo.set(valor_despues_S)			

		#---------------Prima--------------------
		datos = re.findall(r"I([\d.,]+)", elementos)
		if datos:
			valor_despues_I = datos[-1]

		if "," in valor_despues_I:
			valor_final = valor_despues_I.replace(",", ".")
			prima.set(valor_final)
		else:
			prima.set(valor_despues_I)

		#---------------Prima Extra--------------------
		datos = re.findall(r"Y([\d.,]+)", elementos)
		if datos:
			valor_despues_Y = datos[-1]

		if "," in valor_despues_Y:
			valor_final = valor_despues_Y.replace(",", ".")
			pextra.set(valor_final)
		else:
			pextra.set(valor_despues_Y)

		#---------------Precio--------------------
		datos = re.findall(r"N([\d.,]+)", elementos)
		valor_despues_N = 0
		valor_final = 0
		if datos:
			valor_despues_N = datos[-1]

		if "," in valor_despues_N:
			valor_final = valor_despues_N.replace(",", ".")
			precio.set(valor_final)
			total = valor_final
		else:
			precio.set(valor_despues_N)
			total = valor_despues_N

		color_frame_venta()
		
		#---------------Del--------------------
		datos = re.findall(r"L([\d.,]+)", elementos)
		if datos:
			valor_despues_L = datos[-1]

		if "," in valor_despues_L:
			valor_final = valor_despues_L.replace(",", ".")
			de.set(valor_final)
		else:
			de.set(valor_despues_L)

		#---------------Al--------------------
		datos = re.findall(r"M([\d.,]+)", elementos)
		if datos:
			valor_despues_M = datos[-1]

		if "," in valor_despues_M:
			valor_final = valor_despues_M.replace(",", ".")
			al.set(valor_final)
		else:
			al.set(valor_despues_M)

		#---------------Vendidos--------------------
		datos = re.findall(r"O([\d.,]+)", elementos)
		if datos:
			valor_despues_O = datos[-1]

		if "," in valor_despues_O:
			valor_final = valor_despues_O.replace(",", ".")
			vendidos.set(valor_final)
		else:
			vendidos.set(valor_despues_O)

		#---------------Impresos--------------------
		datos = re.findall(r"t([\d.,]+)", elementos)
		if datos:
			valor_despues_t = datos[-1]

		if "," in valor_despues_t:
			valor_final = valor_despues_t.replace(",", ".")
			impresos.set(valor_final)
		else:
			impresos.set(valor_despues_t)

		#---------------Informaticos--------------------
		datos = re.findall(r"g([\d.,]+)", elementos)
		if datos:
			valor_despues_g = datos[-1]

		if "," in valor_despues_g:
			valor_final = valor_despues_g.replace(",", ".")
			informaticos.set(valor_final)
		else:
			informaticos.set(valor_despues_g)

		#---------------Recaudado--------------------
		datos = re.findall(r"u([\d.,]+)", elementos)
		if datos:
			valor_despues_u = datos[-1]

		if "," in valor_despues_u:
			valor_final = valor_despues_u.replace(",", ".")
			recaudado.set(valor_final)
		else:
			recaudado.set(valor_despues_u)

		#--------------- caja --------------------

		if precio.get() == 1:
			caja.set(float(impresos.get() * 1.5 * 0.37))
			salida.set(de.get())
			CartonSalida_1()
			CartonSalida_1_proxima()
		elif precio.get() == 2:
			caja.set(float(impresos.get() * 2 * 0.37))
			salida_2.set(de.get())
			CartonSalida_2()
			CartonSalida_2_proxima()
		elif precio.get() == 3:
			caja.set(float(impresos.get() * 3 * 0.37))
			salida_3.set(de.get())
			CartonSalida_3()
			CartonSalida_3_proxima()
		elif precio.get() == 6:
			caja.set(float(impresos.get() * 6 * 0.37))
			salida_6.set(de.get())
			CartonSalida_6()
			CartonSalida_6_proxima()

		cambiaColor()
	except:
		pass

def color_frame_venta():
	global total

	labels = [label_precio, label_precio_E, label_del, label_impresos, label_recaudado, label_recaudado_E, label_caja, label_caja_E, label_linea,
	label_linea_E, label_vendidos, label_al, label_informaticos, label_bingo, label_bingo_E, label_bingo_E, label_prima_extra, label_prima_extra_E,
	label_prima, label_prima_E]
	if total == "1.50":
		Venta_frame.config(bg="#000099")
		for label in labels:
			label.config(bg="#000099")

	elif total == "2.00":
		Venta_frame.config(bg="#8B0000")#8B0000
		for label in labels:
			label.config(bg="#8B0000")

	elif total == "3.00":
		Venta_frame.config(bg="#FF1493")
		for label in labels:
			label.config(bg="#FF1493")
	elif total == "6.00":
		Venta_frame.config(bg="#2F4F4F")
		for label in labels:
			label.config(bg="#2F4F4F")

def cerrando():
	precio = float(entry_precio.get())
	if precio == 1.5:
		if SalidaEntry_1.get() != entry_del.get() or SalidaEntry_1.get() == "0" or SalidaEntry_1.get() == "":
			MessageBox.showinfo(message="Carton de Salida incorrecto", title="ATENCION")
		else:
			liquida(1.5)
	elif precio == 2:
		if SalidaEntry_2.get() != entry_del.get() or SalidaEntry_2.get() == "0" or SalidaEntry_2.get() == "":
			MessageBox.showinfo(message="Carton de Salida incorrecto", title="ATENCION")
		else:
			liquida(2)
	elif precio == 3:
		if SalidaEntry_3.get() != entry_del.get() or SalidaEntry_3.get() == "0" or SalidaEntry_3.get() == "":
			MessageBox.showinfo(message="Carton de Salida incorrecto", title="ATENCION")
		else:
			liquida(3)
	elif precio == 6:
		if SalidaEntry_6.get() != entry_del.get() or SalidaEntry_6.get() == "0" or SalidaEntry_6.get() == "":
			MessageBox.showinfo(message="Carton de Salida incorrecto", title="ATENCION")
		else:
			liquida(6)
	else:
		MessageBox.showinfo(message="Error en el Precio asignado", title="ATENCION")

def subir_individual(num):
	if num == 1:
		numero_series_rango1.config(text=numero_series1["text"])
	elif num == 2:
		numero_series_rango2.config(text=numero_series2["text"])
	elif num == 3:
		numero_series_rango3.config(text=numero_series3["text"])
	elif num == 4:
		numero_series_rango4.config(text=numero_series4["text"])
	elif num == 5:
		numero_series_rango5.config(text=numero_series5["text"])
	elif num == 6:
		numero_series_rango6.config(text=numero_series6["text"])
	elif num == 7:
		numero_series_rango7.config(text=numero_series7["text"])
	elif num == 8:
		numero_series_rango8.config(text=numero_series8["text"])
	elif num == 9:
		numero_series_rango9.config(text=numero_series9["text"])

	CartonSalida_1()
	CartonSalida_2()
	CartonSalida_3()
	CartonSalida_6()
	cambiaColor()

def datos_historico1():
	liquidacion_historico_1_rango1.config(text=liquidacion_liqui1["text"])
	pico_salida_historico_1_rango_1.config(text=pico_salida_liqui1["text"])
	series_histirico_1_rango_1.config(text=series_liquidacionr1["text"])
	carton_salida_historico_1_rango_1.config(text=carton_salida_liqui1["text"])

	liquidacion_historico_1_rango2.config(text=liquidacion_liqui2["text"])
	series_histirico_1_rango_2.config(text=series_liquidacionr2["text"])
	carton_salida_historico_1_rango_2.config(text=carton_salida_liqui2["text"])

	liquidacion_historico_1_rango3.config(text=liquidacion_liqui3["text"])
	series_histirico_1_rango_3.config(text=series_liquidacionr3["text"])
	carton_salida_historico_1_rango_3.config(text=carton_salida_liqui3["text"])

	liquidacion_historico_1_rango4.config(text=liquidacion_liqui4["text"])
	series_histirico_1_rango_4.config(text=series_liquidacionr4["text"])
	carton_salida_historico_1_rango_4.config(text=carton_salida_liqui4["text"])

	liquidacion_historico_1_rango5.config(text=liquidacion_liqui5["text"])
	series_histirico_1_rango_5.config(text=series_liquidacionr5["text"])
	carton_salida_historico_1_rango_5.config(text=carton_salida_liqui5["text"])

	liquidacion_historico_1_rango6.config(text=liquidacion_liqui6["text"])
	series_histirico_1_rango_6.config(text=series_liquidacionr6["text"])
	carton_salida_historico_1_rango_6.config(text=carton_salida_liqui6["text"])

	liquidacion_historico_1_rango7.config(text=liquidacion_liqui7["text"])
	series_histirico_1_rango_7.config(text=series_liquidacionr7["text"])
	carton_salida_historico_1_rango_7.config(text=carton_salida_liqui7["text"])

	liquidacion_historico_1_rango8.config(text=liquidacion_liqui8["text"])
	series_histirico_1_rango_8.config(text=series_liquidacionr8["text"])
	carton_salida_historico_1_rango_8.config(text=carton_salida_liqui8["text"])

	liquidacion_historico_1_rango9.config(text=liquidacion_liqui9["text"])
	series_histirico_1_rango_9.config(text=series_liquidacionr9["text"])
	carton_salida_historico_1_rango_9.config(text=carton_salida_liqui9["text"])

	liquidacion_historico_1_cierre.config(text=liquidacion_liqui_cierre["text"])
	pico_historico_1_cierre.config(text=pico_cierre_liqui["text"])
	series_historico_1_cierre.config(text=series_liquidacion_cierre["text"])
	carton_salida_historico_1_cierre.config(text=carton_salida_liqui1_cierre["text"])

	liquidacion_historico_1_total.config(text=liquidacion_liqui_total["text"])
	total_series_historico_1.config(text=total_series_liqui["text"])
	total_cartones_historico_1.config(text=entry_impresos.get())

def datos_historico2():
	pico_salida_historico_2_rango_1.config(text=pico_salida_historico_1_rango_1["text"])
	series_histirico_2_rango_1.config(text=series_histirico_1_rango_1["text"])
	carton_salida_historico_2_rango_1.config(text=carton_salida_historico_1_rango_1["text"])

	series_histirico_2_rango_2.config(text=series_histirico_1_rango_2["text"])
	carton_salida_historico_2_rango_2.config(text=carton_salida_historico_1_rango_2["text"])

	series_histirico_2_rango_3.config(text=series_histirico_1_rango_3["text"])
	carton_salida_historico_2_rango_3.config(text=carton_salida_historico_1_rango_3["text"])

	series_histirico_2_rango_4.config(text=series_histirico_1_rango_4["text"])
	carton_salida_historico_2_rango_4.config(text=carton_salida_historico_1_rango_4["text"])

	series_histirico_2_rango_5.config(text=series_histirico_1_rango_5["text"])
	carton_salida_historico_2_rango_5.config(text=carton_salida_historico_1_rango_5["text"])

	series_histirico_2_rango_6.config(text=series_histirico_1_rango_6["text"])
	carton_salida_historico_2_rango_6.config(text=carton_salida_historico_1_rango_6["text"])

	series_histirico_2_rango_7.config(text=series_histirico_1_rango_7["text"])
	carton_salida_historico_2_rango_7.config(text=carton_salida_historico_1_rango_7["text"])

	series_histirico_2_rango_8.config(text=series_histirico_1_rango_8["text"])
	carton_salida_historico_2_rango_8.config(text=carton_salida_historico_1_rango_8["text"])

	series_histirico_2_rango_9.config(text=series_histirico_1_rango_9["text"])
	carton_salida_historico_2_rango_9.config(text=carton_salida_historico_1_rango_9["text"])

	pico_historico_2_cierre.config(text=pico_historico_1_cierre["text"])
	series_historico_2_cierre.config(text=series_historico_1_cierre["text"])
	carton_salida_historico_2_cierre.config(text=carton_salida_historico_1_cierre["text"])

	total_series_historico_2.config(text=total_series_historico_1["text"])
	total_cartones_historico_2.config(text=total_cartones_historico_1["text"])

	datos_historico1()

def datos_historico3():
	pico_salida_historico_3_rango_1.config(text=pico_salida_historico_2_rango_1["text"])
	series_histirico_3_rango_1.config(text=series_histirico_2_rango_1["text"])
	carton_salida_historico_3_rango_1.config(text=carton_salida_historico_2_rango_1["text"])

	series_histirico_3_rango_2.config(text=series_histirico_2_rango_2["text"])
	carton_salida_historico_3_rango_2.config(text=carton_salida_historico_2_rango_2["text"])

	series_histirico_3_rango_3.config(text=series_histirico_2_rango_3["text"])
	carton_salida_historico_3_rango_3.config(text=carton_salida_historico_2_rango_3["text"])

	series_histirico_3_rango_4.config(text=series_histirico_2_rango_4["text"])
	carton_salida_historico_3_rango_4.config(text=carton_salida_historico_2_rango_4["text"])

	series_histirico_3_rango_5.config(text=series_histirico_2_rango_5["text"])
	carton_salida_historico_3_rango_5.config(text=carton_salida_historico_2_rango_5["text"])

	series_histirico_3_rango_6.config(text=series_histirico_2_rango_6["text"])
	carton_salida_historico_3_rango_6.config(text=carton_salida_historico_2_rango_6["text"])

	series_histirico_3_rango_7.config(text=series_histirico_2_rango_7["text"])
	carton_salida_historico_3_rango_7.config(text=carton_salida_historico_2_rango_7["text"])

	series_histirico_3_rango_8.config(text=series_histirico_2_rango_8["text"])
	carton_salida_historico_3_rango_8.config(text=carton_salida_historico_2_rango_8["text"])

	series_histirico_3_rango_9.config(text=series_histirico_2_rango_9["text"])
	carton_salida_historico_3_rango_9.config(text=carton_salida_historico_2_rango_9["text"])

	pico_historico_3_cierre.config(text=pico_historico_2_cierre["text"])
	series_historico_3_cierre.config(text=series_historico_2_cierre["text"])
	carton_salida_historico_3_cierre.config(text=carton_salida_historico_2_cierre["text"])

	total_series_historico_3.config(text=total_series_historico_2["text"])
	total_cartones_historico_3.config(text=total_cartones_historico_2["text"])

	datos_historico2()

def datos_historico4():
	pico_salida_historico_4_rango_1.config(text=pico_salida_historico_3_rango_1["text"])
	series_histirico_4_rango_1.config(text=series_histirico_3_rango_1["text"])
	carton_salida_historico_4_rango_1.config(text=carton_salida_historico_3_rango_1["text"])

	series_histirico_4_rango_2.config(text=series_histirico_3_rango_2["text"])
	carton_salida_historico_4_rango_2.config(text=carton_salida_historico_3_rango_2["text"])

	series_histirico_4_rango_3.config(text=series_histirico_3_rango_3["text"])
	carton_salida_historico_4_rango_3.config(text=carton_salida_historico_3_rango_3["text"])

	series_histirico_4_rango_4.config(text=series_histirico_3_rango_4["text"])
	carton_salida_historico_4_rango_4.config(text=carton_salida_historico_3_rango_4["text"])

	series_histirico_4_rango_5.config(text=series_histirico_3_rango_5["text"])
	carton_salida_historico_4_rango_5.config(text=carton_salida_historico_3_rango_5["text"])

	series_histirico_4_rango_6.config(text=series_histirico_3_rango_6["text"])
	carton_salida_historico_4_rango_6.config(text=carton_salida_historico_3_rango_6["text"])

	series_histirico_4_rango_7.config(text=series_histirico_3_rango_7["text"])
	carton_salida_historico_4_rango_7.config(text=carton_salida_historico_3_rango_7["text"])

	series_histirico_4_rango_8.config(text=series_histirico_3_rango_8["text"])
	carton_salida_historico_4_rango_8.config(text=carton_salida_historico_3_rango_8["text"])

	series_histirico_4_rango_9.config(text=series_histirico_3_rango_9["text"])
	carton_salida_historico_4_rango_9.config(text=carton_salida_historico_3_rango_9["text"])

	pico_historico_4_cierre.config(text=pico_historico_3_cierre["text"])
	series_historico_4_cierre.config(text=series_historico_3_cierre["text"])
	carton_salida_historico_4_cierre.config(text=carton_salida_historico_2_cierre["text"])

	total_series_historico_4.config(text=total_series_historico_3["text"])
	total_cartones_historico_4.config(text=total_cartones_historico_3["text"])

	datos_historico3()

def datos_historico5():
	pico_salida_historico_5_rango_1.config(text=pico_salida_historico_4_rango_1["text"])
	series_histirico_5_rango_1.config(text=series_histirico_4_rango_1["text"])
	carton_salida_historico_5_rango_1.config(text=carton_salida_historico_4_rango_1["text"])

	series_histirico_5_rango_2.config(text=series_histirico_4_rango_2["text"])
	carton_salida_historico_5_rango_2.config(text=carton_salida_historico_4_rango_2["text"])

	series_histirico_5_rango_3.config(text=series_histirico_4_rango_3["text"])
	carton_salida_historico_5_rango_3.config(text=carton_salida_historico_4_rango_3["text"])

	series_histirico_5_rango_4.config(text=series_histirico_4_rango_4["text"])
	carton_salida_historico_5_rango_4.config(text=carton_salida_historico_4_rango_4["text"])

	series_histirico_5_rango_5.config(text=series_histirico_4_rango_5["text"])
	carton_salida_historico_5_rango_5.config(text=carton_salida_historico_4_rango_5["text"])

	series_histirico_5_rango_6.config(text=series_histirico_4_rango_6["text"])
	carton_salida_historico_5_rango_6.config(text=carton_salida_historico_4_rango_6["text"])

	series_histirico_5_rango_7.config(text=series_histirico_4_rango_7["text"])
	carton_salida_historico_5_rango_7.config(text=carton_salida_historico_4_rango_7["text"])

	series_histirico_5_rango_8.config(text=series_histirico_4_rango_8["text"])
	carton_salida_historico_5_rango_8.config(text=carton_salida_historico_4_rango_8["text"])

	series_histirico_5_rango_9.config(text=series_histirico_4_rango_9["text"])
	carton_salida_historico_5_rango_9.config(text=carton_salida_historico_4_rango_9["text"])

	pico_historico_5_cierre.config(text=pico_historico_4_cierre["text"])
	series_historico_5_cierre.config(text=series_historico_4_cierre["text"])
	carton_salida_historico_5_cierre.config(text=carton_salida_historico_4_cierre["text"])

	total_series_historico_5.config(text=total_series_historico_4["text"])
	total_cartones_historico_5.config(text=total_cartones_historico_4["text"])

	datos_historico4()

def datos_historico6():
	pico_salida_historico_6_rango_1.config(text=pico_salida_historico_5_rango_1["text"])
	series_histirico_6_rango_1.config(text=series_histirico_5_rango_1["text"])
	carton_salida_historico_6_rango_1.config(text=carton_salida_historico_5_rango_1["text"])

	series_histirico_6_rango_2.config(text=series_histirico_5_rango_2["text"])
	carton_salida_historico_6_rango_2.config(text=carton_salida_historico_5_rango_2["text"])

	series_histirico_6_rango_3.config(text=series_histirico_5_rango_3["text"])
	carton_salida_historico_6_rango_3.config(text=carton_salida_historico_5_rango_3["text"])

	series_histirico_6_rango_4.config(text=series_histirico_5_rango_4["text"])
	carton_salida_historico_6_rango_4.config(text=carton_salida_historico_5_rango_4["text"])

	series_histirico_6_rango_5.config(text=series_histirico_5_rango_5["text"])
	carton_salida_historico_6_rango_5.config(text=carton_salida_historico_5_rango_5["text"])

	series_histirico_6_rango_6.config(text=series_histirico_5_rango_6["text"])
	carton_salida_historico_6_rango_6.config(text=carton_salida_historico_5_rango_6["text"])

	series_histirico_6_rango_7.config(text=series_histirico_5_rango_7["text"])
	carton_salida_historico_6_rango_7.config(text=carton_salida_historico_5_rango_7["text"])

	series_histirico_6_rango_8.config(text=series_histirico_5_rango_8["text"])
	carton_salida_historico_6_rango_8.config(text=carton_salida_historico_5_rango_8["text"])

	series_histirico_6_rango_9.config(text=series_histirico_5_rango_9["text"])
	carton_salida_historico_6_rango_9.config(text=carton_salida_historico_5_rango_9["text"])

	pico_historico_6_cierre.config(text=pico_historico_5_cierre["text"])
	series_historico_6_cierre.config(text=series_historico_5_cierre["text"])
	carton_salida_historico_6_cierre.config(text=carton_salida_historico_5_cierre["text"])

	total_series_historico_6.config(text=total_series_historico_5["text"])
	total_cartones_historico_6.config(text=total_cartones_historico_5["text"])

	datos_historico5()

def poner_al_frente_raiz():
	raiz.focus_force()

def poner_al_frente_root():
	root.focus_force()

def focus_next_window(event):
	CartonSalida_1()
	SalidaEntry_2.focus()

def focus_next_window_2(event):
	CartonSalida_2()
	SalidaEntry_3.focus()

def focus_next_window_3(event):
	CartonSalida_3()
	SalidaEntry_6.focus()

def focus_next_window_6(event):
	CartonSalida_6()
	boton_cierra.focus()

def reset():
	global control_parpadeo_inicial; global valor1; global valor2; global valor3; global valor4; 
	global valor5; global valor6; global valor7; global valor8; global valor9
	
	salida.set(0); valor1 = 0; valor2 = 0; valor3 = 0; valor4 = 0; valor5 = 0; valor6 = 0
	salida_2.set(0); valor7 = 0; valor8 = 0; valor9 = 0
	salida_3.set(0)
	salida_6.set(0)

	control_parpadeo_inicial = 0
	etiqueta_automatic.pack_forget()
	boton_prepara_rectifica.pack_forget()
	etiqueta_vacia.pack()
	boton_prepara_rectifica.pack()
	boton_prepara_rectifica.config(text="COMENZAR")
	etiquita_instrucciones_inicial.pack()
	parpadeo_inicial(etiquita_instrucciones_inicial)

	numero_series_rango1.config(text=0)
	numero_series_rango2.config(text=0)
	numero_series_rango3.config(text=0)
	numero_series_rango4.config(text=0)
	numero_series_rango5.config(text=0)
	numero_series_rango6.config(text=0)
	numero_series_rango7.config(text=0)
	numero_series_rango8.config(text=0)
	numero_series_rango9.config(text=0)
	CartonSalida_1()
	CartonSalida_2()
	CartonSalida_3()
	CartonSalida_6()
	pico_r1.config(text=0)
	pico_r1_2.config(text=0)
	pico_r1_3.config(text=0)
	pico_r1_6.config(text=0)
	cartones_cierre.config(text=0)
	cartones_cierre_2.config(text=0)
	cartones_cierre_3.config(text=0)
	cartones_cierre_6.config(text=0)
	salida.set("")
	salida_2.set("")
	salida_3.set("")
	salida_6.set("")
	numero_series1.config(text=0)
	numero_series2.config(text=0)
	numero_series3.config(text=0)
	numero_series4.config(text=0)
	numero_series5.config(text=0)
	numero_series6.config(text=0)
	numero_series7.config(text=0)
	numero_series8.config(text=0)
	numero_series9.config(text=0)
	#SalidaEntry_1.focus()

	CartonSalida_1_proxima()
	CartonSalida_2_proxima()
	CartonSalida_3_proxima()
	CartonSalida_6_proxima()

def parpadeo_inicial(etiquita_instrucciones_inicial):
	if control_parpadeo_inicial == 0:
		if etiquita_instrucciones_inicial.cget("foreground") == "red":
			etiquita_instrucciones_inicial.config (foreground="black")
		else:
			etiquita_instrucciones_inicial.config(foreground="red")
		etiquita_instrucciones_inicial.after(1100, parpadeo_inicial, etiquita_instrucciones_inicial)
	else:
		pass

def parpadeo(etiquita_instrucciones):
	if control_parpadeo == 1:
		if etiquita_instrucciones.cget("foreground") == "red":
			etiquita_instrucciones.config (foreground="black")
		else:
			etiquita_instrucciones.config(foreground="red")
		etiquita_instrucciones.after(1100, parpadeo, etiquita_instrucciones)
	else:
		pass

def atras():
	global bandera; global historico
	global control_atras; global serie_r1_atras; global serie_r2_atras; global serie_r3_atras; global serie_r4_atras;
	global serie_r5_atras; global serie_r6_atras; global serie_r7_atras; global serie_r8_atras; global serie_r9_atras;
	global series_liquidacion_atras_r1; global control_parpadeo

	control_parpadeo = 1
	etiquita_instrucciones.pack()
	etiquita_instrucciones.config(foreground="black", background="#31BFE4")
	parpadeo(etiquita_instrucciones)

	historico = 0
	bandera = 1

	serie_r1_atras = numero_series_rango1["text"]
	serie_r2_atras = numero_series_rango2["text"]
	serie_r3_atras = numero_series_rango3["text"]
	serie_r4_atras = numero_series_rango4["text"]
	serie_r5_atras = numero_series_rango5["text"]
	serie_r6_atras = numero_series_rango6["text"]
	serie_r7_atras = numero_series_rango7["text"]
	serie_r8_atras = numero_series_rango8["text"]
	serie_r9_atras = numero_series_rango9["text"]

	boton_atras['state'] = DISABLED

	if control_atras == 1:
		salida.set(entry_del.get())
	elif control_atras == 2:
		salida_2.set(entry_del.get())
	elif control_atras == 3:
		salida_3.set(entry_del.get())
	else:
		salida_6.set(entry_del.get())

	liquidacion_atras()
	CartonSalida_1()
	CartonSalida_1_proxima()
	CartonSalida_2()
	CartonSalida_2_proxima()
	CartonSalida_3()
	CartonSalida_3_proxima()
	CartonSalida_6()
	CartonSalida_6_proxima()

def PreparaRectifica():
	global bandera
	global serie_r1_atras; global serie_r2_atras; global serie_r3_atras; global serie_r4_atras;
	global serie_r5_atras; global serie_r6_atras; global serie_r7_atras; global serie_r8_atras; global serie_r9_atras;
	global control_parpadeo_inicial
    
	valor_atras = 1
	etiqueta_vacia.pack_forget()
	boton_prepara_rectifica.pack_forget()
	etiqueta_automatic.pack()
	boton_prepara_rectifica.pack()
	boton_prepara_rectifica.config(text="SUBIR TODOS")
	etiquita_instrucciones_inicial.pack_forget()
	etiquita_instrucciones.pack_forget()
	control_parpadeo_inicial = 1

	if bandera == 1:
		numero_series_rango1.config(text=serie_r1_atras)
		numero_series_rango2.config(text=serie_r2_atras)
		numero_series_rango3.config(text=serie_r3_atras)
		numero_series_rango4.config(text=serie_r4_atras)
		numero_series_rango5.config(text=serie_r5_atras)
		numero_series_rango6.config(text=serie_r6_atras)
		numero_series_rango7.config(text=serie_r7_atras)
		numero_series_rango8.config(text=serie_r8_atras)
		numero_series_rango9.config(text=serie_r9_atras)
	else:
		numero_series_rango1.config(text=numero_series1["text"], fg = "blue")
		numero_series_rango2.config(text=numero_series2["text"], fg = "blue")
		numero_series_rango3.config(text=numero_series3["text"], fg = "blue")
		numero_series_rango4.config(text=numero_series4["text"], fg = "blue")
		numero_series_rango5.config(text=numero_series5["text"], fg = "blue")
		numero_series_rango6.config(text=numero_series6["text"], fg = "blue")
		numero_series_rango7.config(text=numero_series7["text"], fg = "blue")
		numero_series_rango8.config(text=numero_series8["text"], fg = "blue")
		numero_series_rango9.config(text=numero_series9["text"], fg = "blue")

	CartonSalida_1()
	CartonSalida_2()
	CartonSalida_3()
	CartonSalida_6()
	cambiaColor()

	bandera = 0

def liquidacion_atras():
	numero_series_rango1.config(text=series_liquidacionr1["text"])
	numero_series_rango2.config(text=series_liquidacionr2["text"])
	numero_series_rango3.config(text=series_liquidacionr3["text"])
	numero_series_rango4.config(text=series_liquidacionr4["text"])
	numero_series_rango5.config(text=series_liquidacionr5["text"])
	numero_series_rango6.config(text=series_liquidacionr6["text"])
	numero_series_rango7.config(text=series_liquidacionr7["text"])
	numero_series_rango8.config(text=series_liquidacionr8["text"])
	numero_series_rango9.config(text=series_liquidacionr9["text"])

	series_liquidacionr1.config(text=series_liquidacion_atras_r1)
	series_liquidacionr2.config(text=series_liquidacion_atras_r2)
	series_liquidacionr3.config(text=series_liquidacion_atras_r3)
	series_liquidacionr4.config(text=series_liquidacion_atras_r4)
	series_liquidacionr5.config(text=series_liquidacion_atras_r5)
	series_liquidacionr6.config(text=series_liquidacion_atras_r6)
	series_liquidacionr7.config(text=series_liquidacion_atras_r7)
	series_liquidacionr8.config(text=series_liquidacion_atras_r8)
	series_liquidacionr9.config(text=series_liquidacion_atras_r9)
	series_liquidacion_cierre.config(text=series_liquidacion_atras_cierre)

	total_series_liqui.config(text=series_liquidacion_atras_total)
	pico_salida_liqui1.config(text=pico_salida_liqui1_atras)
	pico_cierre_liqui.config(text=pico_cierre_liqui_atras)

	carton_salida_liqui1.config(text=carton_salida_liqui1_atras)
	carton_salida_liqui2.config(text=carton_salida_liqui2_atras)
	carton_salida_liqui3.config(text=carton_salida_liqui3_atras)
	carton_salida_liqui4.config(text=carton_salida_liqui4_atras)
	carton_salida_liqui5.config(text=carton_salida_liqui5_atras)
	carton_salida_liqui6.config(text=carton_salida_liqui6_atras)
	carton_salida_liqui7.config(text=carton_salida_liqui7_atras)
	carton_salida_liqui8.config(text=carton_salida_liqui8_atras)
	carton_salida_liqui9.config(text=carton_salida_liqui9_atras)
	carton_salida_liqui1_cierre.config(text=carton_salida_liqui1_cierre_atras)

	labels = [series_liquidacionr1, series_liquidacionr2,series_liquidacionr3,series_liquidacionr4,series_liquidacionr5,series_liquidacionr6,
		series_liquidacionr7,series_liquidacionr8,series_liquidacionr9,series_liquidacion_cierre,total_series_liqui,pico_salida_liqui1,
		pico_cierre_liqui,carton_salida_liqui1,carton_salida_liqui2,carton_salida_liqui3,carton_salida_liqui4,carton_salida_liqui5,
		carton_salida_liqui6,carton_salida_liqui7,carton_salida_liqui8,carton_salida_liqui9,carton_salida_liqui1_cierre]
	
	for label in labels:
		label.config(fg="black")

	liquidacion_liqui1.config(text=liquidacion_liqui1_atras)
	liquidacion_liqui2.config(text=liquidacion_liqui2_atras)
	liquidacion_liqui3.config(text=liquidacion_liqui3_atras)
	liquidacion_liqui4.config(text=liquidacion_liqui4_atras)
	liquidacion_liqui5.config(text=liquidacion_liqui5_atras)
	liquidacion_liqui6.config(text=liquidacion_liqui6_atras)
	liquidacion_liqui7.config(text=liquidacion_liqui7_atras)
	liquidacion_liqui8.config(text=liquidacion_liqui8_atras)
	liquidacion_liqui9.config(text=liquidacion_liqui9_atras)
	liquidacion_liqui_cierre.config(text=liquidacion_liqui_cierre_atras)
	liquidacion_liqui_total.config(text=liquidacion_liqui_total_atras)

def salir():
	global hilo_actualizacion, cliente
	if MessageBox.askquestion("Salir", "¿Deseas salir de la aplicación?") == "yes":
		detener_hilo.set()
		if cliente:
			cliente.close()
	try:
		ruta_ejecutable = r"C:\CajaMesaControl\Menu\Menu.exe"
		os.startfile(ruta_ejecutable)
	except:
		pass
	if raiz:
		raiz.destroy()

def incrementar(num):
	global valor1; global valor2; global valor3; global valor4; global valor5
	global valor6; global valor7; global valor8; global valor9

	if num == 1:
		valor1 = valor1 + 1
		numero_series1.config(text=valor1)
	if num == 2:
		valor2 = valor2 + 1
		numero_series2.config(text=valor2) 
	if num == 3:
		valor3 = valor3 + 1
		numero_series3.config(text=valor3)
	if num == 4:
		valor4 = valor4 + 1
		numero_series4.config(text=valor4)
	if num == 5:
		valor5 = valor5 + 1
		numero_series5.config(text=valor5)
	if num == 6:
		valor6 = valor6 + 1
		numero_series6.config(text=valor6)
	if num == 7:
		valor7 = valor7 + 1
		numero_series7.config(text=valor7)
	if num == 8:
		valor8 = valor8 + 1
		numero_series8.config(text=valor8)
	if num == 9:
		valor9 = valor9 + 1
		numero_series9.config(text=valor9)

	CartonSalida_1_proxima()
	CartonSalida_2_proxima()
	CartonSalida_3_proxima()
	CartonSalida_6_proxima()

def decrementar(num):
	global valor1; global valor2; global valor3; global valor4; global valor5
	global valor6; global valor7; global valor8; global valor9
	
	if num == 1 :
		if valor1 == 0 :
	 		numero_series1.config(text=valor1)
		else:
			valor1 = valor1 - 1
			numero_series1.config(text=valor1)
	if num == 2 :
		if valor2 == 0 :
	 		numero_series2.config(text=valor2)
		else:
			valor2 = valor2 - 1
			numero_series2.config(text=valor2)
	if num == 3:
		if valor3 == 0 :
	 		numero_series3.config(text=valor3)
		else:
			valor3 = valor3 - 1
			numero_series3.config(text=valor3)
	if num == 4:
		if valor4 == 0 :
	 		numero_series4.config(text=valor4)
		else:
			valor4 = valor4 - 1
			numero_series4.config(text=valor4)
	if num == 5:
		if valor5 == 0 :
	 		numero_series5.config(text=valor5)
		else:
			valor5 = valor5 - 1
			numero_series5.config(text=valor5)
	if num == 6:
		if valor6 == 0 :
	 		numero_series6.config(text=valor6)
		else:
			valor6 = valor6 - 1
			numero_series6.config(text=valor6)
	if num == 7:
		if valor7 == 0 :
	 		numero_series7.config(text=valor7)
		else:
			valor7 = valor7 - 1
			numero_series7.config(text=valor7)
	if num == 8:
		if valor8 == 0 :
	 		numero_series8.config(text=valor8)
		else:
			valor8 = valor8 - 1
			numero_series8.config(text=valor8)
	if num == 9:
		if valor9 == 0 :
	 		numero_series9.config(text=valor9)
		else:
			valor9 = valor9 - 1
			numero_series9.config(text=valor9)

	CartonSalida_1_proxima()
	CartonSalida_2_proxima()
	CartonSalida_3_proxima()
	CartonSalida_6_proxima()

def pico_salida_1():
	try:
		if int(SalidaEntry_1.get()) == 0 or SalidaEntry_1.get() == "":
			pass
		else:
			pico_sal_1 = 7 - (int(SalidaEntry_1.get()) % 6)
			if pico_sal_1 == 7:
				return 1
			elif pico_sal_1 == 6:
				return 0
			else:
				return pico_sal_1
	except:
		pass

def pico_salid_2():
	try:
		if int(SalidaEntry_2.get()) == 0 or SalidaEntry_2.get() == "":
			pass
		else:
			pico_sal_2 = 7 - (int(SalidaEntry_2.get()) % 6)
			if pico_sal_2 == 7:
				return 1
			elif pico_sal_2 == 6:
				return 0
			else:
				return pico_sal_2
	except:
		pass

def pico_salid_3():
	try:
		if int(SalidaEntry_3.get()) == 0 or SalidaEntry_3.get() == "":
			pass
		else:
			pico_sal_3 = 7 - (int(SalidaEntry_3.get()) % 6)
			if pico_sal_3 == 7:
				return 1
			elif pico_sal_3 == 6:
				return 0
			else:
				return pico_sal_3
	except:
		pass

def pico_salid_6():
	try:
		if int(SalidaEntry_6.get()) == 0 or SalidaEntry_6.get() == "":
			pass
		else:
			pico_sal_6 = 7 - (int(SalidaEntry_6.get()) % 6)
			if pico_sal_6 == 7:
				return 1
			elif pico_sal_6 == 6:
				return 0
			else:
				return pico_sal_6
	except:
		pass

def pico_salida_liquidacion():
	try:
		if int(entry_del.get()) == 0 or int(entry_del.get()) == "":
			pass
		else:
			pico_sal_liquidacion = 7 - (int(entry_del.get()) % 6)
			if pico_sal_liquidacion == 7:
				return 1
			elif pico_sal_liquidacion == 6:
				return 0
			else:
				return pico_sal_liquidacion
	except:
		pass

def pico_cierre():
	try:
		if int(entry_al.get()) == 0 or int(entry_al.get()) == "":
			pass
		else:
			pico_cie = (int(entry_al.get()) % 6)
			pico_cierre_liqui.config(text = pico_cie)
			return pico_cie
	except:
		pass

def CartonSalida_1():
	pico_salida = pico_salida_1()

	cambiaColor()	

	try:
		if SalidaEntry_1.get() == "":
			pass
		else:
			CarSalR = SalidaEntry_1.get()
			CarSalR1 = int(CarSalR)
			pico_r1.config(text=pico_salida)

			#----Rango 2-----

			if int(numero_series_rango2["text"]) == 0 :
				cartones_r2.config(text=0)
			else:
				CarSalR2 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6)
				if CarSalR2 > 1800:
					cartones_r2.config(text=CarSalR2 - 1800)
				else:
					cartones_r2.config(text=CarSalR2)
				
			#----Rango 3-----

			if int(numero_series_rango3["text"]) == 0 :
				cartones_r3.config(text=0)
			else:
				CarSalR3 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6)
				if CarSalR3 > 1800:
					cartones_r3.config(text=CarSalR3 - 1800)
				else:
					cartones_r3.config(text=CarSalR3)

			#----Rango 4-----

			if int(numero_series_rango4["text"]) == 0 :
				cartones_r4.config(text=0)
			else:
				CarSalR4 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6)
				if CarSalR4 > 1800:
					cartones_r4.config(text=CarSalR4 - 1800)
				else:
					cartones_r4.config(text=CarSalR4)

			#----Rango 5-----

			if int(numero_series_rango5["text"]) == 0 :
				cartones_r5.config(text=0)
			else:
				CarSalR5 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6)
				if CarSalR5 > 1800:
					cartones_r5.config(text=CarSalR5 - 1800)
				else:
					cartones_r5.config(text=CarSalR5)

			#----Rango 6-----

			if int(numero_series_rango6["text"]) == 0 :
				cartones_r6.config(text=0)
			else:
				CarSalR6 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6)
				if CarSalR6 > 1800:
					cartones_r6.config(text=CarSalR6 - 1800)
				else:
					cartones_r6.config(text=CarSalR6)

			#----Rango 7-----

			if int(numero_series_rango7["text"]) == 0 :
				cartones_r7.config(text=0)
			else:
				CarSalR7 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6)
				if CarSalR7 > 1800:
					cartones_r7.config(text=CarSalR7 - 1800)
				else:
					cartones_r7.config(text=CarSalR7)

			#----Rango 8-----

			if int(numero_series_rango8["text"]) == 0 :
				cartones_r8.config(text=0)
			else:
				CarSalR8 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6)
				if CarSalR8 > 1800:
					cartones_r8.config(text=CarSalR8 - 1800)
				else:
					cartones_r8.config(text=CarSalR8)

			#----Rango 9-----

			if int(numero_series_rango9["text"]) == 0 :
				cartones_r9.config(text=0)
			else:
				CarSalR9 = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6)
				if CarSalR9 > 1800:
					cartones_r9.config(text=CarSalR9 - 1800)
				else:
					cartones_r9.config(text=CarSalR9)

			#----Rango cierre-----

			CarSalCie = int(CarSalR1) + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
			if CarSalCie > 1800:
				cartones_cierre.config(text=CarSalCie - 1800)
			else:
				cartones_cierre.config(text=CarSalCie)
	except:
		pass

def CartonSalida_1_proxima():
	pico_salida = pico_salida_1()	

	try:
		if SalidaEntry_1.get() == "":
			cartones_r2_proxima.config(text=0)
			cartones_r3_proxima.config(text=0)
			cartones_r4_proxima.config(text=0)
			cartones_r5_proxima.config(text=0)
			cartones_r6_proxima.config(text=0)
			cartones_r7_proxima.config(text=0)
			cartones_r8_proxima.config(text=0)
			cartones_r9_proxima.config(text=0)
			cartones_cierre_proxima.config(text=0)
		else:
			CarSalR = SalidaEntry_1.get()
			CarSalR1 = int(CarSalR)
			pico_r1.config(text=pico_salida)

			#----Rango 2-----

			if int(numero_series2["text"]) == 0 :
				cartones_r2_proxima.config(text=0)
			else:
				CarSalR2 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6)
				if CarSalR2 > 1800:
					cartones_r2_proxima.config(text=CarSalR2 - 1800)
				else:
					cartones_r2_proxima.config(text=CarSalR2)
				
			#----Rango 3-----

			if int(numero_series3["text"]) == 0 :
				cartones_r3_proxima.config(text=0)
			else:
				CarSalR3 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6)
				if CarSalR3 > 1800:
					cartones_r3_proxima.config(text=CarSalR3 - 1800)
				else:
					cartones_r3_proxima.config(text=CarSalR3)

			#----Rango 4-----

			if int(numero_series4["text"]) == 0 :
				cartones_r4_proxima.config(text=0)
			else:
				CarSalR4 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6)
				if CarSalR4 > 1800:
					cartones_r4_proxima.config(text=CarSalR4 - 1800)
				else:
					cartones_r4_proxima.config(text=CarSalR4)

			#----Rango 5-----

			if int(numero_series5["text"]) == 0 :
				cartones_r5_proxima.config(text=0)
			else:
				CarSalR5 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6)
				if CarSalR5 > 1800:
					cartones_r5_proxima.config(text=CarSalR5 - 1800)
				else:
					cartones_r5_proxima.config(text=CarSalR5)

			#----Rango 6-----

			if int(numero_series6["text"]) == 0 :
				cartones_r6_proxima.config(text=0)
			else:
				CarSalR6 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6)
				if CarSalR6 > 1800:
					cartones_r6_proxima.config(text=CarSalR6 - 1800)
				else:
					cartones_r6_proxima.config(text=CarSalR6)

			#----Rango 7-----

			if int(numero_series7["text"]) == 0 :
				cartones_r7_proxima.config(text=0)
			else:
				CarSalR7 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6)
				if CarSalR7 > 1800:
					cartones_r7_proxima.config(text=CarSalR7 - 1800)
				else:
					cartones_r7_proxima.config(text=CarSalR7)

			#----Rango 8-----

			if int(numero_series8["text"]) == 0 :
				cartones_r8_proxima.config(text=0)
			else:
				CarSalR8 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6)
				if CarSalR8 > 1800:
					cartones_r8_proxima.config(text=CarSalR8 - 1800)
				else:
					cartones_r8_proxima.config(text=CarSalR8)

			#----Rango 9-----

			if int(numero_series9["text"]) == 0 :
				cartones_r9_proxima.config(text=0)
			else:
				CarSalR9 = CarSalR1 + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6)
				if CarSalR9 > 1800:
					cartones_r9_proxima.config(text=CarSalR9 - 1800)
				else:
					cartones_r9_proxima.config(text=CarSalR9)

			#----Rango cierre-----

			CarSalCie = int(CarSalR1) + pico_salida + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6) + (int(numero_series9["text"]) * 6)
			if CarSalCie > 1800:
				cartones_cierre_proxima.config(text=CarSalCie - 1800)
			else:
				cartones_cierre_proxima.config(text=CarSalCie)
	except:
		pass

def CartonSalida_2():
	pico_salida_2 = pico_salid_2()

	try:
		if SalidaEntry_2.get() == "":
			pass
		else:
			CarSalR1 = SalidaEntry_2.get()
			CarSalR1_2 = int(CarSalR1)
			pico_r1_2.config(text=pico_salida_2)

			#----Rango 2-----

			if int(numero_series_rango2["text"]) == 0 :
				cartones_r2_2.config(text=0)
			else:
				CarSalR2_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) #
				if CarSalR2_2 > 1800:
					cartones_r2_2.config(text=CarSalR2_2 - 1800)
				else:
					cartones_r2_2.config(text=CarSalR2_2)
				
			#----Rango 3-----

			if int(numero_series_rango3["text"]) == 0 :
				cartones_r3_2.config(text=0)
			else:
				CarSalR3_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6)
				if CarSalR3_2 > 1800:
					cartones_r3_2.config(text=CarSalR3_2 - 1800)
				else:
					cartones_r3_2.config(text=CarSalR3_2)

			#----Rango 4-----

			if int(numero_series_rango4["text"]) == 0 :
				cartones_r4_2.config(text=0)
			else:
				CarSalR4_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6)
				if CarSalR4_2 > 1800:
					cartones_r4_2.config(text=CarSalR4_2 - 1800)
				else:
					cartones_r4_2.config(text=CarSalR4_2)

			#----Rango 5-----

			if int(numero_series_rango5["text"]) == 0 :
				cartones_r5_2.config(text=0)
			else:
				CarSalR5_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6)
				if CarSalR5_2 > 1800:
					cartones_r5_2.config(text=CarSalR5_2 - 1800)
				else:
					cartones_r5_2.config(text=CarSalR5_2)

			#----Rango 6-----

			if int(numero_series_rango6["text"]) == 0 :
				cartones_r6_2.config(text=0)
			else:
				CarSalR6_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6)
				if CarSalR6_2 > 1800:
					cartones_r6_2.config(text=CarSalR6_2 - 1800)
				else:
					cartones_r6_2.config(text=CarSalR6_2)

			#----Rango 7-----

			if int(numero_series_rango7["text"]) == 0 :
				cartones_r7_2.config(text=0)
			else:
				CarSalR7_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6)
				if CarSalR7_2 > 1800:
					cartones_r7_2.config(text=CarSalR7_2 - 1800)
				else:
					cartones_r7_2.config(text=CarSalR7_2)

			#----Rango 8-----

			if int(numero_series_rango8["text"]) == 0 :
				cartones_r8_2.config(text=0)
			else:
				CarSalR8_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6)
				if CarSalR8_2 > 1800:
					cartones_r8_2.config(text=CarSalR8_2 - 1800)
				else:
					cartones_r8_2.config(text=CarSalR8_2)

			#----Rango 9-----

			if int(numero_series_rango9["text"]) == 0 :
				cartones_r9_2.config(text=0)
			else:
				CarSalR9_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6)
				if CarSalR9_2 > 1800:
					cartones_r9_2.config(text=CarSalR9_2 - 1800)
				else:
					cartones_r9_2.config(text=CarSalR9_2)

			#----Rango cierre-----

			CarSalCie_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
			if CarSalCie_2 > 1800:
				cartones_cierre_2.config(text=CarSalCie_2 - 1800)
			else:
				cartones_cierre_2.config(text=CarSalCie_2)
	except:
		pass

def CartonSalida_2_proxima():
	pico_salida_2 = pico_salid_2()

	#cambiaColor()	

	try:
		if SalidaEntry_2.get() == "":
			cartones_r2_2_proxima.config(text=0)
			cartones_r3_2_proxima.config(text=0)
			cartones_r4_2_proxima.config(text=0)
			cartones_r5_2_proxima.config(text=0)
			cartones_r6_2_proxima.config(text=0)
			cartones_r7_2_proxima.config(text=0)
			cartones_r8_2_proxima.config(text=0)
			cartones_r9_2_proxima.config(text=0)
			cartones_cierre_2_proxima.config(text=0)
		else:
			CarSalR1 = SalidaEntry_2.get()
			CarSalR1_2 = int(CarSalR1)
			pico_r1_2.config(text=pico_salida_2)

			#----Rango 2-----

			if int(numero_series2["text"]) == 0 :
				cartones_r2_2_proxima.config(text=0)
			else:
				CarSalR2 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6)
				if CarSalR2 > 1800:
					cartones_r2_2_proxima.config(text=CarSalR2 - 1800)
				else:
					cartones_r2_2_proxima.config(text=CarSalR2)
				
			#----Rango 3-----

			if int(numero_series3["text"]) == 0 :
				cartones_r3_2_proxima.config(text=0)
			else:
				CarSalR3 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6)
				if CarSalR3 > 1800:
					cartones_r3_2_proxima.config(text=CarSalR3 - 1800)
				else:
					cartones_r3_2_proxima.config(text=CarSalR3)

			#----Rango 4-----

			if int(numero_series4["text"]) == 0 :
				cartones_r4_2_proxima.config(text=0)
			else:
				CarSalR4 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6)
				if CarSalR4 > 1800:
					cartones_r4_2_proxima.config(text=CarSalR4 - 1800)
				else:
					cartones_r4_2_proxima.config(text=CarSalR4)

			#----Rango 5-----

			if int(numero_series5["text"]) == 0 :
				cartones_r5_2_proxima.config(text=0)
			else:
				CarSalR5 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6)
				if CarSalR5 > 1800:
					cartones_r5_2_proxima.config(text=CarSalR5 - 1800)
				else:
					cartones_r5_2_proxima.config(text=CarSalR5)

			#----Rango 6-----

			if int(numero_series6["text"]) == 0 :
				cartones_r6_2_proxima.config(text=0)
			else:
				CarSalR6 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6)
				if CarSalR6 > 1800:
					cartones_r6_2_proxima.config(text=CarSalR6 - 1800)
				else:
					cartones_r6_2_proxima.config(text=CarSalR6)

			#----Rango 7-----

			if int(numero_series7["text"]) == 0 :
				cartones_r7_2_proxima.config(text=0)
			else:
				CarSalR7 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6)
				if CarSalR7 > 1800:
					cartones_r7_2_proxima.config(text=CarSalR7 - 1800)
				else:
					cartones_r7_2_proxima.config(text=CarSalR7)

			#----Rango 8-----

			if int(numero_series8["text"]) == 0 :
				cartones_r8_2_proxima.config(text=0)
			else:
				CarSalR8 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6)
				if CarSalR8 > 1800:
					cartones_r8_2_proxima.config(text=CarSalR8 - 1800)
				else:
					cartones_r8_2_proxima.config(text=CarSalR8)

			#----Rango 9-----

			if int(numero_series9["text"]) == 0 :
				cartones_r9_2_proxima.config(text=0)
			else:
				CarSalR9 = CarSalR1_2 + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6)
				if CarSalR9 > 1800:
					cartones_r9_2_proxima.config(text=CarSalR9 - 1800)
				else:
					cartones_r9_2_proxima.config(text=CarSalR9)

			#----Rango cierre-----

			CarSalCie = int(CarSalR1_2) + pico_salida_2 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6) + (int(numero_series9["text"]) * 6)
			if CarSalCie > 1800:
				cartones_cierre_2_proxima.config(text=CarSalCie - 1800)
			else:
				cartones_cierre_2_proxima.config(text=CarSalCie)
	except:
		pass

def CartonSalida_3():
	pico_salida_3 = pico_salid_3()

	try:
		if SalidaEntry_3.get() == "":
			pass
		else:
			CarSalR1 = SalidaEntry_3.get()
			CarSalR1_3 = int(CarSalR1)
			pico_r1_3.config(text=pico_salida_3)

			#----Rango 2-----

			if int(numero_series_rango2["text"]) == 0 :
				cartones_r2_3.config(text=0)
			else:
				CarSalR2_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) #
				if CarSalR2_3 > 1800:
					cartones_r2_3.config(text=CarSalR2_3 - 1800)
				else:
					cartones_r2_3.config(text=CarSalR2_3)
				
			#----Rango 3-----

			if int(numero_series_rango3["text"]) == 0 :
				cartones_r3_3.config(text=0)
			else:
				CarSalR3_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6)
				if CarSalR3_3 > 1800:
					cartones_r3_3.config(text=CarSalR3_3 - 1800)
				else:
					cartones_r3_3.config(text=CarSalR3_3)

			#----Rango 4-----

			if int(numero_series_rango4["text"]) == 0 :
				cartones_r4_3.config(text=0)
			else:
				CarSalR4_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6)
				if CarSalR4_3 > 1800:
					cartones_r4_3.config(text=CarSalR4_3 - 1800)
				else:
					cartones_r4_3.config(text=CarSalR4_3)

			#----Rango 5-----

			if int(numero_series_rango5["text"]) == 0 :
				cartones_r5_3.config(text=0)
			else:
				CarSalR5_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6)
				if CarSalR5_3 > 1800:
					cartones_r5_3.config(text=CarSalR5_3 - 1800)
				else:
					cartones_r5_3.config(text=CarSalR5_3)

			#----Rango 6-----

			if int(numero_series_rango6["text"]) == 0 :
				cartones_r6_3.config(text=0)
			else:
				CarSalR6_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6)
				if CarSalR6_3 > 1800:
					cartones_r6_3.config(text=CarSalR6_3 - 1800)
				else:
					cartones_r6_3.config(text=CarSalR6_3)

			#----Rango 7-----

			if int(numero_series_rango7["text"]) == 0 :
				cartones_r7_3.config(text=0)
			else:
				CarSalR7_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6)
				if CarSalR7_3 > 1800:
					cartones_r7_3.config(text=CarSalR7_3 - 1800)
				else:
					cartones_r7_3.config(text=CarSalR7_3)

			#----Rango 8-----

			if int(numero_series_rango8["text"]) == 0 :
				cartones_r8_3.config(text=0)
			else:
				CarSalR8_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6)
				if CarSalR8_3 > 1800:
					cartones_r8_3.config(text=CarSalR8_3 - 1800)
				else:
					cartones_r8_3.config(text=CarSalR8_3)

			#----Rango 9-----

			if int(numero_series_rango9["text"]) == 0 :
				cartones_r9_3.config(text=0)
			else:
				CarSalR9_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6)
				if CarSalR9_3 > 1800:
					cartones_r9_3.config(text=CarSalR9_3 - 1800)
				else:
					cartones_r9_3.config(text=CarSalR9_3)

			#----Rango cierre-----

			CarSalCie_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
				
			if CarSalCie_3 > 1800:
				cartones_cierre_3.config(text=CarSalCie_3 - 1800)
			else:
				cartones_cierre_3.config(text=CarSalCie_3)
	except:
		pass

def CartonSalida_3_proxima():
	pico_salida_3 = pico_salid_3()

	try:
		if SalidaEntry_3.get() == "":
			cartones_r2_3_proxima.config(text=0)
			cartones_r3_3_proxima.config(text=0)
			cartones_r4_3_proxima.config(text=0)
			cartones_r5_3_proxima.config(text=0)
			cartones_r6_3_proxima.config(text=0)
			cartones_r7_3_proxima.config(text=0)
			cartones_r8_3_proxima.config(text=0)
			cartones_r9_3_proxima.config(text=0)
			cartones_cierre_3_proxima.config(text=0)
		else:
			CarSalR1 = SalidaEntry_3.get()
			CarSalR1_3 = int(CarSalR1)
			pico_r1_3.config(text=pico_salida_3)

			#----Rango 2-----

			if int(numero_series2["text"]) == 0 :
				cartones_r2_3_proxima.config(text=0)
			else:
				CarSalR2 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6)
				if CarSalR2 > 1800:
					cartones_r2_3_proxima.config(text=CarSalR2 - 1800)
				else:
					cartones_r2_3_proxima.config(text=CarSalR2)
				
			#----Rango 3-----

			if int(numero_series3["text"]) == 0 :
				cartones_r3_3_proxima.config(text=0)
			else:
				CarSalR3 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6)
				if CarSalR3 > 1800:
					cartones_r3_3_proxima.config(text=CarSalR3 - 1800)
				else:
					cartones_r3_3_proxima.config(text=CarSalR3)

			#----Rango 4-----

			if int(numero_series4["text"]) == 0 :
				cartones_r4_3_proxima.config(text=0)
			else:
				CarSalR4 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6)
				if CarSalR4 > 1800:
					cartones_r4_3_proxima.config(text=CarSalR4 - 1800)
				else:
					cartones_r4_3_proxima.config(text=CarSalR4)

			#----Rango 5-----

			if int(numero_series5["text"]) == 0 :
				cartones_r5_3_proxima.config(text=0)
			else:
				CarSalR5 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6)
				if CarSalR5 > 1800:
					cartones_r5_3_proxima.config(text=CarSalR5 - 1800)
				else:
					cartones_r5_3_proxima.config(text=CarSalR5)

			#----Rango 6-----

			if int(numero_series6["text"]) == 0 :
				cartones_r6_3_proxima.config(text=0)
			else:
				CarSalR6 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6)
				if CarSalR6 > 1800:
					cartones_r6_3_proxima.config(text=CarSalR6 - 1800)
				else:
					cartones_r6_3_proxima.config(text=CarSalR6)

			#----Rango 7-----

			if int(numero_series7["text"]) == 0 :
				cartones_r7_3_proxima.config(text=0)
			else:
				CarSalR7 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6)
				if CarSalR7 > 1800:
					cartones_r7_3_proxima.config(text=CarSalR7 - 1800)
				else:
					cartones_r7_3_proxima.config(text=CarSalR7)

			#----Rango 8-----

			if int(numero_series8["text"]) == 0 :
				cartones_r8_3_proxima.config(text=0)
			else:
				CarSalR8 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6)
				if CarSalR8 > 1800:
					cartones_r8_3_proxima.config(text=CarSalR8 - 1800)
				else:
					cartones_r8_3_proxima.config(text=CarSalR8)

			#----Rango 9-----

			if int(numero_series9["text"]) == 0 :
				cartones_r9_3_proxima.config(text=0)
			else:
				CarSalR9 = CarSalR1_3 + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6)
				if CarSalR9 > 1800:
					cartones_r9_3_proxima.config(text=CarSalR9 - 1800)
				else:
					cartones_r9_3_proxima.config(text=CarSalR9)

			#----Rango cierre-----

			CarSalCie = int(CarSalR1_3) + pico_salida_3 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6) + (int(numero_series9["text"]) * 6)
			if CarSalCie > 1800:
				cartones_cierre_3_proxima.config(text=CarSalCie - 1800)
			else:
				cartones_cierre_3_proxima.config(text=CarSalCie)
	except:
		pass

def CartonSalida_6():
	pico_salida_6 = pico_salid_6()

	try:
		if SalidaEntry_6.get() == "":
			pass
		else:
			CarSalR1 = int(SalidaEntry_6.get())
			CarSalR1_6 = int(CarSalR1)
			pico_r1_6.config(text=pico_salida_6)

			#----Rango 2-----

			if int(numero_series_rango2["text"]) == 0 :
				cartones_r2_6.config(text=0)
			else:
				CarSalR2_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) #
				if CarSalR2_6 > 1800:
					cartones_r2_6.config(text=CarSalR2_6 - 1800)
				else:
					cartones_r2_6.config(text=CarSalR2_6)
				
			#----Rango 3-----

			if int(numero_series_rango3["text"]) == 0 :
				cartones_r3_6.config(text=0)
			else:
				CarSalR3_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6)
				if CarSalR3_6 > 1800:
					cartones_r3_6.config(text=CarSalR3_6 - 1800)
				else:
					cartones_r3_6.config(text=CarSalR3_6)

			#----Rango 4-----

			if int(numero_series_rango4["text"]) == 0 :
				cartones_r4_6.config(text=0)
			else:
				CarSalR4_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6)
				if CarSalR4_6 > 1800:
					cartones_r4_6.config(text=CarSalR4_6 - 1800)
				else:
					cartones_r4_6.config(text=CarSalR4_6)

			#----Rango 5-----

			if int(numero_series_rango5["text"]) == 0 :
				cartones_r5_6.config(text=0)
			else:
				CarSalR5_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6)
				if CarSalR5_6 > 1800:
					cartones_r5_6.config(text=CarSalR5_6 - 1800)
				else:
					cartones_r5_6.config(text=CarSalR5_6)

			#----Rango 6-----

			if int(numero_series_rango6["text"]) == 0 :
				cartones_r6_6.config(text=0)
			else:
				CarSalR6_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6)
				if CarSalR6_6 > 1800:
					cartones_r6_6.config(text=CarSalR6_6 - 1800)
				else:
					cartones_r6_6.config(text=CarSalR6_6)

			#----Rango 7-----

			if int(numero_series_rango7["text"]) == 0 :
				cartones_r7_6.config(text=0)
			else:
				CarSalR7_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6)
				if CarSalR7_6 > 1800:
					cartones_r7_6.config(text=CarSalR7_6 - 1800)
				else:
					cartones_r7_6.config(text=CarSalR7_6)

			#----Rango 8-----

			if int(numero_series_rango8["text"]) == 0 :
				cartones_r8_6.config(text=0)
			else:
				CarSalR8_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6)
				if CarSalR8_6 > 1800:
					cartones_r8_6.config(text=CarSalR8_6 - 1800)
				else:
					cartones_r8_6.config(text=CarSalR8_6)

			#----Rango 9-----

			if int(numero_series_rango9["text"]) == 0 :
				cartones_r9_6.config(text=0)
			else:
				CarSalR9_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6)
				if CarSalR9_6 > 1800:
					cartones_r9_6.config(text=CarSalR9_6 - 1800)
				else:
					cartones_r9_6.config(text=CarSalR9_6)

			#----Rango cierre-----

			CarSalCie_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
			if CarSalCie_6 > 1800:
				cartones_cierre_6.config(text=CarSalCie_6 - 1800)
			else:
				cartones_cierre_6.config(text=CarSalCie_6)
	except:
		pass

def CartonSalida_6_proxima():
	pico_salida_6 = pico_salid_6()

	try:
		if SalidaEntry_6.get() == "":
			cartones_r2_6_proxima.config(text=0)
			cartones_r3_6_proxima.config(text=0)
			cartones_r4_6_proxima.config(text=0)
			cartones_r5_6_proxima.config(text=0)
			cartones_r6_6_proxima.config(text=0)
			cartones_r7_6_proxima.config(text=0)
			cartones_r8_6_proxima.config(text=0)
			cartones_r9_6_proxima.config(text=0)
			cartones_cierre_6_proxima.config(text=0)
		else:
			CarSalR1 = int(SalidaEntry_6.get())
			CarSalR1_6 = int(CarSalR1)
			pico_r1_6.config(text=pico_salida_6)

			#----Rango 2-----

			if int(numero_series2["text"]) == 0 :
				cartones_r2_6_proxima.config(text=0)
			else:
				CarSalR2 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6)
				if CarSalR2 > 1800:
					cartones_r2_6_proxima.config(text=CarSalR2 - 1800)
				else:
					cartones_r2_6_proxima.config(text=CarSalR2)
				
			#----Rango 3-----

			if int(numero_series3["text"]) == 0 :
				cartones_r3_6_proxima.config(text=0)
			else:
				CarSalR3 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6)
				if CarSalR3 > 1800:
					cartones_r3_6_proxima.config(text=CarSalR3 - 1800)
				else:
					cartones_r3_6_proxima.config(text=CarSalR3)

			#----Rango 4-----

			if int(numero_series4["text"]) == 0 :
				cartones_r4_6_proxima.config(text=0)
			else:
				CarSalR4 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6)
				if CarSalR4 > 1800:
					cartones_r4_6_proxima.config(text=CarSalR4 - 1800)
				else:
					cartones_r4_6_proxima.config(text=CarSalR4)

			#----Rango 5-----

			if int(numero_series5["text"]) == 0 :
				cartones_r5_6_proxima.config(text=0)
			else:
				CarSalR5 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6)
				if CarSalR5 > 1800:
					cartones_r5_6_proxima.config(text=CarSalR5 - 1800)
				else:
					cartones_r5_6_proxima.config(text=CarSalR5)

			#----Rango 6-----

			if int(numero_series6["text"]) == 0 :
				cartones_r6_6_proxima.config(text=0)
			else:
				CarSalR6 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6)
				if CarSalR6 > 1800:
					cartones_r6_6_proxima.config(text=CarSalR6 - 1800)
				else:
					cartones_r6_6_proxima.config(text=CarSalR6)

			#----Rango 7-----

			if int(numero_series7["text"]) == 0 :
				cartones_r7_6_proxima.config(text=0)
			else:
				CarSalR7 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6)
				if CarSalR7 > 1800:
					cartones_r7_6_proxima.config(text=CarSalR7 - 1800)
				else:
					cartones_r7_6_proxima.config(text=CarSalR7)

			#----Rango 8-----

			if int(numero_series8["text"]) == 0 :
				cartones_r8_6_proxima.config(text=0)
			else:
				CarSalR8 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6)
				if CarSalR8 > 1800:
					cartones_r8_6_proxima.config(text=CarSalR8 - 1800)
				else:
					cartones_r8_6_proxima.config(text=CarSalR8)

			#----Rango 9-----

			if int(numero_series9["text"]) == 0 :
				cartones_r9_6_proxima.config(text=0)
			else:
				CarSalR9 = CarSalR1_6 + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6)
				if CarSalR9 > 1800:
					cartones_r9_6_proxima.config(text=CarSalR9 - 1800)
				else:
					cartones_r9_6_proxima.config(text=CarSalR9)

			#----Rango cierre-----

			CarSalCie = int(CarSalR1_6) + pico_salida_6 + (int(numero_series1["text"]) * 6) + (int(numero_series2["text"]) * 6) + (int(numero_series3["text"]) * 6) + (int(numero_series4["text"]) * 6) + (int(numero_series5["text"]) * 6) + (int(numero_series6["text"]) * 6) + (int(numero_series7["text"]) * 6) + (int(numero_series8["text"]) * 6) + (int(numero_series9["text"]) * 6)
			if CarSalCie > 1800:
				cartones_cierre_6_proxima.config(text=CarSalCie - 1800)
			else:
				cartones_cierre_6_proxima.config(text=CarSalCie)
	except:
		pass

def comprobacion_1():
	fallo = 0
	totalCar = int(entry_impresos.get())

	try:
		series_asignadas = int(numero_series_rango1["text"]) + int(numero_series_rango2["text"]) + int(numero_series_rango3["text"]) + int(numero_series_rango4["text"]) + int(numero_series_rango5["text"]) + int(numero_series_rango6["text"]) + int(numero_series_rango7["text"]) + int(numero_series_rango8["text"]) + int(numero_series_rango9["text"])
		if totalCar < series_asignadas * 6:
			MessageBox.showinfo(message="Series ASIGNADAS superior a cartones a la venta\n corrija el cierre o número de series", title="ATENCION")
			series_cie = 0
			fallo = 1
		return fallo
	except:
		pass

def series_cierre():
	totalCar = int(entry_impresos.get())
	pico_salida = pico_salida_liquidacion()
	pico_cierre_fin = pico_cierre()
	series_cie = 0

	try:
		series_asignadas = int(series_liquidacionr1["text"]) + int(series_liquidacionr2["text"]) + int(series_liquidacionr3["text"]) + int(series_liquidacionr4["text"]) + int(series_liquidacionr5["text"]) + int(series_liquidacionr6["text"]) + int(series_liquidacionr7["text"]) + int(series_liquidacionr8["text"]) + int(series_liquidacionr9["text"]) 
		if entry_del.get() == "" or int(entry_del.get()) == 0 or entry_al.get() == "" or int(entry_al.get()) == 0:
			pass
		else:
			if totalCar - pico_salida >= 6 and totalCar - pico_salida  < 12:				
				series_cie = 0
			else:
				series_cie = round((totalCar - pico_salida - pico_cierre_fin) / 6) - series_asignadas

		if series_cie < 0:
			MessageBox.showinfo(message="Número de series asignadas superior a cartones a la venta\n vuelva a introducir el cierre o baje número de series", title="ATENCION")
			borrar()
			series_cie = 0
		return series_cie

	except:
		pass

def comprobacion_2():
	fallo = 0
	totalCar_2 = int(entry_impresos.get())

	try:
		series_asignadas_2 = int(numero_series_rango1["text"]) + int(numero_series_rango2["text"]) + int(numero_series_rango3["text"]) + int(numero_series_rango4["text"]) + int(numero_series_rango5["text"]) + int(numero_series_rango6["text"]) + int(numero_series_rango7["text"]) + int(numero_series_rango8["text"]) + int(numero_series_rango9["text"])
		if totalCar_2 < series_asignadas_2 * 6:
			MessageBox.showinfo(message="Series ASIGNADAS superior a cartones a la venta\n corrija el cierre o número de series", title="ATENCION")
			series_cie_2 = 0
			fallo = 1
		return fallo
	except:
		pass

def comprobacion_3():
	fallo = 0
	totalCar_3 = int(entry_impresos.get())

	try:
		series_asignadas_3 = int(numero_series_rango1["text"]) + int(numero_series_rango2["text"]) + int(numero_series_rango3["text"]) + int(numero_series_rango4["text"]) + int(numero_series_rango5["text"]) + int(numero_series_rango6["text"]) + int(numero_series_rango7["text"]) + int(numero_series_rango8["text"]) + int(numero_series_rango9["text"])
		if totalCar_3 < series_asignadas_3 * 6:
			MessageBox.showinfo(message="Series ASIGNADAS superior a cartones a la venta\n corrija el cierre o número de series", title="ATENCION")
			series_cie_3 = 0
			fallo = 1
		return fallo
	except:
		pass

def comprobacion_6():
	fallo = 0
	totalCar_6 = int(entry_impresos.get())

	try:
		series_asignadas_6 = int(numero_series_rango1["text"]) + int(numero_series_rango2["text"]) + int(numero_series_rango3["text"]) + int(numero_series_rango4["text"]) + int(numero_series_rango5["text"]) + int(numero_series_rango6["text"]) + int(numero_series_rango7["text"]) + int(numero_series_rango8["text"]) + int(numero_series_rango9["text"])
		if totalCar_6 < series_asignadas_6 * 6:
			MessageBox.showinfo(message="Series ASIGNADAS superior a cartones a la venta\n corrija el cierre o número de series", title="ATENCION")
			series_cie_6 = 0
			fallo = 1
		return fallo
	except:
		pass

def series_total():
	series_cier = series_cierre()

	try:
		series_totales = series_cier + int(series_liquidacionr1["text"]) + int(series_liquidacionr2["text"]) + int(series_liquidacionr3["text"]) + int(series_liquidacionr4["text"]) + int(series_liquidacionr5["text"]) + int(series_liquidacionr6["text"]) + int(series_liquidacionr7["text"]) + int(series_liquidacionr8["text"]) + int(series_liquidacionr9["text"]) 
		return series_totales
	except:
		pass

# ------------------------cambio color----------------------------------------

def cambiaColor():
	if valor2 != 0:
		label_R2.config(text="RANGO 2",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R2.config(text="RANGO 2", fg="black", font=("Times New Roman",17,"bold"))

	if valor3 != 0:
		label_R3.config(text="RANGO 3",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R3.config(text="RANGO 3",fg="black", font=("Times New Roman",17,"bold"))

	if valor4 != 0:
		label_R4.config(text="RANGO 4",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R4.config(text="RANGO 4",fg="black", font=("Times New Roman",17,"bold"))

	if valor5 != 0:
		label_R5.config(text="RANGO 5",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R5.config(text="RANGO 5",fg="black", font=("Times New Roman",17,"bold"))

	if valor6 != 0:
		label_R6.config(text="RANGO 6",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R6.config(text="RANGO 6",fg="black", font=("Times New Roman",17,"bold"))

	if valor7 != 0:
		label_R7.config(text="RANGO 7",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R7.config(text="RANGO 7",fg="black", font=("Times New Roman",17,"bold"))

	if valor8 != 0:
		label_R8.config(text="RANGO 8",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R8.config(text="RANGO 8",fg="black", font=("Times New Roman",17,"bold"))

	if valor9 != 0:
		label_R9.config(text="RANGO 9",fg="green", font=("Times New Roman",17,"bold"))
	else:
		label_R9.config(text="RANGO 9",fg="black", font=("Times New Roman",17,"bold"))			

	#--------------cambio color zona liquidacion---------------------------

	if carton_salida_liqui2["text"] == 0 or carton_salida_liqui2["text"] == "0":
		label_R2_liquidacion.config(text="RANGO 2",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R2_liquidacion.config(text="RANGO 2",fg="green", font=("Times New Roman",17,"bold"))

	if carton_salida_liqui3["text"] == 0 or carton_salida_liqui3["text"] == "0":
		label_R3_liquidacion.config(text="RANGO 3",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R3_liquidacion.config(text="RANGO 3",fg="green", font=("Times New Roman",17,"bold"))

	if carton_salida_liqui4["text"] == 0 or carton_salida_liqui4["text"] == "0":
		label_R4_liquidacion.config(text="RANGO 4",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R4_liquidacion.config(text="RANGO 4",fg="green", font=("Times New Roman",17,"bold"))

	if carton_salida_liqui5["text"] == 0 or carton_salida_liqui5["text"] == "0":
		label_R5_liquidacion.config(text="RANGO 5",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R5_liquidacion.config(text="RANGO 5",fg="green", font=("Times New Roman",17,"bold"))

	if carton_salida_liqui6["text"] == 0 or carton_salida_liqui6["text"] == "0":
		label_R6_liquidacion.config(text="RANGO 6",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R6_liquidacion.config(text="RANGO 6",fg="green", font=("Times New Roman",17,"bold"))

	if carton_salida_liqui7["text"] == 0 or carton_salida_liqui7["text"] == "0":
		label_R7_liquidacion.config(text="RANGO 7",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R7_liquidacion.config(text=" RANGO 7",fg="green", font=("Times New Roman",17,"bold"))

	if carton_salida_liqui8["text"] == 0 or carton_salida_liqui8["text"] == "0":
		label_R8_liquidacion.config(text="RANGO 8",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R8_liquidacion.config(text="RANGO 8",fg="green", font=("Times New Roman",17,"bold"))

	if carton_salida_liqui9["text"] == 0 or carton_salida_liqui9["text"] == "0":
		label_R9_liquidacion.config(text="RANGO 9",fg="black", font=("Times New Roman",17,"bold"))
	else:
		label_R9_liquidacion.config(text="RANGO 9",fg="green", font=("Times New Roman",17,"bold"))

def atras_liquidacion():
	global series_liquidacion_atras_r1; global series_liquidacion_atras_r2; global series_liquidacion_atras_r3; global series_liquidacion_atras_r4;
	global series_liquidacion_atras_r5; global series_liquidacion_atras_r6; global series_liquidacion_atras_r7; global series_liquidacion_atras_r8;
	global series_liquidacion_atras_r9; global series_liquidacion_atras_cierre; global series_liquidacion_atras_total; global pico_salida_liqui1_atras;
	global pico_cierre_liqui_atras; global carton_salida_liqui1_atras; global carton_salida_liqui2_atras; global carton_salida_liqui3_atras;
	global carton_salida_liqui4_atras; global carton_salida_liqui5_atras; global carton_salida_liqui6_atras; global carton_salida_liqui7_atras;
	global carton_salida_liqui8_atras; global carton_salida_liqui9_atras; global carton_salida_liqui1_cierre_atras; global total_cartones_liquidacion_atras;
	global liquidacion_liqui1_atras; global liquidacion_liqui2_atras; global liquidacion_liqui3_atras; global liquidacion_liqui4_atras;
	global liquidacion_liqui5_atras; global liquidacion_liqui6_atras; global liquidacion_liqui7_atras; global liquidacion_liqui8_atras;
	global liquidacion_liqui9_atras; global liquidacion_liqui_cierre_atras; global liquidacion_liqui_total_atras; global label_liquidacion_atras
	global color_atras_final

	series_liquidacion_atras_r1 = series_liquidacionr1["text"]
	series_liquidacion_atras_r2 = series_liquidacionr2["text"]
	series_liquidacion_atras_r3 = series_liquidacionr3["text"]
	series_liquidacion_atras_r4 = series_liquidacionr4["text"]
	series_liquidacion_atras_r5 = series_liquidacionr5["text"]
	series_liquidacion_atras_r6 = series_liquidacionr6["text"]
	series_liquidacion_atras_r7 = series_liquidacionr7["text"]
	series_liquidacion_atras_r8 = series_liquidacionr8["text"]
	series_liquidacion_atras_r9 = series_liquidacionr9["text"]
	series_liquidacion_atras_cierre = series_liquidacion_cierre["text"]
	series_liquidacion_atras_total = total_series_liqui["text"]
	pico_salida_liqui1_atras = pico_salida_liqui1["text"]
	pico_cierre_liqui_atras = pico_cierre_liqui["text"]
	carton_salida_liqui1_atras = carton_salida_liqui1["text"]
	carton_salida_liqui2_atras = carton_salida_liqui2["text"]
	carton_salida_liqui3_atras = carton_salida_liqui3["text"]
	carton_salida_liqui4_atras = carton_salida_liqui4["text"]
	carton_salida_liqui5_atras = carton_salida_liqui5["text"]
	carton_salida_liqui6_atras = carton_salida_liqui6["text"]
	carton_salida_liqui7_atras = carton_salida_liqui7["text"]
	carton_salida_liqui8_atras = carton_salida_liqui8["text"]
	carton_salida_liqui9_atras = carton_salida_liqui9["text"]
	carton_salida_liqui1_cierre_atras = carton_salida_liqui1_cierre["text"]

	liquidacion_liqui1_atras = liquidacion_liqui1["text"]
	liquidacion_liqui2_atras = liquidacion_liqui2["text"]
	liquidacion_liqui3_atras = liquidacion_liqui3["text"]
	liquidacion_liqui4_atras = liquidacion_liqui4["text"]
	liquidacion_liqui5_atras = liquidacion_liqui5["text"]
	liquidacion_liqui6_atras = liquidacion_liqui6["text"]
	liquidacion_liqui7_atras = liquidacion_liqui7["text"]
	liquidacion_liqui8_atras = liquidacion_liqui8["text"]
	liquidacion_liqui9_atras = liquidacion_liqui9["text"]
	liquidacion_liqui_cierre_atras = liquidacion_liqui_cierre["text"]
	liquidacion_liqui_total_atras = liquidacion_liqui_total["text"]

	if color_atras == 1:
		color_atras_final = "blue"
	elif color_atras ==  2:
		color_atras_final = "#8B0000"
	elif color_atras == 3:
		color_atras_final = "#FF1493"
	else:
		color_atras_final = "#2F4F4F"
	
def sube_a_liquidacion():
	global liquida_total; global color_atras

	color_atras = 1
	atras_liquidacion()

	try:
		pico_salida = pico_salida_liquidacion()
		pico_cierre_fin = pico_cierre()
		total_cartones = int(entry_impresos.get())
		CarSalR1 = int(entry_del.get())

		series_liquidacionr1.config(text=numero_series_rango1["text"],fg ="blue")
		pico_salida_liqui1.config(text=pico_salida,fg ="blue")

		try:
			r1 = numero_series_rango1["text"] * 6 + int(SalidaEntry_1.get()) + pico_salida - 1
			if r1 >= 1801:
				r1 = r1 - 1800
				resultado = int(SalidaEntry_1.get()),"-",r1
				carton_salida_liqui1.config(text=resultado,fg ="blue")
			else:
				resultado = int(SalidaEntry_1.get()),"-",r1
				carton_salida_liqui1.config(text=resultado,fg ="blue")
		except:
			pass

		#-------------------------Liquidacion rango 2------------------------------

		series_liquidacionr2.config(text=numero_series_rango2["text"],fg ="blue")

		try:
			r1 = numero_series_rango2["text"] * 6 + cartones_r2["text"] - 1
			if numero_series_rango2["text"] == 0:
				carton_salida_liqui2.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango2["text"] * 6 + cartones_r2["text"] - 1801
				resultado = cartones_r2["text"],"-",r1
				carton_salida_liqui2.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r2["text"],"-",r1
				carton_salida_liqui2.config(text=resultado,fg ="blue")
		except:
			pass
			
		#------------------Liquidacion rango 3--------------------------
		
		series_liquidacionr3.config(text=numero_series_rango3["text"],fg ="blue")

		try:
			r1 = numero_series_rango3["text"] * 6 + cartones_r3["text"] - 1
			if numero_series_rango3["text"] == 0:
				carton_salida_liqui3.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango3["text"] * 6 + cartones_r3["text"] - 1801
				resultado = cartones_r3["text"],"-",r1
				carton_salida_liqui3.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r3["text"],"-",r1
				carton_salida_liqui3.config(text=resultado,fg ="blue")
		except:
			pass
		
		#------------------Liquidacion rango 4--------------------------
		
		series_liquidacionr4.config(text=numero_series_rango4["text"],fg ="blue")

		try:
			r1 = numero_series_rango4["text"] * 6 + cartones_r4["text"] - 1
			if numero_series_rango4["text"] == 0:
				carton_salida_liqui4.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango4["text"] * 6 + cartones_r4["text"] - 1801
				resultado = cartones_r4["text"],"-",r1
				carton_salida_liqui4.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r4["text"],"-",r1
				carton_salida_liqui4.config(text=resultado,fg ="blue")
		except:
			pass

		#------------------Liquidacion rango 5--------------------------
		
		series_liquidacionr5.config(text=numero_series_rango5["text"],fg ="blue")

		try:
			r1 = numero_series_rango5["text"] * 6 + cartones_r5["text"] - 1
			if numero_series_rango5["text"] == 0:
				carton_salida_liqui5.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango5["text"] * 6 + cartones_r5["text"] - 1801
				resultado = cartones_r5["text"],"-",r1
				carton_salida_liqui5.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r5["text"],"-",r1
				carton_salida_liqui5.config(text=resultado,fg ="blue")
		except:
			pass    		

		#------------------Liquidacion rango 6--------------------------
		
		series_liquidacionr6.config(text=numero_series_rango6["text"],fg ="blue")

		try:
			r1 = numero_series_rango6["text"] * 6 + cartones_r6["text"] - 1
			if numero_series_rango6["text"] == 0:
				carton_salida_liqui6.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango6["text"] * 6 + cartones_r6["text"] - 1801
				resultado = cartones_r6["text"],"-",r1
				carton_salida_liqui6.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r6["text"],"-",r1
				carton_salida_liqui6.config(text=resultado,fg ="blue")
		except:
			pass    

		#------------------Liquidacion rango 7--------------------------
		
		series_liquidacionr7.config(text=numero_series_rango7["text"],fg ="blue")

		try:
			r1 = numero_series_rango7["text"] * 6 + cartones_r7["text"] - 1
			if numero_series_rango7["text"] == 0:
				carton_salida_liqui7.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango7["text"] * 6 + cartones_r7["text"] - 1801
				resultado = cartones_r7["text"],"-",r1
				carton_salida_liqui7.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r7["text"],"-",r1
				carton_salida_liqui7.config(text=resultado,fg ="blue")
		except:
			pass

		#------------------Liquidacion rango 8--------------------------
		
		series_liquidacionr8.config(text=numero_series_rango8["text"],fg ="blue")

		try:
			r1 = numero_series_rango8["text"] * 6 + cartones_r8["text"] - 1
			if numero_series_rango8["text"] == 0:
				carton_salida_liqui8.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango8["text"] * 6 + cartones_r8["text"] - 1801
				resultado = cartones_r8["text"],"-",r1
				carton_salida_liqui8.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r8["text"],"-",r1
				carton_salida_liqui8.config(text=resultado,fg ="blue")
		except:
			pass

		#------------------Liquidacion rango 9--------------------------
		
		series_liquidacionr9.config(text=numero_series_rango9["text"],fg ="blue")

		try:
			r1 = numero_series_rango9["text"] * 6 + cartones_r9["text"] - 1
			if numero_series_rango9["text"] == 0:
				carton_salida_liqui9.config(text="0",fg ="blue")
			elif r1 >= 1801:
				r1 = numero_series_rango9["text"] * 6 + cartones_r9["text"] - 1801
				resultado = cartones_r9["text"],"-",r1
				carton_salida_liqui9.config(text=resultado,fg ="blue")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r9["text"],"-",r1
				carton_salida_liqui9.config(text=resultado,fg ="blue")
		except:
			pass

		#------------------Liquidacion cierre--------------------------

		total_series_cierre = series_cierre()
		series_liquidacion_cierre.config(text=total_series_cierre,fg ="blue")

		try:
			CarSalCie = CarSalR1 + pico_salida + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
			if CarSalCie >= 1800:
				resultado= CarSalCie - 1800, "-", entry_al.get()
			else: 
				resultado = CarSalCie, "-", entry_al.get()
			carton_salida_liqui1_cierre.config(text=resultado, fg ="blue")
			pico_cierre_liqui.config(fg ="blue")
		except:
			pass

		#----------------------Liquidacion Total-----------------------------
		series_totales = series_total()

		try:
			liquida_total = total_cartones * 1.5,"€"
			liquidacion_liqui_total.config(text=liquida_total, fg="#800080")
			total_series_liqui.config(text=series_totales, fg ="blue")
			total_cartones_liquidacion.config(text=total_cartones, fg ="blue")
		except:
			pass

		if int(entry_al.get()) == 1800:
			salida.set(1)
			PreparaRectifica()
			CartonSalida_1()
			CartonSalida_1_proxima()
			total_car_1.config(text = 0)
		else:
			salida.set(int (entry_al.get()) + 1)
			PreparaRectifica()
			CartonSalida_1()
			CartonSalida_1_proxima()
			total_car_1.config(text = 0)

		pico_cierre_liqui.config(text = pico_cierre_fin)
	except:
		pass

# --------------------- Sube a liquidacion 2----------------------------------

def sube_a_liquidacion_2():
	global liquida_total; global color_atras

	color_atras = 2
	atras_liquidacion()

	try:
		pico_salida_2 = pico_salida_liquidacion()
		pico_cierre_fin = pico_cierre()
		total_cartone_2 = int(entry_impresos.get())
		CarSalR1_2 = int(entry_del.get())
		
		series_liquidacionr1.config(text=numero_series_rango1["text"],fg ="#8B0000")
		pico_salida_liqui1.config(text=pico_salida_2,fg ="#8B0000")

		try:
			r1 = numero_series_rango1["text"] * 6 + int(SalidaEntry_2.get()) + pico_salida_2 - 1
			if r1 >= 1801:
				r1 = r1 - 1800
				resultado = int(SalidaEntry_2.get()),"-",r1
				carton_salida_liqui1.config(text=resultado,fg ="#8B0000")
			else:
				resultado = int(SalidaEntry_2.get()),"-",r1
				carton_salida_liqui1.config(text=resultado,fg ="#8B0000")
		except:
			pass

		#-------------------------Liquidacion rango 2------------------------------

		series_liquidacionr2.config(text=numero_series_rango2["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango2["text"] * 6 + cartones_r2_2["text"] - 1
			if numero_series_rango2["text"] == 0:
				carton_salida_liqui2.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango2["text"] * 6 + cartones_r2_2["text"] - 1801
				resultado = cartones_r2_2["text"],"-",r1
				carton_salida_liqui2.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r2_2["text"],"-",r1
				carton_salida_liqui2.config(text=resultado,fg ="#8B0000")
		except:
			pass
			
		#------------------Liquidacion rango 3--------------------------
		
		series_liquidacionr3.config(text=numero_series_rango3["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango3["text"] * 6 + cartones_r3_2["text"] - 1
			if numero_series_rango3["text"] == 0:
				carton_salida_liqui3.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango3["text"] * 6 + cartones_r3_2["text"] - 1801
				resultado = cartones_r3_2["text"],"-",r1
				carton_salida_liqui3.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r3_2["text"],"-",r1
				carton_salida_liqui3.config(text=resultado,fg ="#8B0000")
		except:
			pass
		
		#------------------Liquidacion rango 4--------------------------
		
		series_liquidacionr4.config(text=numero_series_rango4["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango4["text"] * 6 + cartones_r4_2["text"] - 1
			if numero_series_rango4["text"] == 0:
				carton_salida_liqui4.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango4["text"] * 6 + cartones_r4_2["text"] - 1801
				resultado = cartones_r4_2["text"],"-",r1
				carton_salida_liqui4.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r4_2["text"],"-",r1
				carton_salida_liqui4.config(text=resultado,fg ="#8B0000")
		except:
			pass   		

		#------------------Liquidacion rango 5--------------------------
		
		series_liquidacionr5.config(text=numero_series_rango5["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango5["text"] * 6 + cartones_r5_2["text"] - 1
			if numero_series_rango5["text"] == 0:
				carton_salida_liqui5.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango5["text"] * 6 + cartones_r5_2["text"] - 1801
				resultado = cartones_r5_2["text"],"-",r1
				carton_salida_liqui5.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r5_2["text"],"-",r1
				carton_salida_liqui5.config(text=resultado,fg ="#8B0000")
		except:
			pass    		

		#------------------Liquidacion rango 6--------------------------
		
		series_liquidacionr6.config(text=numero_series_rango6["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango6["text"] * 6 + cartones_r6_2["text"] - 1
			if numero_series_rango6["text"] == 0:
				carton_salida_liqui6.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango6["text"] * 6 + cartones_r6_2["text"] - 1801
				resultado = cartones_r6_2["text"],"-",r1
				carton_salida_liqui6.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r6_2["text"],"-",r1
				carton_salida_liqui6.config(text=resultado,fg ="#8B0000")
		except:
			pass    

		#------------------Liquidacion rango 7--------------------------
		
		series_liquidacionr7.config(text=numero_series_rango7["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango7["text"] * 6 + cartones_r7_2["text"] - 1
			if numero_series_rango7["text"] == 0:
				carton_salida_liqui7.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango7["text"] * 6 + cartones_r7_2["#8B0000"] - 1801
				resultado = cartones_r7_2["text"],"-",r1
				carton_salida_liqui7.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r7_2["text"],"-",r1
				carton_salida_liqui7.config(text=resultado,fg ="#8B0000")
		except:
			pass

		#------------------Liquidacion rango 8--------------------------
		
		series_liquidacionr8.config(text=numero_series_rango8["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango8["text"] * 6 + cartones_r8_2["text"] - 1
			if numero_series_rango8["text"] == 0:
				carton_salida_liqui8.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango8["text"] * 6 + cartones_r8_2["text"] - 1801
				resultado = cartones_r8_2["text"],"-",r1
				carton_salida_liqui8.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r8_2["text"],"-",r1
				carton_salida_liqui8.config(text=resultado,fg ="#8B0000")
		except:
			pass

		#------------------Liquidacion rango 9--------------------------
		
		series_liquidacionr9.config(text=numero_series_rango9["text"],fg ="#8B0000")

		try:
			r1 = numero_series_rango9["text"] * 6 + cartones_r9_2["text"] - 1
			if numero_series_rango9["text"] == 0:
				carton_salida_liqui9.config(text="0",fg ="#8B0000")
			elif r1 >= 1801:
				r1 = numero_series_rango9["text"] * 6 + cartones_r9_2["text"] - 1801
				resultado = cartones_r9_2["text"],"-",r1
				carton_salida_liqui9.config(text=resultado,fg ="#8B0000")
			elif r1 <= 1800 and r1 != 0:
				resultado = cartones_r9_2["text"],"-",r1
				carton_salida_liqui9.config(text=resultado,fg ="#8B0000")
		except:
			pass

		#------------------Liquidacion cierre--------------------------

		series_cierr_2 = series_cierre()#series_cierre_2
		series_liquidacion_cierre.config(text=series_cierr_2, fg ="#8B0000")

		try:
			CarSalCie_2 = CarSalR1_2 + pico_salida_2 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
			if CarSalCie_2 >= 1800:
				resultado = CarSalCie_2 - 1800, "-", entry_al.get()
			else:
				resultado = CarSalCie_2, "-", entry_al.get()
			carton_salida_liqui1_cierre.config(text=resultado, fg ="#8B0000")
			pico_cierre_liqui.config(fg ="#8B0000")
		except:
			pass

		#----------------------Liquidación Total-----------------------------
		series_totales_2 = series_total()#series_total_2

		try:
			liquida_total = total_cartone_2 * 2,"€"
			liquidacion_liqui_total.config(text=liquida_total)
			total_series_liqui.config(text=series_totales_2, fg ="#8B0000")
			total_cartones_liquidacion.config(text=total_cartone_2, fg ="#8B0000")
		except:
			pass

		if int(entry_al.get()) == 1800:
			salida_2.set(1)
			PreparaRectifica()
			CartonSalida_2()
			CartonSalida_2_proxima()
			total_car_2.config(text = 0)
		else:
			salida_2.set(int(entry_al.get()) + 1)
			PreparaRectifica()
			CartonSalida_2()
			CartonSalida_2_proxima()
			total_car_2.config(text = 0)

		pico_cierre_liqui.config(text = pico_cierre_fin)
	except:
		pass

# --------------------------Sube a liquidación 3------------------------------

def sube_a_liquidacion_3():
	global liquida_total; global color_atras

	color_atras = 3
	atras_liquidacion()

	try:
		pico_salida_3 = pico_salida_liquidacion()
		pico_cierre_fin = pico_cierre()
		total_cartone_3 = int(entry_impresos.get())
		CarSalR1_3 = int(entry_del.get())
		
		series_liquidacionr1.config(text=numero_series_rango1["text"],fg ="#FF1493")
		pico_salida_liqui1.config(text=pico_salida_3,fg ="#FF1493")
		r1 = numero_series_rango1["text"] * 6 + int(SalidaEntry_3.get()) + pico_salida_3 - 1
		if r1 >= 1801:
			r1 = r1 - 1800
			resultado = int(SalidaEntry_3.get()),"-",r1
			carton_salida_liqui1.config(text=resultado,fg ="#FF1493")
		else:
			resultado = int(SalidaEntry_3.get()),"-",r1
			carton_salida_liqui1.config(text=resultado,fg ="#FF1493")

		#-------------------------Liquidacion rango 2------------------------------

		series_liquidacionr2.config(text=numero_series_rango2["text"],fg ="#FF1493")
		r1 = numero_series_rango2["text"] * 6 + cartones_r2_3["text"] - 1
		if numero_series_rango2["text"] == 0:
			carton_salida_liqui2.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango2["text"] * 6 + cartones_r2_3["text"] - 1801
			resultado = cartones_r2_3["text"],"-",r1
			carton_salida_liqui2.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r2_3["text"],"-",r1
			carton_salida_liqui2.config(text=resultado,fg ="#FF1493")
			
		#------------------Liquidacion rango 3--------------------------
		
		series_liquidacionr3.config(text=numero_series_rango3["text"],fg ="#FF1493")
		r1 = numero_series_rango3["text"] * 6 + cartones_r3_3["text"] - 1
		if numero_series_rango3["text"] == 0:
			carton_salida_liqui3.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango3["text"] * 6 + cartones_r3_3["text"] - 1801
			resultado = cartones_r3_3["text"],"-",r1
			carton_salida_liqui3.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r3_3["text"],"-",r1
			carton_salida_liqui3.config(text=resultado,fg ="#FF1493")
		
		#------------------Liquidacion rango 4--------------------------
		
		series_liquidacionr4.config(text=numero_series_rango4["text"],fg ="#FF1493")
		r1 = numero_series_rango4["text"] * 6 + cartones_r4_3["text"] - 1
		if numero_series_rango4["text"] == 0:
			carton_salida_liqui4.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango4["text"] * 6 + cartones_r4_3["text"] - 1801
			resultado = cartones_r4_3["text"],"-",r1
			carton_salida_liqui4.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r4_3["text"],"-",r1
			carton_salida_liqui4.config(text=resultado,fg ="#FF1493")   		

		#------------------Liquidacion rango 5--------------------------
		
		series_liquidacionr5.config(text=numero_series_rango5["text"],fg ="#FF1493")
		r1 = numero_series_rango5["text"] * 6 + cartones_r5_3["text"] - 1
		if numero_series_rango5["text"] == 0:
			carton_salida_liqui5.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango5["text"] * 6 + cartones_r5_3["text"] - 1801
			resultado = cartones_r5_3["text"],"-",r1
			carton_salida_liqui5.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r5_3["text"],"-",r1
			carton_salida_liqui5.config(text=resultado,fg ="#FF1493")    		

		#------------------Liquidacion rango 6--------------------------
		
		series_liquidacionr6.config(text=numero_series_rango6["text"],fg ="#FF1493")
		r1 = numero_series_rango6["text"] * 6 + cartones_r6_3["text"] - 1
		if numero_series_rango6["text"] == 0:
			carton_salida_liqui6.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango6["text"] * 6 + cartones_r6_3["text"] - 1801
			resultado = cartones_r6_3["text"],"-",r1
			carton_salida_liqui6.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r6_3["text"],"-",r1
			carton_salida_liqui6.config(text=resultado,fg ="#FF1493")    

		#------------------Liquidacion rango 7--------------------------
		
		series_liquidacionr7.config(text=numero_series_rango7["text"],fg ="#FF1493")
		r1 = numero_series_rango7["text"] * 6 + cartones_r7_3["text"] - 1
		if numero_series_rango7["text"] == 0:
			carton_salida_liqui7.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango7["text"] * 6 + cartones_r7_3["#FF1493"] - 1801
			resultado = cartones_r7_3["text"],"-",r1
			carton_salida_liqui7.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r7_3["text"],"-",r1
			carton_salida_liqui7.config(text=resultado,fg ="#FF1493")

		#------------------Liquidacion rango 8--------------------------
		
		series_liquidacionr8.config(text=numero_series_rango8["text"],fg ="#FF1493")
		r1 = numero_series_rango8["text"] * 6 + cartones_r8_3["text"] - 1
		if numero_series_rango8["text"] == 0:
			carton_salida_liqui8.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango8["text"] * 6 + cartones_r8_3["text"] - 1801
			resultado = cartones_r8_3["text"],"-",r1
			carton_salida_liqui8.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r8_3["text"],"-",r1
			carton_salida_liqui8.config(text=resultado,fg ="#FF1493")

		#------------------Liquidacion rango 9--------------------------
		
		series_liquidacionr9.config(text=numero_series_rango9["text"],fg ="#FF1493")
		r1 = numero_series_rango9["text"] * 6 + cartones_r9_3["text"] - 1
		if numero_series_rango9["text"] == 0:
			carton_salida_liqui9.config(text="0",fg ="#FF1493")
		elif r1 >= 1801:
			r1 = numero_series_rango9["text"] * 6 + cartones_r9_3["text"] - 1801
			resultado = cartones_r9_3["text"],"-",r1
			carton_salida_liqui9.config(text=resultado,fg ="#FF1493")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r9_3["text"],"-",r1
			carton_salida_liqui9.config(text=resultado,fg ="#FF1493")

		#------------------Liquidacion cierre--------------------------

		series_cierr_3 = series_cierre()#series_cierre_3
		series_liquidacion_cierre.config(text=series_cierr_3, fg ="#FF1493")

		CarSalCie_3 = CarSalR1_3 + pico_salida_3 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
		if CarSalCie_3 >= 1800:
			resultado = CarSalCie_3 - 1800, "-", entry_al.get()
		else: 
			resultado = CarSalCie_3, "-", entry_al.get()
		carton_salida_liqui1_cierre.config(text=resultado, fg ="#FF1493")
		pico_cierre_liqui.config(fg ="#FF1493")

		#----------------------Liquidación Total-----------------------------
		series_totales_3 = series_total()#series_total_3
		
		liquida_total = total_cartone_3 * 3,"€"
		liquidacion_liqui_total.config(text=liquida_total)
		total_series_liqui.config(text=series_totales_3, fg ="#FF1493")

		if int(entry_al.get()) == 1800:
			salida_3.set(1)
			PreparaRectifica()
			CartonSalida_3()
			CartonSalida_3_proxima()
			total_car_3.config(text = 0)
		else:
			salida_3.set(int(entry_al.get()) + 1)
			PreparaRectifica()
			CartonSalida_3()
			CartonSalida_3_proxima()
			total_car_3.config(text = 0)

		pico_cierre_liqui.config(text = pico_cierre_fin)
	except:
		pass

# ----------------------------Sube a liquidación 6----------------------

def sube_a_liquidacion_6():
	global serie_r1_atras; global serie_r2_atras; global serie_r3_atras; global serie_r4_atras;
	global serie_r5_atras; global serie_r6_atras; global serie_r7_atras; global serie_r8_atras; global serie_r9_atras;
	global liquida_total; global color_atras

	color_atras = 4

	atras_liquidacion()

	try:
		pico_salida_6 = pico_salida_liquidacion()
		pico_cierre_fin = pico_cierre()
		total_cartone_6 = int(entry_impresos.get())
		CarSalR1_6 = int(entry_del.get())

		series_liquidacionr1.config(text=numero_series_rango1["text"],fg ="#2F4F4F")
		pico_salida_liqui1.config(text=pico_salida_6,fg ="#2F4F4F")
		r1 = numero_series_rango1["text"] * 6 + int(SalidaEntry_6.get()) + pico_salida_6 - 1
		if r1 >= 1801:
			r1 = r1 - 1800
			resultado = int(SalidaEntry_6.get()),"-",r1
			carton_salida_liqui1.config(text=resultado,fg ="#2F4F4F")
		else:
			resultado = int(SalidaEntry_6.get()),"-",r1
			carton_salida_liqui1.config(text=resultado,fg ="#2F4F4F")

		#-------------------------Liquidacion rango 2------------------------------

		series_liquidacionr2.config(text=numero_series_rango2["text"],fg ="#2F4F4F")
		r1 = numero_series_rango2["text"] * 6 + cartones_r2_6["text"] - 1
		if numero_series_rango2["text"] == 0:
			carton_salida_liqui2.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango2["text"] * 6 + cartones_r2_6["text"] - 1801
			resultado = cartones_r2_6["text"],"-",r1
			carton_salida_liqui2.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r2_6["text"],"-",r1
			carton_salida_liqui2.config(text=resultado,fg ="#2F4F4F")
			
		#------------------Liquidacion rango 3--------------------------
		
		series_liquidacionr3.config(text=numero_series_rango3["text"],fg ="#2F4F4F")
		r1 = numero_series_rango3["text"] * 6 + cartones_r3_6["text"] - 1
		if numero_series_rango3["text"] == 0:
			carton_salida_liqui3.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango3["text"] * 6 + cartones_r3_6["text"] - 1801
			resultado = cartones_r3_6["text"],"-",r1
			carton_salida_liqui3.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r3_6["text"],"-",r1
			carton_salida_liqui3.config(text=resultado,fg ="#2F4F4F")
		
		#------------------Liquidacion rango 4--------------------------
		
		series_liquidacionr4.config(text=numero_series_rango4["text"],fg ="#2F4F4F")
		r1 = numero_series_rango4["text"] * 6 + cartones_r4_6["text"] - 1
		if numero_series_rango4["text"] == 0:
			carton_salida_liqui4.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango4["text"] * 6 + cartones_r4_6["text"] - 1801
			resultado = cartones_r4_6["text"],"-",r1
			carton_salida_liqui4.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r4_6["text"],"-",r1
			carton_salida_liqui4.config(text=resultado,fg ="#2F4F4F")   		

		#------------------Liquidacion rango 5--------------------------
		
		series_liquidacionr5.config(text=numero_series_rango5["text"],fg ="#2F4F4F")
		r1 = numero_series_rango5["text"] * 6 + cartones_r5_6["text"] - 1
		if numero_series_rango5["text"] == 0:
			carton_salida_liqui5.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango5["text"] * 6 + cartones_r5_6["text"] - 1801
			resultado = cartones_r5_6["text"],"-",r1
			carton_salida_liqui5.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r5_6["text"],"-",r1
			carton_salida_liqui5.config(text=resultado,fg ="#2F4F4F")    		

		#------------------Liquidacion rango 6--------------------------
		
		series_liquidacionr6.config(text=numero_series_rango6["text"],fg ="#2F4F4F")
		r1 = numero_series_rango6["text"] * 6 + cartones_r6_6["text"] - 1
		if numero_series_rango6["text"] == 0:
			carton_salida_liqui6.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango6["text"] * 6 + cartones_r6_6["text"] - 1801
			resultado = cartones_r6_6["text"],"-",r1
			carton_salida_liqui6.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r6_6["text"],"-",r1
			carton_salida_liqui6.config(text=resultado,fg ="#2F4F4F")    

		#------------------Liquidacion rango 7--------------------------
		
		series_liquidacionr7.config(text=numero_series_rango7["text"],fg ="#2F4F4F")
		r1 = numero_series_rango7["text"] * 6 + cartones_r7_6["text"] - 1
		if numero_series_rango7["text"] == 0:
			carton_salida_liqui7.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango7["text"] * 6 + cartones_r7_6["#2F4F4F"] - 1801
			resultado = cartones_r7_6["text"],"-",r1
			carton_salida_liqui7.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r7_6["text"],"-",r1
			carton_salida_liqui7.config(text=resultado,fg ="#2F4F4F")

		#------------------Liquidacion rango 8--------------------------
		
		series_liquidacionr8.config(text=numero_series_rango8["text"],fg ="#2F4F4F")
		r1 = numero_series_rango8["text"] * 6 + cartones_r8_6["text"] - 1
		if numero_series_rango8["text"] == 0:
			carton_salida_liqui8.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango8["text"] * 6 + cartones_r8_6["text"] - 1801
			resultado = cartones_r8_6["text"],"-",r1
			carton_salida_liqui8.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r8_6["text"],"-",r1
			carton_salida_liqui8.config(text=resultado,fg ="#2F4F4F")

		#------------------Liquidacion rango 9--------------------------
		
		series_liquidacionr9.config(text=numero_series_rango9["text"],fg ="#2F4F4F")
		r1 = numero_series_rango9["text"] * 6 + cartones_r9_6["text"] - 1
		if numero_series_rango9["text"] == 0:
			carton_salida_liqui9.config(text="0",fg ="#2F4F4F")
		elif r1 >= 1801:
			r1 = numero_series_rango9["text"] * 6 + cartones_r9_6["text"] - 1801
			resultado = cartones_r9_6["text"],"-",r1
			carton_salida_liqui9.config(text=resultado,fg ="#2F4F4F")
		elif r1 <= 1800 and r1 != 0:
			resultado = cartones_r9_6["text"],"-",r1
			carton_salida_liqui9.config(text=resultado,fg ="#2F4F4F")

		#------------------Liquidacion cierre--------------------------

		series_cierr_6 = series_cierre()#series_cierre_6
		series_liquidacion_cierre.config(text=series_cierr_6, fg ="#2F4F4F")

		CarSalCie_6 = CarSalR1_6 + pico_salida_6 + (int(numero_series_rango1["text"]) * 6) + (int(numero_series_rango2["text"]) * 6) + (int(numero_series_rango3["text"]) * 6) + (int(numero_series_rango4["text"]) * 6) + (int(numero_series_rango5["text"]) * 6) + (int(numero_series_rango6["text"]) * 6) + (int(numero_series_rango7["text"]) * 6) + (int(numero_series_rango8["text"]) * 6) + (int(numero_series_rango9["text"]) * 6)
		if CarSalCie_6 >= 1800:
			resultado = CarSalCie_6 - 1800, "-", entry_al.get()
		else: 
			resultado = CarSalCie_6, "-", entry_al.get()
		carton_salida_liqui1_cierre.config(text=resultado, fg ="#2F4F4F")
		pico_cierre_liqui.config(fg ="#2F4F4F")

		#----------------------Liquidación Total-----------------------------
		series_totales_6 = series_total()#series_total_6
		liquida_total = int(entry_impresos.get()) * 6,"€"
		liquidacion_liqui_total.config(text=liquida_total)
		total_series_liqui.config(text=series_totales_6, fg ="#2F4F4F")

		if int(entry_al.get()) == 1800:

			salida_6.set(1)
			PreparaRectifica()
			CartonSalida_6()
			CartonSalida_6_proxima()
			total_car_6.config(text = 0)
			
		else:
			salida_6.set(int(entry_al.get()) + 1)
			PreparaRectifica()
			CartonSalida_6()
			CartonSalida_6_proxima()
			total_car_6.config(text = 0)

		pico_cierre_liqui.config(text = pico_cierre_fin)
	except:
		pass

# ---------------------------liquidacion------------------------------------------------

def liquida(num):
	global control_atras; global control_parpadeo; global historico
	
	control_parpadeo = 0
	etiquita_instrucciones.pack_forget()

	if entry_al.get() == "" or int(entry_al.get()) == 0:
		pass
	else:
		if num == 1.5:
			verifica = comprobacion_1()
			if verifica == 1:
				pass
			else:
				control_atras = 1
				boton_atras['state'] = NORMAL
				sube_a_liquidacion()
				calcula_liquidacion(1.5)
				if historico == 1:
					datos_historico6()
				else:
					historico = 1
		elif num == 2:
			verifica_2 = comprobacion_2()
			if verifica_2 == 1:
				pass
			else:
				control_atras = 2
				boton_atras['state'] = NORMAL
				sube_a_liquidacion_2()
				calcula_liquidacion(2)	
				if historico == 1:
					datos_historico6()
				else:
					historico = 1
		elif num == 3:
			verifica_3 = comprobacion_3()
			if verifica_3 == 1:
				pass
			else:
				control_atras = 3
				boton_atras['state'] = NORMAL
				sube_a_liquidacion_3()
				calcula_liquidacion(3)
				if historico == 1:
					datos_historico6()
				else:
					historico = 1
		else:
			verifica_6 = comprobacion_6()
			if verifica_6 == 1:
				pass
			else:
				control_atras = 6
				boton_atras['state'] = NORMAL
				sube_a_liquidacion_6()
				calcula_liquidacion(6)	
				if historico == 1:
					datos_historico6()
				else:
					historico = 1

def calcula_liquidacion(num):
	try:
		liquida1 = (int(series_liquidacionr1["text"]) * 6 + int(pico_salida_liqui1["text"])) * num ,"€"
		liquidacion_liqui1.config(text=liquida1)

		liquida_cierre = (int(series_liquidacion_cierre["text"]) * 6 + int(pico_cierre_liqui["text"]))* num,"€"
		liquidacion_liqui_cierre.config(text=liquida_cierre)

		liquida2 = int(series_liquidacionr2["text"]) * 6 * num,"€"
		liquidacion_liqui2.config(text=liquida2)

		liquida3 = int(series_liquidacionr3["text"]) * 6 * num,"€"
		liquidacion_liqui3.config(text=liquida3)

		liquida4 = int(series_liquidacionr4["text"]) * 6 * num,"€"
		liquidacion_liqui4.config(text=liquida4)

		liquida5 = int(series_liquidacionr5["text"]) * 6 * num,"€"
		liquidacion_liqui5.config(text=liquida5)

		liquida6 = int(series_liquidacionr6["text"]) * 6 * num,"€"
		liquidacion_liqui6.config(text=liquida6)

		liquida7 = int(series_liquidacionr7["text"]) * 6 * num,"€"
		liquidacion_liqui7.config(text=liquida7)

		liquida8 = int(series_liquidacionr8["text"]) * 6 * num,"€"
		liquidacion_liqui8.config(text=liquida8)

		liquida9 = int(series_liquidacionr9["text"]) * 6 * num,"€"
		liquidacion_liqui9.config(text=liquida9)

		liquida_total = int(total_cartones_liquidacion["text"]) * num,"€"
		liquidacion_liqui_total.config(text=liquida_total)

		totalCaja()
	except:
		pass

# ---------------------------- Entorno Grafico---------------------------------------

caja_partida=IntVar()
linea=IntVar()
bingo=IntVar()
de=IntVar()
al=IntVar()
precio=IntVar()
vendidos=IntVar()
prima=IntVar()
pextra=IntVar()
impresos=IntVar()
caja=IntVar()
informaticos=IntVar()
recaudado=IntVar()
linea.set(0)
bingo.set(0)
prima.set(0)
pextra.set(0)
de.set(0)
al.set(0)
precio.set(0)
vendidos.set(0)
impresos.set(0)
caja.set(0)
informaticos.set(0)
recaudado.set(0)

marco2=Frame(raiz,bg="#000099")#
marco2.pack(expand=True, fill= BOTH)

marco1=Frame(raiz,bg="#3149E4")
marco1.pack(expand=True, fill= BOTH)

Venta_frame = Frame(raiz,bg="#000099")
Venta_frame.pack(expand=True, fill= BOTH)

label_precio = Label(Venta_frame, text ="                     PRECIO",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_precio.grid(row = 0, column = 0)
entry_precio = Entry(Venta_frame,justify= RIGHT, state="readonly",textvariable=precio, font=("Arial",12,"bold"), width=10)
entry_precio.grid(row = 0, column = 1)
label_precio_E = Label(Venta_frame, text ="€",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_precio_E.grid(row = 0, column = 2)

label_del = Label(Venta_frame, text ="       DEL",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_del.grid(row = 0, column = 3)
entry_del = Entry(Venta_frame,justify= RIGHT, state="readonly",textvariable=de, font=("Arial",12,"bold"), width=10)
entry_del.grid(row = 0, column = 4)

label_impresos = Label(Venta_frame, text ="                 IMPRESOS",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_impresos.grid(row = 0, column = 5)
entry_impresos = Entry(Venta_frame,justify= RIGHT, state="readonly",textvariable=impresos, font=("Arial",12,"bold"), width=10)
entry_impresos.grid(row = 0, column = 6)

label_recaudado = Label(Venta_frame, text ="                 RECAUDADO",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_recaudado.grid(row = 0, column = 7)
entry_recaudado = Entry(Venta_frame,justify= RIGHT, state="readonly",textvariable=recaudado, font=("Arial",12,"bold"), width=10)
entry_recaudado.grid(row = 0, column = 8)
label_recaudado_E = Label(Venta_frame, text ="€",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_recaudado_E.grid(row = 0, column = 9)

label_caja = Label(Venta_frame, text ="          CAJA IMPRESOS",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_caja.grid(row = 1, column = 7)
entry_caja = Entry(Venta_frame,justify= RIGHT, state="readonly",textvariable=caja, font=("Arial",12,"bold"), width=10)
entry_caja.grid(row = 1, column = 8)
label_caja_E = Label(Venta_frame, text ="€",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_caja_E.grid(row = 1, column = 9)

label_linea = Label(Venta_frame, text ="             PREMIO DE LINEA",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_linea.grid(row = 0, column = 10)
entry_linea = Entry(Venta_frame,justify= RIGHT,textvariable=linea, font=("Arial",12,"bold"), width=10, state="readonly")
entry_linea.grid(row = 0, column = 11)
label_linea_E = Label(Venta_frame, text ="€",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_linea_E.grid(row = 0, column = 12)

label_prima = Label(Venta_frame, text ="           PRIMA",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_prima.grid(row = 0, column = 13)
entry_prima = Entry(Venta_frame,justify= RIGHT,textvariable=prima, font=("Arial",12,"bold"), width=10, state="readonly")
entry_prima.grid(row = 0, column = 14)
label_prima_E = Label(Venta_frame, text ="€",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_prima_E.grid(row = 0, column = 15)

label_vendidos = Label(Venta_frame, text ="               VENDIDOS",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_vendidos.grid(row = 1, column = 0) 
entry_vendidos = Entry(Venta_frame,justify= RIGHT,textvariable=vendidos, state="readonly", font=("Arial",12,"bold"), width=10)
entry_vendidos.grid(row = 1, column = 1)

label_al = Label(Venta_frame, text ="          AL",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_al.grid(row = 1, column = 3)
entry_al = Entry(Venta_frame,justify= RIGHT, state="readonly",textvariable=al, font=("Arial",12,"bold"), width=10)
entry_al.grid(row = 1, column = 4)

label_informaticos = Label(Venta_frame, text ="      INFORMÁTICOS",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_informaticos.grid(row = 1, column = 5)
entry_informaticos = Entry(Venta_frame,justify= RIGHT, state="readonly",textvariable=informaticos, font=("Arial",12,"bold"), width=10)
entry_informaticos.grid(row = 1, column = 6)

label_bingo = Label(Venta_frame, text ="            PREMIO DE BINGO",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_bingo.grid(row = 1, column = 10)
entry_bingo = Entry(Venta_frame,justify= RIGHT,textvariable=bingo, font=("Arial",12,"bold"), width=10, state="readonly")
entry_bingo.grid(row = 1, column = 11)
label_bingo_E = Label(Venta_frame, text ="€",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_bingo_E.grid(row = 1, column = 12)

label_prima_extra = Label(Venta_frame, text ="       P. EXTRA",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_prima_extra.grid(row = 1, column = 13)
entry_prima_extra = Entry(Venta_frame,justify= RIGHT,textvariable=pextra, font=("Arial",12,"bold"), width=10, state="readonly")
entry_prima_extra.grid(row = 1, column = 14)
label_prima_extra_E = Label(Venta_frame, text ="€",bg="#000099", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
label_prima_extra_E.grid(row = 1, column = 15)

marca_conexion = Label(Venta_frame, text ="En espera",bg="red", fg ="#F0F8FF", font=("Times New Roman",12,"bold"))
marca_conexion.grid(row = 0, rowspan=2, column = 16, padx=20)

marco=Frame(raiz)
marco.pack(expand=True, fill= BOTH)
marco.config(bg="lightblue")

marco0=Frame(raiz)
marco0.pack(expand=True, fill= BOTH)
marco0.config(bg="lightblue")

marcoA=Frame(raiz)
marcoA.pack(expand=True, fill= BOTH)
marcoA.config(bg="lightblue")

marcoFinal=Frame(raiz)
marcoFinal.pack(expand=True, fill= BOTH)
marcoFinal.config(bg="lightblue")

marcoIntermedioFinal=Frame(raiz)
marcoIntermedioFinal.pack(expand=True, fill= BOTH)
marcoIntermedioFinal.config(bg="lightblue")
Label(marcoIntermedioFinal, text = "",bg="lightblue", font=("Arial",3)).pack()

photoSube=PhotoImage(file=r"c:\CajaMesaControl\flechaSube.png")
photoBaja=PhotoImage(file=r"c:\CajaMesaControl\flechaBaja.png")

#variables
salida = IntVar()
salida_2 = IntVar()
salida_3 = IntVar()
salida_6 = IntVar()
totalCar = IntVar()
totalCar_2 = IntVar()

salida.set("")
salida_2.set("")
salida_3.set("")
salida_6.set("")

# ------------------------Frames precios------------------------------------------

precios_frame = Frame(marco)
precios_frame.pack(expand=True, fill= BOTH, side=LEFT)
precios_frame.config(bg="gray90")

Label(precios_frame, text = "PRECIOS",bg="gray90",fg="black", font=("Times New Roman",15)).pack(pady=36)

Label(precios_frame, text="1,5€", bg="white", fg="blue", font=("Times New Roman",22,"bold"),width=3).pack(pady=26)

Label(precios_frame, text= "2€", bg="white", fg="#8B0000", font=("Times New Roman",22,"bold"),width=3).pack()

Label(precios_frame, text= "3€", bg="white", fg="#FF1493", font=("Times New Roman",22,"bold"),width=3).pack(pady=26)

Label(precios_frame, text= "6€", bg="white", fg="#2F4F4F", font=("Times New Roman",22,"bold"),width=3).pack()

# ------------------------Frames rango 1----------------------------------------

rango1_frame = Frame(marco)
rango1_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango1_frame.config(bg="#31BFE4")

Label(rango1_frame, text = " RANGO 1",bg="#31BFE4",fg="green", font=("Times New Roman",17,"bold")).pack()

Label(rango1_frame, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

numero_series_rango1=Label(rango1_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango1.pack()
numero_series_rango1.configure(foreground="blue", bg = "white",width=3)

Label(rango1_frame, text = "SALIDAS",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

validacion = raiz.register(validar_entrada)

SalidaEntry_1 = Entry(rango1_frame, validate="key",validatecommand=(validacion, "%P"), justify= RIGHT, textvariable=salida, fg = "blue",  font=("Times New Roman",22,"bold"), width=5)
SalidaEntry_1.pack(pady = 6)
SalidaEntry_1.bind("<Return>", focus_next_window)

SalidaEntry_2 = Entry(rango1_frame, validate="key",validatecommand=(validacion, "%P"),justify= RIGHT, textvariable=salida_2, fg="#8B0000", font=("Times New Roman",22,"bold"), width=5)
SalidaEntry_2.pack(pady = 20)
SalidaEntry_2.bind("<Return>", focus_next_window_2)

SalidaEntry_3 = Entry(rango1_frame, validate="key",validatecommand=(validacion, "%P"),justify= RIGHT, textvariable=salida_3, fg="#FF1493", font=("Times New Roman",22,"bold"), width=5)
SalidaEntry_3.pack(pady = 10)
SalidaEntry_3.bind("<Return>", focus_next_window_3)

SalidaEntry_6 = Entry(rango1_frame, validate="key",validatecommand=(validacion, "%P"),justify= RIGHT, textvariable=salida_6, fg="#2F4F4F", font=("Times New Roman",22,"bold"), width=5)
SalidaEntry_6.pack(pady = 20)
SalidaEntry_6.bind("<Return>", focus_next_window_6)

#--------------------------Frame Picos-------------------------------------

rango_pico_salida_frame = Frame(marco)
rango_pico_salida_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango_pico_salida_frame.config(bg="#31BFE4")

AA = Label(rango_pico_salida_frame, text= "", bg="#31BFE4", font=("Times New Roman",1))
AA.pack(pady = 60)

pico_r1 = Label(rango_pico_salida_frame, text = "0", bg="white",fg = "blue", font=("Times New Roman",12,"bold"))
pico_r1.pack()

pico_r1_2 = Label(rango_pico_salida_frame, text = "0", bg="white",fg = "#8B0000", font=("Times New Roman",12,"bold"))
pico_r1_2.pack(pady = 38)

pico_r1_3 = Label(rango_pico_salida_frame, text = "0", bg="white",fg = "#FF1493", font=("Times New Roman",12,"bold"))
pico_r1_3.pack()

pico_r1_6 = Label(rango_pico_salida_frame, text = "0", bg="white",fg = "#2F4F4F", font=("Times New Roman",12,"bold"))
pico_r1_6.pack(pady = 40)

# ------------------------Frames rango 2----------------------------------------

rango2_frame = Frame(marco)
rango2_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango2_frame.config(bg="#C0C0C0")

label_R2 = Label(rango2_frame, text = "RANGO 2",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R2.pack()
label_R2.config(fg="black")

label_R2_series = Label(rango2_frame, text = "SERIES", font=("Times New Roman",13,"bold"))
label_R2_series.pack()
label_R2_series.configure(bg="#C0C0C0")

numero_series_rango2=Label(rango2_frame, text=0,font=("Times New Roman",18,"bold"))
numero_series_rango2.pack()
numero_series_rango2.configure(foreground="blue", bg = "white",width=3)

Label_R2_salida = Label(rango2_frame, text = "SALIDAS",bg="#C0C0C0", font=("Times New Roman",13,"bold"))
Label_R2_salida.pack()
Label_R2_salida.configure(bg="#C0C0C0")

cartones_r2 = Label(rango2_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_r2.pack()
cartones_r2_proxima = Label(rango2_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r2_proxima.pack(pady=1)

Label(rango2_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r2_2 = Label(rango2_frame, text= "0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r2_2.pack()
cartones_r2_2_proxima = Label(rango2_frame, text= "0", bg="white", fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r2_2_proxima.pack(pady=1)

Label(rango2_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r2_3= Label(rango2_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r2_3.pack()
cartones_r2_3_proxima= Label(rango2_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r2_3_proxima.pack(pady=1)

Label(rango2_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r2_6= Label(rango2_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",22,"bold"),width=5)
cartones_r2_6.pack()
cartones_r2_6_proxima= Label(rango2_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r2_6_proxima.pack(pady=1)

Label(rango2_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

# ------------------------Frames rango 3----------------------------------------

rango3_frame = Frame(marco)
rango3_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango3_frame.config(bg="gray59")

label_R3 = Label(rango3_frame, text = "RANGO 3",bg="gray59", font=("Times New Roman",17,"bold"))
label_R3.pack()
label_R3.config(fg="black")

Label(rango3_frame, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

numero_series_rango3=Label(rango3_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango3.pack()
numero_series_rango3.configure(foreground="blue", bg = "white",width=3)

Label(rango3_frame, text = "SALIDAS",bg="gray59", font=("Times New Roman",13,"bold")).pack()

cartones_r3 = Label(rango3_frame, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_r3.pack()
cartones_r3_proxima = Label(rango3_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r3_proxima.pack(pady=1)

Label(rango3_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r3_2= Label(rango3_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r3_2.pack()
cartones_r3_2_proxima = Label(rango3_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r3_2_proxima.pack(pady=1)

Label(rango3_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r3_3= Label(rango3_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r3_3.pack()
cartones_r3_3_proxima = Label(rango3_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r3_3_proxima.pack(pady=1)

Label(rango3_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r3_6= Label(rango3_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_r3_6.pack()
cartones_r3_6_proxima = Label(rango3_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r3_6_proxima.pack(pady=1)

# ------------------------Frames rango 4----------------------------------------

rango4_frame = Frame(marco)
rango4_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango4_frame.config(bg="#C0C0C0")

label_R4 = Label(rango4_frame, text = "RANGO 4",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R4.pack()
label_R4.config(fg="black")

Label(rango4_frame, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

numero_series_rango4=Label(rango4_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango4.pack()
numero_series_rango4.configure(foreground="blue", bg = "white",width=3)

Label(rango4_frame, text = "SALIDAS",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

cartones_r4 = Label(rango4_frame, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"),width=5)
cartones_r4.pack()
cartones_r4_proxima = Label(rango4_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r4_proxima.pack(pady=1)

Label(rango4_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r4_2= Label(rango4_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r4_2.pack()
cartones_r4_2_proxima = Label(rango4_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r4_2_proxima.pack(pady=1)

Label(rango4_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r4_3= Label(rango4_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r4_3.pack()
cartones_r4_3_proxima = Label(rango4_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r4_3_proxima.pack(pady=1)

Label(rango4_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r4_6= Label(rango4_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_r4_6.pack()
cartones_r4_6_proxima = Label(rango4_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r4_6_proxima.pack(pady=1)

# ------------------------Frames rango 5----------------------------------------

rango5_frame = Frame(marco)
rango5_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango5_frame.config(bg="gray59")

label_R5 = Label(rango5_frame, text = "RANGO 5",bg="gray59", font=("Times New Roman",17,"bold"))
label_R5.pack()
label_R5.config(fg="black")

Label(rango5_frame, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

numero_series_rango5=Label(rango5_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango5.pack()
numero_series_rango5.configure(foreground="blue", bg = "white",width=3)

Label(rango5_frame, text = "SALIDAS",bg="gray59", font=("Times New Roman",13,"bold")).pack()

cartones_r5 = Label(rango5_frame, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_r5.pack()
cartones_r5_proxima = Label(rango5_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r5_proxima.pack(pady=1)

Label(rango5_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r5_2= Label(rango5_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r5_2.pack()
cartones_r5_2_proxima = Label(rango5_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r5_2_proxima.pack(pady=1)

Label(rango5_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r5_3= Label(rango5_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r5_3.pack()
cartones_r5_3_proxima = Label(rango5_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r5_3_proxima.pack(pady=1)

Label(rango5_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r5_6= Label(rango5_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_r5_6.pack()
cartones_r5_6_proxima = Label(rango5_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r5_6_proxima.pack(pady=1)

# ------------------------Frames rango 6----------------------------------------

rango6_frame = Frame(marco)
rango6_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango6_frame.config(bg="#C0C0C0")

label_R6 = Label(rango6_frame, text = "RANGO 6",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R6.pack()
label_R6.config(fg="black")

Label(rango6_frame, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

numero_series_rango6=Label(rango6_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango6.pack()
numero_series_rango6.configure(foreground="blue", bg = "white",width=3)

Label(rango6_frame, text = "SALIDAS",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

cartones_r6 = Label(rango6_frame, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_r6.pack()
cartones_r6_proxima = Label(rango6_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r6_proxima.pack(pady=1)

Label(rango6_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r6_2= Label(rango6_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r6_2.pack()
cartones_r6_2_proxima = Label(rango6_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r6_2_proxima.pack(pady=1)

Label(rango6_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r6_3= Label(rango6_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r6_3.pack()
cartones_r6_3_proxima = Label(rango6_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r6_3_proxima.pack(pady=1)

Label(rango6_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r6_6= Label(rango6_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_r6_6.pack()
cartones_r6_6_proxima = Label(rango6_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r6_6_proxima.pack(pady=1)

# ------------------------Frames rango 7----------------------------------------

rango7_frame = Frame(marco)
rango7_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango7_frame.config(bg="gray59")

label_R7 = Label(rango7_frame, text = "RANGO 7",bg="gray59", font=("Times New Roman",17,"bold"))
label_R7.pack()
label_R7.config(fg="black")

Label(rango7_frame, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

numero_series_rango7=Label(rango7_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango7.pack()
numero_series_rango7.configure(foreground="blue", bg = "white",width=3)

Label(rango7_frame, text = "SALIDAS",bg="gray59", font=("Times New Roman",13,"bold")).pack()

cartones_r7 = Label(rango7_frame, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_r7.pack()
cartones_r7_proxima = Label(rango7_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r7_proxima.pack(pady=1)

Label(rango7_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r7_2= Label(rango7_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r7_2.pack()
cartones_r7_2_proxima = Label(rango7_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r7_2_proxima.pack(pady=1)

Label(rango7_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r7_3= Label(rango7_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r7_3.pack()
cartones_r7_3_proxima = Label(rango7_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r7_3_proxima.pack(pady=1)

Label(rango7_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r7_6= Label(rango7_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_r7_6.pack()
cartones_r7_6_proxima = Label(rango7_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r7_6_proxima.pack(pady=1)

# ------------------------Frames rango 8----------------------------------------

rango8_frame = Frame(marco)
rango8_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango8_frame.config(bg="#C0C0C0")

label_R8 = Label(rango8_frame, text = "RANGO 8",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R8.pack()
label_R8.config(fg="black")

Label(rango8_frame, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

numero_series_rango8=Label(rango8_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango8.pack()
numero_series_rango8.configure(foreground="blue", bg = "white",width=3)

Label(rango8_frame, text = "SALIDAS",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

cartones_r8 = Label(rango8_frame, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_r8.pack()
cartones_r8_proxima = Label(rango8_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r8_proxima.pack(pady=1)

Label(rango8_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r8_2= Label(rango8_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r8_2.pack()
cartones_r8_2_proxima = Label(rango8_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r8_2_proxima.pack(pady=1)

Label(rango8_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r8_3= Label(rango8_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r8_3.pack()
cartones_r8_3_proxima = Label(rango8_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r8_3_proxima.pack(pady=1)

Label(rango8_frame, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

cartones_r8_6= Label(rango8_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_r8_6.pack()
cartones_r8_6_proxima = Label(rango8_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r8_6_proxima.pack(pady=1)

# ------------------------Frames rango 9----------------------------------------

rango9_frame = Frame(marco)
rango9_frame.pack(expand=True, fill= BOTH, side=LEFT)
rango9_frame.config(bg="gray59")

label_R9 = Label(rango9_frame, text = "RANGO 9",bg="gray59", font=("Times New Roman",17,"bold"))
label_R9.pack()
label_R9.config(fg="black")

Label(rango9_frame, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

numero_series_rango9=Label(rango9_frame, text=0,font=("Times New Roman",22,"bold"))
numero_series_rango9.pack()
numero_series_rango9.configure(foreground="blue", bg = "white",width=3)

Label(rango9_frame, text = "SALIDAS",bg="gray59", font=("Times New Roman",13,"bold")).pack()

cartones_r9 = Label(rango9_frame, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_r9.pack()
cartones_r9_proxima = Label(rango9_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_r9_proxima.pack(pady=1)

Label(rango9_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r9_2= Label(rango9_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_r9_2.pack()
cartones_r9_2_proxima = Label(rango9_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_r9_2_proxima.pack(pady=1)

Label(rango9_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r9_3= Label(rango9_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_r9_3.pack()
cartones_r9_3_proxima = Label(rango9_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_r9_3_proxima.pack(pady=1)

Label(rango9_frame, text= "", bg="gray59", font=("Times New Roman",1),width=5).pack()

cartones_r9_6= Label(rango9_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_r9_6.pack()
cartones_r9_6_proxima = Label(rango9_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_r9_6_proxima.pack(pady=1)

# ------------------------Frames cierre----------------------------------------

cierre_frame = Frame(marco)
cierre_frame.pack(expand=True, fill= BOTH, side=LEFT)
cierre_frame.config(bg="#31BFE4")

Label(cierre_frame, text = " CIERRE ",bg="#31BFE4",fg="green", font=("Times New Roman",17,"bold")).pack()

Label(cierre_frame, text = "",bg="#31BFE4", font=("Arial",37,"bold")).pack()

Label(cierre_frame, text = "SALIDAS",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

cartones_cierre = Label(cierre_frame, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"),width=5)
cartones_cierre.pack()
cartones_cierre_proxima = Label(cierre_frame, text = "0" ,bg="white",fg="blue", font=("Times New Roman",12,"bold"),width=5)
cartones_cierre_proxima.pack(pady=1)

Label(cierre_frame, text= "", bg="#31BFE4", font=("Times New Roman",1),width=5).pack()

cartones_cierre_2= Label(cierre_frame, text="0", bg="white", fg="#8B0000", font=("Times New Roman",18,"bold"),width=5)
cartones_cierre_2.pack()
cartones_cierre_2_proxima = Label(cierre_frame, text = "0" ,bg="white",fg="#8B0000", font=("Times New Roman",12,"bold"),width=5)
cartones_cierre_2_proxima.pack(pady=1)

Label(cierre_frame, text= "", bg="#31BFE4", font=("Times New Roman",1),width=5).pack()

cartones_cierre_3= Label(cierre_frame, text="0", bg="white", fg="#FF1493", font=("Times New Roman",18,"bold"),width=5)
cartones_cierre_3.pack()
cartones_cierre_3_proxima = Label(cierre_frame, text = "0" ,bg="white",fg="#FF1493", font=("Times New Roman",12,"bold"),width=5)
cartones_cierre_3_proxima.pack(pady=1)

Label(cierre_frame, text= "", bg="#31BFE4", font=("Times New Roman",1),width=5).pack()

cartones_cierre_6= Label(cierre_frame, text="0", bg="white", fg="#2F4F4F", font=("Times New Roman",18,"bold"),width=5)
cartones_cierre_6.pack()
cartones_cierre_6_proxima = Label(cierre_frame, text = "0" ,bg="white",fg="#2F4F4F", font=("Times New Roman",12,"bold"),width=5)
cartones_cierre_6_proxima.pack(pady=1)

#------------------------------ zona botones liquída y atras------------------------------------------

var = IntVar()
var.set(2)

salida.set("")

vacio = Label(marco0, text= "", bg="lightblue", font=("Times New Roman",1),width=5)
vacio.grid(row=0, column=0, padx=100)

boton_cierra=Button(marco0, text="CIERRA", command=cerrando, bg="#2F4F4F", fg ="#F0F8FF", padx = 30, pady = 4, font=("Times New Roman", 14,"bold"),cursor="hand2", width=6, height=1 )
boton_cierra.grid(row=0, column=3, padx=500, pady=5)

boton_atras=Button(marco0, text="ATRÁS",command = atras, state = DISABLED, bg ="blue", fg = "#F0F8FF", font=("Times New Roman", 12,"bold") ,cursor="hand2")
boton_atras.grid(row = 0, column = 4)

#----------------------------------------zona liquidacion rango 1----------------------------------------------

FrameLiquiR1 = Frame(marco1)
FrameLiquiR1.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR1.config(bg="#31BFE4")

label_R1_liquidacion = Label(FrameLiquiR1, text = "RANGO 1",bg="#31BFE4", font=("Times New Roman",17,"bold"))
label_R1_liquidacion.pack()
label_R1_liquidacion.config(fg="green")

liquidacion_liqui1 = Label(FrameLiquiR1, text = "0€", bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui1.pack()

pico_salida_liqui1 = Label(FrameLiquiR1, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"))
pico_salida_liqui1.pack(side=RIGHT,anchor=NW, pady = 30)

Label(FrameLiquiR1, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr1 = Label(FrameLiquiR1, text = "0", bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr1.pack()

carton_salida_liqui1 = Label(FrameLiquiR1, text = "0", background="white",foreground="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui1.pack(pady=1)

#----------------------------------------zona liquidacion rango 2----------------------------------------------

FrameLiquiR2 = Frame(marco1)
FrameLiquiR2.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR2.config(bg="#C0C0C0")

label_R2_liquidacion = Label(FrameLiquiR2, text = "RANGO 2",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R2_liquidacion.pack()
label_R2_liquidacion.config(fg="black")

liquidacion_liqui2 = Label(FrameLiquiR2, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui2.pack()

Label(FrameLiquiR2, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr2 = Label(FrameLiquiR2, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr2.pack()

carton_salida_liqui2 = Label(FrameLiquiR2, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui2.pack(pady=1)

Label(FrameLiquiR2, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

#----------------------------------------zona liquidacion rango 3----------------------------------------------

FrameLiquiR3 = Frame(marco1)
FrameLiquiR3.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR3.config(bg="gray59")

label_R3_liquidacion = Label(FrameLiquiR3, text = "RANGO 3",bg="gray59", font=("Times New Roman",17,"bold"))
label_R3_liquidacion.pack()
label_R3_liquidacion.config(fg="black")

liquidacion_liqui3 = Label(FrameLiquiR3, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui3.pack()

Label(FrameLiquiR3, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr3 = Label(FrameLiquiR3, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr3.pack()

carton_salida_liqui3 = Label(FrameLiquiR3, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui3.pack(pady=1)

#----------------------------------------zona liquidacion rango 4----------------------------------------------

FrameLiquiR4 = Frame(marco1)
FrameLiquiR4.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR4.config(bg="#C0C0C0")

label_R4_liquidacion = Label(FrameLiquiR4, text = "RANGO 4",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R4_liquidacion.pack()
label_R4_liquidacion.config(fg="black")

liquidacion_liqui4 = Label(FrameLiquiR4, text = "0€",bg="white",fg="#800080",font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui4.pack()

Label(FrameLiquiR4, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr4 = Label(FrameLiquiR4, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr4.pack()

carton_salida_liqui4 = Label(FrameLiquiR4, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui4.pack(pady=1)

#----------------------------------------zona liquidacion rango 5----------------------------------------------

FrameLiquiR5 = Frame(marco1)
FrameLiquiR5.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR5.config(bg="gray59")

label_R5_liquidacion = Label(FrameLiquiR5, text = "RANGO 5",bg="gray59", font=("Times New Roman",17,"bold"))
label_R5_liquidacion.pack()
label_R5_liquidacion.config(fg="black")

liquidacion_liqui5 = Label(FrameLiquiR5, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui5.pack()

Label(FrameLiquiR5, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr5 = Label(FrameLiquiR5, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr5.pack()

carton_salida_liqui5 = Label(FrameLiquiR5, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui5.pack(pady=1)

#----------------------------------------zona liquidacion rango 6----------------------------------------------

FrameLiquiR6 = Frame(marco1)
FrameLiquiR6.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR6.config(bg="#C0C0C0")

label_R6_liquidacion = Label(FrameLiquiR6, text = "RANGO 6",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R6_liquidacion.pack()
label_R6_liquidacion.config(fg="black")

liquidacion_liqui6 = Label(FrameLiquiR6, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui6.pack()

Label(FrameLiquiR6, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr6 = Label(FrameLiquiR6, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr6.pack()

carton_salida_liqui6 = Label(FrameLiquiR6, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui6.pack(pady=1)

#----------------------------------------zona liquidacion rango 7----------------------------------------------

FrameLiquiR7 = Frame(marco1)
FrameLiquiR7.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR7.config(bg="gray59")

label_R7_liquidacion = Label(FrameLiquiR7, text = "RANGO 7",bg="gray59", font=("Times New Roman",17,"bold"))
label_R7_liquidacion.pack()
label_R7_liquidacion.config(fg="black")

liquidacion_liqui7 = Label(FrameLiquiR7, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui7.pack()

Label(FrameLiquiR7, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr7 = Label(FrameLiquiR7, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr7.pack()

carton_salida_liqui7 = Label(FrameLiquiR7, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui7.pack(pady=1)

#----------------------------------------zona liquidacion rango 8----------------------------------------------

FrameLiquiR8 = Frame(marco1)
FrameLiquiR8.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR8.config(bg="#C0C0C0")

label_R8_liquidacion = Label(FrameLiquiR8, text = "RANGO 8",bg="#C0C0C0", font=("Times New Roman",17,"bold"))
label_R8_liquidacion.pack()
label_R8_liquidacion.config(fg="black")

liquidacion_liqui8 = Label(FrameLiquiR8, text = "0",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui8.pack()

Label(FrameLiquiR8, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr8 = Label(FrameLiquiR8, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr8.pack()

carton_salida_liqui8 = Label(FrameLiquiR8, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui8.pack(pady=1)

#----------------------------------------zona liquidacion rango 9----------------------------------------------

FrameLiquiR9 = Frame(marco1)
FrameLiquiR9.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiR9.config(bg="gray59")

label_R9_liquidacion = Label(FrameLiquiR9, text = "RANGO 9",bg="gray59", font=("Times New Roman",17,"bold"))
label_R9_liquidacion.pack()
label_R9_liquidacion.config(fg="black")

liquidacion_liqui9 = Label(FrameLiquiR9, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui9.pack()

Label(FrameLiquiR9, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_liquidacionr9 = Label(FrameLiquiR9, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacionr9.pack()

carton_salida_liqui9 = Label(FrameLiquiR9, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui9.pack(pady=1)

#----------------------------------------zona liquidacion rango cierre----------------------------------------------

FrameLiquiCierre = Frame(marco1)
FrameLiquiCierre.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiCierre.config(bg="#31BFE4")

Label(FrameLiquiCierre, text = "CIERRE",bg="#31BFE4",fg="green", font=("Times New Roman",17,"bold")).pack()

liquidacion_liqui_cierre = Label(FrameLiquiCierre, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"),width=7)
liquidacion_liqui_cierre.pack()

pico_cierre_liqui = Label(FrameLiquiCierre, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"), width=1)
pico_cierre_liqui.pack(side=RIGHT,anchor=NW, pady = 30)

Label(FrameLiquiCierre, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_liquidacion_cierre = Label(FrameLiquiCierre, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_liquidacion_cierre.pack()

carton_salida_liqui1_cierre = Label(FrameLiquiCierre, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_liqui1_cierre.pack(pady=1)

#----------------------------------------zona liquidacion rango total----------------------------------------------

FrameLiquiTotal = Frame(marco1)
FrameLiquiTotal.pack(expand=True, fill= BOTH, side=LEFT)
FrameLiquiTotal.config(bg="dodger blue")

Label(FrameLiquiTotal, text = "TOTAL",bg="dodger blue", font=("Times New Roman",17,"bold")).pack()

liquidacion_liqui_total = Label(FrameLiquiTotal, text = "0€",bg="white",fg="#800080", font=("Times New Roman",22,"bold"), width=7)
liquidacion_liqui_total.pack()

Label(FrameLiquiTotal, text = "SERIES",bg="dodger blue", font=("Times New Roman",13,"bold")).pack()
total_series_liqui = Label(FrameLiquiTotal, text = "0",bg="white",fg ="blue", font=("Times New Roman",22,"bold"), width=4)
total_series_liqui.pack()

#----------------------------------------zona sube/baja series relleno------------------------------------------------------
rangoFinal0_frame = Frame(marcoFinal)
rangoFinal0_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal0_frame.config(bg="#C0C0C0")

Button(rangoFinal0_frame, text="Histórico", command=poner_al_frente_root, bg= "Green", fg="White",font=("Times New Roman",15,"bold"),cursor="hand2", width=7).grid(row = 0, column = 0, padx=3, pady = 10)
Button(rangoFinal0_frame, text= "RESET", command=reset, bg= "#8B0000", fg="White",font=("Times New Roman",15,"bold"),cursor="hand2", width=7).grid(row = 1, column = 0, pady = 10)
Button(rangoFinal0_frame, text= "SALIR", command= salir, bg= "red", fg="White", font=("Times New Roman",15,"bold"),cursor="hand2", width=7).grid(row = 2, column = 0)

#----------------------------------------zona sube/baja series rango 1-------------------
rangoFinal1_frame = Frame(marcoFinal)
rangoFinal1_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal1_frame.config(bg="gray59")

Label(rangoFinal1_frame, text = "  RANGO 1  ",bg="gray59", font=("Times New Roman",15,"bold")).pack()

Label(rangoFinal1_frame, text = "SERIES",bg="gray59", font=("Arial",10,"bold")).pack()

numero_series1=Label(rangoFinal1_frame, text=valor1,font=("Times New Roman",17,"bold"), width=2)
numero_series1.pack()
numero_series1.configure(foreground="blue", bg = "white")

Label(rangoFinal1_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_series1=Button(rangoFinal1_frame, command= lambda: incrementar(1), bg = "gray59", image=photoSube, padx = 10, pady=2,cursor="hand2")
boton_sube_series1.pack()

Label(rangoFinal1_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_ahora=Button(rangoFinal1_frame, text="  Subir  ",command=lambda: subir_individual(1), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal1_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_baja_series1=Button(rangoFinal1_frame, command= lambda: decrementar(1), bg = "gray59", image=photoBaja, padx = 10,cursor="hand2" )
boton_baja_series1.pack()

#----------------------------------------zona sube/baja series rango 2------------------------------------------------------

rangoFinal2_frame = Frame(marcoFinal)
rangoFinal2_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal2_frame.config(bg="#C0C0C0")

Label(rangoFinal2_frame, text = " RANGO 2 ",bg="#C0C0C0", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal2_frame, text = "SERIES",bg="#C0C0C0", font=("Arial",10,"bold")).pack()

numero_series2=Label(rangoFinal2_frame, text=valor2,font=("Times New Roman",17,"bold"), width=2)
numero_series2.pack()
numero_series2.configure(foreground="blue", bg = "white")

Label(rangoFinal2_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_series2=Button(rangoFinal2_frame, text="R2 +", command= lambda: incrementar(2), bg = "#C0C0C0", image=photoSube, padx = 10,cursor="hand2" )
boton_sube_series2.pack()

Label(rangoFinal2_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_ahora=Button(rangoFinal2_frame, text="  Subir  ",command= lambda: subir_individual(2), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal2_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_baja_series2=Button(rangoFinal2_frame, text="R2 -", command= lambda: decrementar(2), bg = "#C0C0C0", image=photoBaja, padx = 10,cursor="hand2")
boton_baja_series2.pack()

#----------------------------------------zona sube/baja series rango 3------------------------------------------------------

rangoFinal3_frame = Frame(marcoFinal)
rangoFinal3_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal3_frame.config(bg="gray59")

Label(rangoFinal3_frame, text = " RANGO 3 ",bg="gray59", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal3_frame, text = "SERIES",bg="gray59", font=("Arial",10,"bold")).pack()

numero_series3=Label(rangoFinal3_frame, text=valor3, font=("Times New Roman",17,"bold"), width=2)
numero_series3.pack()
numero_series3.configure(foreground="blue", bg = "white")

Label(rangoFinal3_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_series3=Button(rangoFinal3_frame, text="R3 +", command= lambda: incrementar(3), bg = "gray59", image=photoSube, padx = 10,cursor="hand2")
boton_sube_series3.pack()
boton_sube_series3.configure()

Label(rangoFinal3_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_ahora=Button(rangoFinal3_frame, text="  Subir  ", command=lambda: subir_individual(3), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal3_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_baja_series3=Button(rangoFinal3_frame, text="R3 -", command= lambda: decrementar(3), bg = "gray59", image=photoBaja, padx = 10,cursor="hand2" )
boton_baja_series3.pack()

#----------------------------------------zona sube/baja series rango 4------------------------------------------------------

rangoFinal4_frame = Frame(marcoFinal)
rangoFinal4_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal4_frame.config(bg="#C0C0C0")

Label(rangoFinal4_frame, text = " RANGO 4 ",bg="#C0C0C0", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal4_frame, text = "SERIES",bg="#C0C0C0", font=("Arial",10,"bold")).pack()

numero_series4=Label(rangoFinal4_frame, text=valor4,font=("Times New Roman",17,"bold"), width=2)
numero_series4.pack()
numero_series4.configure(foreground="blue", bg = "white")

Label(rangoFinal4_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_series4=Button(rangoFinal4_frame, text="R4 +", command= lambda: incrementar(4), bg = "#C0C0C0", image=photoSube, padx = 10,cursor="hand2")
boton_sube_series4.pack()

Label(rangoFinal4_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_ahora=Button(rangoFinal4_frame, text="  Subir  ", command=lambda: subir_individual(4), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal4_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_baja_series4=Button(rangoFinal4_frame, text="R4 -", command= lambda: decrementar(4), bg = "#C0C0C0", image=photoBaja, padx = 10,cursor="hand2")
boton_baja_series4.pack()

#----------------------------------------zona sube/baja series rango 5------------------------------------------------------

rangoFinal5_frame = Frame(marcoFinal)
rangoFinal5_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal5_frame.config(bg="gray59")

Label(rangoFinal5_frame, text = " RANGO 5 ",bg="gray59", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal5_frame, text = "SERIES",bg="gray59", font=("Arial",10,"bold")).pack()

numero_series5=Label(rangoFinal5_frame, text=valor5,font=("Times New Roman",17,"bold"), width=2)
numero_series5.pack()
numero_series5.configure(foreground="blue", bg = "white")

Label(rangoFinal5_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_series5=Button(rangoFinal5_frame, text="R5 +", command= lambda: incrementar(5), bg = "gray59", image=photoSube, padx = 10,cursor="hand2" )
boton_sube_series5.pack()

Label(rangoFinal5_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_ahora=Button(rangoFinal5_frame, text="  Subir  ", command=lambda: subir_individual(5), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal5_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_baja_series5=Button(rangoFinal5_frame, text="R5 -", command= lambda: decrementar(5), bg = "gray59", image=photoBaja, padx = 10,cursor="hand2" )
boton_baja_series5.pack()

#----------------------------------------zona sube/baja series rango 6------------------------------------------------------

rangoFinal6_frame = Frame(marcoFinal)
rangoFinal6_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal6_frame.config(bg="#C0C0C0")

Label(rangoFinal6_frame, text = " RANGO 6 ",bg="#C0C0C0", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal6_frame, text = "SERIES",bg="#C0C0C0", font=("Arial",10,"bold")).pack()

numero_series6=Label(rangoFinal6_frame, text=valor6,font=("Times New Roman",17,"bold"), width=2)
numero_series6.pack()
numero_series6.configure(foreground="blue", bg = "white")

Label(rangoFinal6_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_series6=Button(rangoFinal6_frame, text="R6 +", command= lambda: incrementar(6), bg = "#C0C0C0", image=photoSube, padx = 10 ,cursor="hand2")
boton_sube_series6.pack()

Label(rangoFinal6_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_ahora=Button(rangoFinal6_frame, text="  Subir  ", command=lambda: subir_individual(6), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal6_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_baja_series6=Button(rangoFinal6_frame, text="R6 -", command= lambda: decrementar(6), bg = "#C0C0C0", image=photoBaja, padx = 10,cursor="hand2" )
boton_baja_series6.pack()

#----------------------------------------zona sube/baja series rango 7------------------------------------------------------

rangoFinal7_frame = Frame(marcoFinal)
rangoFinal7_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal7_frame.config(bg="gray59")

Label(rangoFinal7_frame, text = " RANGO 7 ",bg="gray59", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal7_frame, text = "SERIES",bg="gray59", font=("Arial",10,"bold")).pack()

numero_series7=Label(rangoFinal7_frame, text=valor7,font=("Times New Roman",17,"bold"), width=2)
numero_series7.pack()
numero_series7.configure(foreground="blue", bg = "white")

Label(rangoFinal7_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_series7=Button(rangoFinal7_frame, text="R7 +", command= lambda: incrementar(7), bg = "gray59", image=photoSube, padx = 10,cursor="hand2" )
boton_sube_series7.pack()

Label(rangoFinal7_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_ahora=Button(rangoFinal7_frame, text="  Subir  ", command=lambda: subir_individual(7), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal7_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_baja_series7=Button(rangoFinal7_frame, text="R7 -", command= lambda: decrementar(7), bg = "gray59", image=photoBaja, padx = 10,cursor="hand2" )
boton_baja_series7.pack()

#----------------------------------------zona sube/baja series rango 8------------------------------------------------------

rangoFinal8_frame = Frame(marcoFinal)
rangoFinal8_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal8_frame.config(bg="#C0C0C0")

Label(rangoFinal8_frame, text = " RANGO 8 ",bg="#C0C0C0", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal8_frame, text = "SERIES",bg="#C0C0C0", font=("Arial",10,"bold")).pack()

numero_series8=Label(rangoFinal8_frame, text=valor8,font=("Times New Roman",17,"bold"), width=2)
numero_series8.pack()
numero_series8.configure(foreground="blue", bg = "white")

Label(rangoFinal8_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_series8=Button(rangoFinal8_frame, text="R8 +", command= lambda: incrementar(8), bg = "#C0C0C0", image=photoSube, padx = 10,cursor="hand2" )
boton_sube_series8.pack()

Label(rangoFinal8_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_sube_ahora=Button(rangoFinal8_frame, text="  Subir  ", command=lambda: subir_individual(8), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal8_frame, text="",font=("Arial",1),bg = "#C0C0C0").pack()

boton_baja_series8=Button(rangoFinal8_frame, text="R8 -", command= lambda: decrementar(8), bg = "#C0C0C0", image=photoBaja, padx = 10,cursor="hand2" )
boton_baja_series8.pack()

#----------------------------------------zona sube/baja series rango 9------------------------------------------------------

rangoFinal9_frame = Frame(marcoFinal)
rangoFinal9_frame.pack(expand=True, fill= BOTH, side=LEFT)
rangoFinal9_frame.config(bg="gray59")

Label(rangoFinal9_frame, text = " RANGO 9 ",bg="gray59", font=("Times New Roman",15,"bold")).pack()
Label(rangoFinal9_frame, text = "SERIES",bg="gray59", font=("Arial",10,"bold")).pack()

numero_series9=Label(rangoFinal9_frame, text=valor9,font=("Times New Roman",17,"bold"), width=2)
numero_series9.pack()
numero_series9.configure(foreground="blue", bg = "white")

Label(rangoFinal9_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_series9=Button(rangoFinal9_frame, text="R9 +", command= lambda: incrementar(9), bg = "gray59", image=photoSube, padx = 10 ,cursor="hand2")
boton_sube_series9.pack()

Label(rangoFinal9_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_sube_ahora=Button(rangoFinal9_frame, text="  Subir  ", command=lambda: subir_individual(9), bg="#8B0000", fg ="#F0F8FF",cursor="hand2")
boton_sube_ahora.pack()

Label(rangoFinal9_frame, text="",font=("Arial",1),bg = "gray59").pack()

boton_baja_series9=Button(rangoFinal9_frame, text="R9 -", command= lambda: decrementar(9), bg = "gray59", image=photoBaja, padx = 10 ,cursor="hand2")
boton_baja_series9.pack()

Label(rangoFinal9_frame, text = "",bg="gray59", font=("Arial",3)).pack()

#----------------------------------------zona sube/baja series cierre------------------------------------------------------

cierreFinal_frame = Frame(marcoFinal)
cierreFinal_frame.pack(expand=True, fill= BOTH, side=LEFT)
cierreFinal_frame.config(bg="#31BFE4")

etiqueta_vacia=Label(cierreFinal_frame, text = "",bg="#31BFE4", font=("Arial", 30))
etiqueta_vacia.pack()
etiqueta_automatic=Label(cierreFinal_frame, text = "Las series preparadas se asignan\nAUTOMATICAMENTE al cerrar.\nSOLO para CORREGIR series\n OLVIDADAS al cerrar pulse este botón",bg="#31BFE4", font=("Arial", 10))
etiquita_instrucciones=Label(cierreFinal_frame, text = "SOLO si desea modificar series\nasígnelas y pulse este botón\nDOS VECES",bg="#31BFE4", font=("Arial", 12))
boton_prepara_rectifica=Button(cierreFinal_frame, text="  COMENZAR  ",command = PreparaRectifica, bg="#8B0000", fg ="#F0F8FF", padx = 22, pady = 4, font=("Times New Roman", 15,"bold"),cursor="hand2" )
boton_prepara_rectifica.pack()
etiquita_instrucciones_inicial=Label(cierreFinal_frame, text = "Prepare series y pulse\neste botón para comenzar", font=("Arial", 14))
etiquita_instrucciones_inicial.pack()
etiquita_instrucciones_inicial.config(foreground="black", background="#31BFE4")

parpadeo_inicial(etiquita_instrucciones_inicial)

#---------------------------------------------------------------------------------------------------------------------

#SalidaEntry_1.focus_set()

# Ventana historico

root = Toplevel()
root.title("Historico")
root.attributes('-fullscreen', True)
root.config(bg="#000099")

medio = Frame(root)
medio.config(bg="white")
medio.pack()
Label(medio, text="PARTIDA ACTUAL", bg="#000099", fg="white", font=("Times New Roman",15,"bold")).pack()

# Historico 1
marco_historico_1 = Frame(root)
marco_historico_1.pack(expand=True, fill= BOTH)
marco_historico_1.config(bg="lightblue")

# Historico_1 rango_1
frame_histortico_1_rango_1 = Frame(marco_historico_1)
frame_histortico_1_rango_1.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_1.config(bg="#31BFE4")

label_historico_1_rango1 = Label(frame_histortico_1_rango_1, text = "RANGO 1",bg="#31BFE4", font=("Times New Roman",16,"bold"))
label_historico_1_rango1.pack()

liquidacion_historico_1_rango1 = Label(frame_histortico_1_rango_1, text = "0€", bg="white",fg="#800080", font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango1.pack()

pico_salida_historico_1_rango_1 = Label(frame_histortico_1_rango_1, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"))
pico_salida_historico_1_rango_1.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_1_rango_1, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_1 = Label(frame_histortico_1_rango_1, text = "0", bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_1.pack()

carton_salida_historico_1_rango_1 = Label(frame_histortico_1_rango_1, text = "0", background="white",foreground="blue", font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_1.pack(pady=1)

# Historico_1 rango_2
frame_histortico_1_rango_2 = Frame(marco_historico_1)
frame_histortico_1_rango_2.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_2.config(bg="#C0C0C0")

label_historico_1_rango2 = Label(frame_histortico_1_rango_2, text = "RANGO 2",bg="#C0C0C0", font=("Times New Roman",16,"bold"))
label_historico_1_rango2.pack()
label_historico_1_rango2.config(fg="black")

liquidacion_historico_1_rango2 = Label(frame_histortico_1_rango_2, text = "0€",bg="white",fg="#800080", font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango2.pack()

Label(frame_histortico_1_rango_2, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_2 = Label(frame_histortico_1_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_2.pack()

carton_salida_historico_1_rango_2 = Label(frame_histortico_1_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_2.pack(pady=1)

# Historico_1 rango_3
frame_histortico_1_rango_3 = Frame(marco_historico_1)
frame_histortico_1_rango_3.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_3.config(bg="gray59")

label_historico_1_rango2 = Label(frame_histortico_1_rango_3, text = "RANGO 3",bg="gray59", font=("Times New Roman",16,"bold"))
label_historico_1_rango2.pack()
label_historico_1_rango2.config(fg="black")

liquidacion_historico_1_rango3 = Label(frame_histortico_1_rango_3, text = "0€",bg="white",fg="#800080", font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango3.pack()

Label(frame_histortico_1_rango_3, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_3 = Label(frame_histortico_1_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_3.pack()

carton_salida_historico_1_rango_3 = Label(frame_histortico_1_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_3.pack(pady=1)

# Historico_1 rango_4
frame_histortico_1_rango_4 = Frame(marco_historico_1)
frame_histortico_1_rango_4.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_4.config(bg="#C0C0C0")

label_historico_1_rango4 = Label(frame_histortico_1_rango_4, text = "RANGO 4",bg="#C0C0C0", font=("Times New Roman",16,"bold"))
label_historico_1_rango4.pack()
label_historico_1_rango4.config(fg="black")

liquidacion_historico_1_rango4 = Label(frame_histortico_1_rango_4, text = "0€",bg="white",fg="#800080",font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango4.pack()

Label(frame_histortico_1_rango_4, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_4 = Label(frame_histortico_1_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_4.pack()

carton_salida_historico_1_rango_4 = Label(frame_histortico_1_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_4.pack(pady=1)

# Historico_1 rango_5
frame_histortico_1_rango_5 = Frame(marco_historico_1)
frame_histortico_1_rango_5.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_5.config(bg="gray59")

label_historico_1_rango5 = Label(frame_histortico_1_rango_5, text = "RANGO 5",bg="gray59", font=("Times New Roman",16,"bold"))
label_historico_1_rango5.pack()
label_historico_1_rango5.config(fg="black")

liquidacion_historico_1_rango5 = Label(frame_histortico_1_rango_5, text = "0€",bg="white",fg="#800080",font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango5.pack()

Label(frame_histortico_1_rango_5, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_5 = Label(frame_histortico_1_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_5.pack()

carton_salida_historico_1_rango_5 = Label(frame_histortico_1_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_5.pack(pady=1)

# Historico_1 rango_6
frame_histortico_1_rango_6 = Frame(marco_historico_1)
frame_histortico_1_rango_6.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_6.config(bg="#C0C0C0")

label_historico_1_rango6 = Label(frame_histortico_1_rango_6, text = "RANGO 6",bg="#C0C0C0", font=("Times New Roman",16,"bold"))
label_historico_1_rango6.pack()
label_historico_1_rango6.config(fg="black")

liquidacion_historico_1_rango6 = Label(frame_histortico_1_rango_6, text = "0€",bg="white",fg="#800080",font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango6.pack()

Label(frame_histortico_1_rango_6, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_6 = Label(frame_histortico_1_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_6.pack()

carton_salida_historico_1_rango_6 = Label(frame_histortico_1_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_6.pack(pady=1)

# Historico 1 rango_7
frame_histortico_1_rango_7 = Frame(marco_historico_1)
frame_histortico_1_rango_7.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_7.config(bg="gray59")

label_historico_1_rango7 = Label(frame_histortico_1_rango_7, text = "RANGO 7",bg="gray59", font=("Times New Roman",16,"bold"))
label_historico_1_rango7.pack()
label_historico_1_rango7.config(fg="black")

liquidacion_historico_1_rango7 = Label(frame_histortico_1_rango_7, text = "0€",bg="white",fg="#800080",font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango7.pack()

Label(frame_histortico_1_rango_7, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_7 = Label(frame_histortico_1_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_7.pack()

carton_salida_historico_1_rango_7 = Label(frame_histortico_1_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_7.pack(pady=1)

# Historico_1 rango_8
frame_histortico_1_rango_8 = Frame(marco_historico_1)
frame_histortico_1_rango_8.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_8.config(bg="#C0C0C0")

label_historico_1_rango8 = Label(frame_histortico_1_rango_8, text = "RANGO 8",bg="#C0C0C0", font=("Times New Roman",16,"bold"))
label_historico_1_rango8.pack()
label_historico_1_rango8.config(fg="black")

liquidacion_historico_1_rango8 = Label(frame_histortico_1_rango_8, text = "0€",bg="white",fg="#800080",font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango8.pack()

Label(frame_histortico_1_rango_8, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_8 = Label(frame_histortico_1_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_8.pack()

carton_salida_historico_1_rango_8 = Label(frame_histortico_1_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_8.pack(pady=1)

# Historico_1 rango_9
frame_histortico_1_rango_9 = Frame(marco_historico_1)
frame_histortico_1_rango_9.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_rango_9.config(bg="gray59")

label_historico_1_rango9 = Label(frame_histortico_1_rango_9, text = "RANGO 9",bg="gray59", font=("Times New Roman",16,"bold"))
label_historico_1_rango9.pack()
label_historico_1_rango9.config(fg="black")

liquidacion_historico_1_rango9 = Label(frame_histortico_1_rango_9, text = "0€",bg="white",fg="#800080",font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_rango9.pack()

Label(frame_histortico_1_rango_9, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_1_rango_9 = Label(frame_histortico_1_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=2)
series_histirico_1_rango_9.pack()

carton_salida_historico_1_rango_9 = Label(frame_histortico_1_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_rango_9.pack(pady=1)

# Historico 1 Cierre
frame_histortico_1_cierre = Frame(marco_historico_1)
frame_histortico_1_cierre.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_1_cierre.config(bg="#31BFE4")

Label(frame_histortico_1_cierre, text = "CIERRE",bg="#31BFE4", font=("Times New Roman",16,"bold")).pack()

liquidacion_historico_1_cierre = Label(frame_histortico_1_cierre, text = "0€",bg="white",fg="#800080", font=("Times New Roman",18,"bold"),width=7)
liquidacion_historico_1_cierre.pack()

pico_historico_1_cierre = Label(frame_histortico_1_cierre, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"), width=1)
pico_historico_1_cierre.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_1_cierre, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_historico_1_cierre = Label(frame_histortico_1_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=2)
series_historico_1_cierre.pack()

carton_salida_historico_1_cierre = Label(frame_histortico_1_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",16,"bold"), width=8)
carton_salida_historico_1_cierre.pack(pady=1)

# historico 1 total

Frame_historico_1_Total = Frame(marco_historico_1)
Frame_historico_1_Total.pack(expand=True, fill= BOTH, side=LEFT)
Frame_historico_1_Total.config(bg="dodger blue")

Label(Frame_historico_1_Total, text = "TOTAL",bg="dodger blue", font=("Times New Roman",16,"bold")).pack()

liquidacion_historico_1_total = Label(Frame_historico_1_Total, text = "0€",bg="white",fg="#800080", font=("Times New Roman",18,"bold"), width=7)
liquidacion_historico_1_total.pack()

Label(Frame_historico_1_Total, text = "SERIES",bg="dodger blue", font=("Times New Roman",13,"bold")).pack()
total_series_historico_1 = Label(Frame_historico_1_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",18,"bold"), width=4)
total_series_historico_1.pack()
Label(Frame_historico_1_Total, text = "CARTONES",bg="dodger blue", font=("Times New Roman",8,"bold")).pack()

total_cartones_historico_1 = Label(Frame_historico_1_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",15,"bold"), width=8)
total_cartones_historico_1.pack(pady=2)

# Medio 1
medio1 = Frame(root)
medio1.config(bg="white")
medio1.pack()
Label(medio1, text="PARTIDAS ANTERIONES",bg="#000099", fg="white", font=("Times New Roman",15,"bold")).pack()

# Historico 2
marco_historico_2 = Frame(root)
marco_historico_2.pack(expand=True, fill= BOTH)
marco_historico_2.config(bg="lightblue")

# Historico_2 rango_1
frame_histortico_2_rango_1 = Frame(marco_historico_2)
frame_histortico_2_rango_1.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_1.config(bg="#31BFE4")

pico_salida_historico_2_rango_1 = Label(frame_histortico_2_rango_1, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"))
pico_salida_historico_2_rango_1.pack(side=RIGHT,anchor=NW, pady = 30)


Label(frame_histortico_2_rango_1, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_1 = Label(frame_histortico_2_rango_1, text = "0", bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_1.pack()

carton_salida_historico_2_rango_1 = Label(frame_histortico_2_rango_1, text = "0", background="white",foreground="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_1.pack(pady=1)

# Historico_2 rango_2
frame_histortico_2_rango_2 = Frame(marco_historico_2)
frame_histortico_2_rango_2.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_2.config(bg="#C0C0C0")

Label(frame_histortico_2_rango_2, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_2 = Label(frame_histortico_2_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_2.pack()

carton_salida_historico_2_rango_2 = Label(frame_histortico_2_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_2.pack(pady=1)

Label(frame_histortico_2_rango_2, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

# Historico 2 rango_3
frame_histortico_2_rango_3 = Frame(marco_historico_2)
frame_histortico_2_rango_3.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_3.config(bg="gray59")

Label(frame_histortico_2_rango_3, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_3 = Label(frame_histortico_2_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_3.pack()

carton_salida_historico_2_rango_3 = Label(frame_histortico_2_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_3.pack(pady=1)

# Historico 2 rango_4
frame_histortico_2_rango_4 = Frame(marco_historico_2)
frame_histortico_2_rango_4.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_4.config(bg="#C0C0C0")

Label(frame_histortico_2_rango_4, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_4 = Label(frame_histortico_2_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_4.pack()

carton_salida_historico_2_rango_4 = Label(frame_histortico_2_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_4.pack(pady=1)

# Historico 2 rango_5
frame_histortico_2_rango_5 = Frame(marco_historico_2)
frame_histortico_2_rango_5.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_5.config(bg="gray59")

Label(frame_histortico_2_rango_5, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_5 = Label(frame_histortico_2_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_5.pack()

carton_salida_historico_2_rango_5 = Label(frame_histortico_2_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_5.pack(pady=1)

# Historico 2 rango_6
frame_histortico_2_rango_6 = Frame(marco_historico_2)
frame_histortico_2_rango_6.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_6.config(bg="#C0C0C0")

Label(frame_histortico_2_rango_6, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_6 = Label(frame_histortico_2_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_6.pack()

carton_salida_historico_2_rango_6 = Label(frame_histortico_2_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_6.pack(pady=1)

# Historico_2 rango_7
frame_histortico_2_rango_7 = Frame(marco_historico_2)
frame_histortico_2_rango_7.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_7.config(bg="gray59")

Label(frame_histortico_2_rango_7, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_7 = Label(frame_histortico_2_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_7.pack()

carton_salida_historico_2_rango_7 = Label(frame_histortico_2_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_7.pack(pady=1)

# Historico_2 rango_8
frame_histortico_2_rango_8 = Frame(marco_historico_2)
frame_histortico_2_rango_8.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_8.config(bg="#C0C0C0")

Label(frame_histortico_2_rango_8, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_8 = Label(frame_histortico_2_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_8.pack()

carton_salida_historico_2_rango_8 = Label(frame_histortico_2_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_8.pack(pady=1)

# Historico_2 rango_9
frame_histortico_2_rango_9 = Frame(marco_historico_2)
frame_histortico_2_rango_9.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_rango_9.config(bg="gray59")

Label(frame_histortico_2_rango_9, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_2_rango_9 = Label(frame_histortico_2_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_2_rango_9.pack()

carton_salida_historico_2_rango_9 = Label(frame_histortico_2_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_rango_9.pack(pady=1)

# Historico 2 Cierre
frame_histortico_2_cierre = Frame(marco_historico_2)
frame_histortico_2_cierre.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_2_cierre.config(bg="#31BFE4")

pico_historico_2_cierre = Label(frame_histortico_2_cierre, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"), width=1)
pico_historico_2_cierre.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_2_cierre, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_historico_2_cierre = Label(frame_histortico_2_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_historico_2_cierre.pack()

carton_salida_historico_2_cierre = Label(frame_histortico_2_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_2_cierre.pack(pady=1)

# historico 2 liquidacion

Frame_historico_2_Total = Frame(marco_historico_2)
Frame_historico_2_Total.pack(expand=True, fill= BOTH, side=LEFT)
Frame_historico_2_Total.config(bg="dodger blue")

Label(Frame_historico_2_Total, text = "SERIES",bg="dodger blue", font=("Times New Roman",13,"bold")).pack()
total_series_historico_2 = Label(Frame_historico_2_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",22,"bold"), width=4)
total_series_historico_2.pack()
Label(Frame_historico_2_Total, text = "CARTONES",bg="dodger blue", font=("Times New Roman",8,"bold")).pack()

total_cartones_historico_2 = Label(Frame_historico_2_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",15,"bold"), width=8)
total_cartones_historico_2.pack(pady=2)

# Medio 2
medio2 = Frame(root)
medio2.config(bg="white")
medio2.pack()
Label(medio2, text="",bg="#000099", font=("Times New Roman",2,"bold")).pack()

# Historico 3
marco_historico_3 = Frame(root)
marco_historico_3.pack(expand=True, fill= BOTH)
marco_historico_3.config(bg="lightblue")

# Historico_3 rango_1
frame_histortico_3_rango_1 = Frame(marco_historico_3)
frame_histortico_3_rango_1.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_1.config(bg="#31BFE4")

pico_salida_historico_3_rango_1 = Label(frame_histortico_3_rango_1, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"))
pico_salida_historico_3_rango_1.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_3_rango_1, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_1 = Label(frame_histortico_3_rango_1, text = "0", bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_1.pack()

carton_salida_historico_3_rango_1 = Label(frame_histortico_3_rango_1, text = "0", background="white",foreground="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_1.pack(pady=1)

# Historico_3 rango_2
frame_histortico_3_rango_2 = Frame(marco_historico_3)
frame_histortico_3_rango_2.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_2.config(bg="#C0C0C0")

Label(frame_histortico_3_rango_2, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_2 = Label(frame_histortico_3_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_2.pack()

carton_salida_historico_3_rango_2 = Label(frame_histortico_3_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_2.pack(pady=1)

Label(frame_histortico_3_rango_2, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

# Historico 3 rango_3
frame_histortico_3_rango_3 = Frame(marco_historico_3)
frame_histortico_3_rango_3.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_3.config(bg="gray59")

Label(frame_histortico_3_rango_3, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_3 = Label(frame_histortico_3_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_3.pack()

carton_salida_historico_3_rango_3 = Label(frame_histortico_3_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_3.pack(pady=1)

# Historico 3 rango_4
frame_histortico_3_rango_4 = Frame(marco_historico_3)
frame_histortico_3_rango_4.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_4.config(bg="#C0C0C0")

Label(frame_histortico_3_rango_4, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_4 = Label(frame_histortico_3_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_4.pack()

carton_salida_historico_3_rango_4 = Label(frame_histortico_3_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_4.pack(pady=1)

# Historico 3 rango_5
frame_histortico_3_rango_5 = Frame(marco_historico_3)
frame_histortico_3_rango_5.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_5.config(bg="gray59")

Label(frame_histortico_3_rango_5, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_5 = Label(frame_histortico_3_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_5.pack()

carton_salida_historico_3_rango_5 = Label(frame_histortico_3_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_5.pack(pady=1)

# Historico 3 rango_6
frame_histortico_3_rango_6 = Frame(marco_historico_3)
frame_histortico_3_rango_6.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_6.config(bg="#C0C0C0")

Label(frame_histortico_3_rango_6, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_6 = Label(frame_histortico_3_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_6.pack()

carton_salida_historico_3_rango_6 = Label(frame_histortico_3_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_6.pack(pady=1)

# Historico_3 rango_7
frame_histortico_3_rango_7 = Frame(marco_historico_3)
frame_histortico_3_rango_7.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_7.config(bg="gray59")

Label(frame_histortico_3_rango_7, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_7 = Label(frame_histortico_3_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_7.pack()

carton_salida_historico_3_rango_7 = Label(frame_histortico_3_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_7.pack(pady=1)

# Historico_3 rango_8
frame_histortico_3_rango_8 = Frame(marco_historico_3)
frame_histortico_3_rango_8.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_8.config(bg="#C0C0C0")

Label(frame_histortico_3_rango_8, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_8 = Label(frame_histortico_3_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_8.pack()

carton_salida_historico_3_rango_8 = Label(frame_histortico_3_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_8.pack(pady=1)

# Historico_3 rango_9
frame_histortico_3_rango_9 = Frame(marco_historico_3)
frame_histortico_3_rango_9.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_rango_9.config(bg="gray59")

Label(frame_histortico_3_rango_9, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_3_rango_9 = Label(frame_histortico_3_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_3_rango_9.pack()

carton_salida_historico_3_rango_9 = Label(frame_histortico_3_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_rango_9.pack(pady=1)

# Historico 3 Cierre
frame_histortico_3_cierre = Frame(marco_historico_3)
frame_histortico_3_cierre.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_3_cierre.config(bg="#31BFE4")

pico_historico_3_cierre = Label(frame_histortico_3_cierre, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"), width=1)
pico_historico_3_cierre.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_3_cierre, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_historico_3_cierre = Label(frame_histortico_3_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_historico_3_cierre.pack()

carton_salida_historico_3_cierre = Label(frame_histortico_3_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_3_cierre.pack(pady=1)

# historico 3 liquidacion

Frame_historico_3_Total = Frame(marco_historico_3)
Frame_historico_3_Total.pack(expand=True, fill= BOTH, side=LEFT)
Frame_historico_3_Total.config(bg="dodger blue")

Label(Frame_historico_3_Total, text = "SERIES",bg="dodger blue", font=("Times New Roman",13,"bold")).pack()
total_series_historico_3 = Label(Frame_historico_3_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",22,"bold"), width=4)
total_series_historico_3.pack()
Label(Frame_historico_3_Total, text = "CARTONES",bg="dodger blue", font=("Times New Roman",8,"bold")).pack()

total_cartones_historico_3 = Label(Frame_historico_3_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",15,"bold"), width=8)
total_cartones_historico_3.pack(pady=2)

# Medio 3
medio3 = Frame(root)
medio3.config(bg="white")
medio3.pack()
Label(medio3, text="",bg="#000099", font=("Times New Roman",2,"bold")).pack()

# Historico 4
marco_historico_4 = Frame(root)
marco_historico_4.pack(expand=True, fill= BOTH)
marco_historico_4.config(bg="lightblue")

# Historico_4 rango_1
frame_histortico_4_rango_1 = Frame(marco_historico_4)
frame_histortico_4_rango_1.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_1.config(bg="#31BFE4")

pico_salida_historico_4_rango_1 = Label(frame_histortico_4_rango_1, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"))
pico_salida_historico_4_rango_1.pack(side=RIGHT,anchor=NW, pady = 30)


Label(frame_histortico_4_rango_1, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_1 = Label(frame_histortico_4_rango_1, text = "0", bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_1.pack()

carton_salida_historico_4_rango_1 = Label(frame_histortico_4_rango_1, text = "0", background="white",foreground="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_1.pack(pady=1)

# Historico_4 rango_2
frame_histortico_4_rango_2 = Frame(marco_historico_4)
frame_histortico_4_rango_2.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_2.config(bg="#C0C0C0")

Label(frame_histortico_4_rango_2, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_2 = Label(frame_histortico_4_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_2.pack()

carton_salida_historico_4_rango_2 = Label(frame_histortico_4_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_2.pack(pady=1)

Label(frame_histortico_4_rango_2, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

# Historico 4 rango_3
frame_histortico_4_rango_3 = Frame(marco_historico_4)
frame_histortico_4_rango_3.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_3.config(bg="gray59")

Label(frame_histortico_4_rango_3, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_3 = Label(frame_histortico_4_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_3.pack()

carton_salida_historico_4_rango_3 = Label(frame_histortico_4_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_3.pack(pady=1)

# Historico 4 rango_4
frame_histortico_4_rango_4 = Frame(marco_historico_4)
frame_histortico_4_rango_4.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_4.config(bg="#C0C0C0")

Label(frame_histortico_4_rango_4, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_4 = Label(frame_histortico_4_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_4.pack()

carton_salida_historico_4_rango_4 = Label(frame_histortico_4_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_4.pack(pady=1)

# Historico 4 rango_5
frame_histortico_4_rango_5 = Frame(marco_historico_4)
frame_histortico_4_rango_5.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_5.config(bg="gray59")

Label(frame_histortico_4_rango_5, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_5 = Label(frame_histortico_4_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_5.pack()

carton_salida_historico_4_rango_5 = Label(frame_histortico_4_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_5.pack(pady=1)

# Historico 4 rango_6
frame_histortico_4_rango_6 = Frame(marco_historico_4)
frame_histortico_4_rango_6.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_6.config(bg="#C0C0C0")

Label(frame_histortico_4_rango_6, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_6 = Label(frame_histortico_4_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_6.pack()

carton_salida_historico_4_rango_6 = Label(frame_histortico_4_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_6.pack(pady=1)

# Historico_4 rango_7
frame_histortico_4_rango_7 = Frame(marco_historico_4)
frame_histortico_4_rango_7.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_7.config(bg="gray59")

Label(frame_histortico_4_rango_7, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_7 = Label(frame_histortico_4_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_7.pack()

carton_salida_historico_4_rango_7 = Label(frame_histortico_4_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_7.pack(pady=1)

# Historico_4 rango_8
frame_histortico_4_rango_8 = Frame(marco_historico_4)
frame_histortico_4_rango_8.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_8.config(bg="#C0C0C0")

Label(frame_histortico_4_rango_8, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_8 = Label(frame_histortico_4_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_8.pack()

carton_salida_historico_4_rango_8 = Label(frame_histortico_4_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_8.pack(pady=1)

# Historico_4 rango_9
frame_histortico_4_rango_9 = Frame(marco_historico_4)
frame_histortico_4_rango_9.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_rango_9.config(bg="gray59")

Label(frame_histortico_4_rango_9, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_4_rango_9 = Label(frame_histortico_4_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_4_rango_9.pack()

carton_salida_historico_4_rango_9 = Label(frame_histortico_4_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_rango_9.pack(pady=1)

# Historico 4 Cierre
frame_histortico_4_cierre = Frame(marco_historico_4)
frame_histortico_4_cierre.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_4_cierre.config(bg="#31BFE4")

pico_historico_4_cierre = Label(frame_histortico_4_cierre, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"), width=1)
pico_historico_4_cierre.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_4_cierre, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_historico_4_cierre = Label(frame_histortico_4_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_historico_4_cierre.pack()

carton_salida_historico_4_cierre = Label(frame_histortico_4_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_4_cierre.pack(pady=1)

# historico 4 liquidacion

Frame_historico_4_Total = Frame(marco_historico_4)
Frame_historico_4_Total.pack(expand=True, fill= BOTH, side=LEFT)
Frame_historico_4_Total.config(bg="dodger blue")

Label(Frame_historico_4_Total, text = "SERIES",bg="dodger blue", font=("Times New Roman",13,"bold")).pack()
total_series_historico_4 = Label(Frame_historico_4_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",22,"bold"), width=4)
total_series_historico_4.pack()
Label(Frame_historico_4_Total, text = "CARTONES",bg="dodger blue", font=("Times New Roman",8,"bold")).pack()

total_cartones_historico_4 = Label(Frame_historico_4_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",15,"bold"), width=8)
total_cartones_historico_4.pack(pady=2)

# Medio 4
medio4 = Frame(root)
medio4.config(bg="white")
medio4.pack()
Label(medio4, text="",bg="#000099", font=("Times New Roman",2,"bold")).pack()

# Historico 5
marco_historico_5 = Frame(root)
marco_historico_5.pack(expand=True, fill= BOTH)
marco_historico_5.config(bg="lightblue")

# Historico_5 rango_1
frame_histortico_5_rango_1 = Frame(marco_historico_5)
frame_histortico_5_rango_1.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_1.config(bg="#31BFE4")

pico_salida_historico_5_rango_1 = Label(frame_histortico_5_rango_1, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"))
pico_salida_historico_5_rango_1.pack(side=RIGHT,anchor=NW, pady = 30)


Label(frame_histortico_5_rango_1, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_1 = Label(frame_histortico_5_rango_1, text = "0", bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_1.pack()

carton_salida_historico_5_rango_1 = Label(frame_histortico_5_rango_1, text = "0", background="white",foreground="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_1.pack(pady=1)

# Historico_5 rango_2
frame_histortico_5_rango_2 = Frame(marco_historico_5)
frame_histortico_5_rango_2.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_2.config(bg="#C0C0C0")

Label(frame_histortico_5_rango_2, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_2 = Label(frame_histortico_5_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_2.pack()

carton_salida_historico_5_rango_2 = Label(frame_histortico_5_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_2.pack(pady=1)

Label(frame_histortico_5_rango_2, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

# Historico 5 rango_3
frame_histortico_5_rango_3 = Frame(marco_historico_5)
frame_histortico_5_rango_3.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_3.config(bg="gray59")

Label(frame_histortico_5_rango_3, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_3 = Label(frame_histortico_5_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_3.pack()

carton_salida_historico_5_rango_3 = Label(frame_histortico_5_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_3.pack(pady=1)

# Historico 5 rango_4
frame_histortico_5_rango_4 = Frame(marco_historico_5)
frame_histortico_5_rango_4.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_4.config(bg="#C0C0C0")

Label(frame_histortico_5_rango_4, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_4 = Label(frame_histortico_5_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_4.pack()

carton_salida_historico_5_rango_4 = Label(frame_histortico_5_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_4.pack(pady=1)

# Historico 5 rango_5
frame_histortico_5_rango_5 = Frame(marco_historico_5)
frame_histortico_5_rango_5.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_5.config(bg="gray59")

Label(frame_histortico_5_rango_5, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_5 = Label(frame_histortico_5_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_5.pack()

carton_salida_historico_5_rango_5 = Label(frame_histortico_5_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_5.pack(pady=1)

# Historico 5 rango_6
frame_histortico_5_rango_6 = Frame(marco_historico_5)
frame_histortico_5_rango_6.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_6.config(bg="#C0C0C0")

Label(frame_histortico_5_rango_6, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_6 = Label(frame_histortico_5_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_6.pack()

carton_salida_historico_5_rango_6 = Label(frame_histortico_5_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_6.pack(pady=1)

# Historico_5 rango_7
frame_histortico_5_rango_7 = Frame(marco_historico_5)
frame_histortico_5_rango_7.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_7.config(bg="gray59")

Label(frame_histortico_5_rango_7, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_7 = Label(frame_histortico_5_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_7.pack()

carton_salida_historico_5_rango_7 = Label(frame_histortico_5_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_7.pack(pady=1)

# Historico_5 rango_8
frame_histortico_5_rango_8 = Frame(marco_historico_5)
frame_histortico_5_rango_8.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_8.config(bg="#C0C0C0")

Label(frame_histortico_5_rango_8, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_8 = Label(frame_histortico_5_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_8.pack()

carton_salida_historico_5_rango_8 = Label(frame_histortico_5_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_8.pack(pady=1)

# Historico_5 rango_9
frame_histortico_5_rango_9 = Frame(marco_historico_5)
frame_histortico_5_rango_9.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_rango_9.config(bg="gray59")

Label(frame_histortico_5_rango_9, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_5_rango_9 = Label(frame_histortico_5_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_5_rango_9.pack()

carton_salida_historico_5_rango_9 = Label(frame_histortico_5_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_rango_9.pack(pady=1)

# Historico 5 Cierre
frame_histortico_5_cierre = Frame(marco_historico_5)
frame_histortico_5_cierre.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_5_cierre.config(bg="#31BFE4")

pico_historico_5_cierre = Label(frame_histortico_5_cierre, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"), width=1)
pico_historico_5_cierre.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_5_cierre, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_historico_5_cierre = Label(frame_histortico_5_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_historico_5_cierre.pack()

carton_salida_historico_5_cierre = Label(frame_histortico_5_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_5_cierre.pack(pady=1)

# historico 5 liquidacion

Frame_historico_5_Total = Frame(marco_historico_5)
Frame_historico_5_Total.pack(expand=True, fill= BOTH, side=LEFT)
Frame_historico_5_Total.config(bg="dodger blue")

Label(Frame_historico_5_Total, text = "SERIES",bg="dodger blue", font=("Times New Roman",13,"bold")).pack()
total_series_historico_5 = Label(Frame_historico_5_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",22,"bold"), width=4)
total_series_historico_5.pack()
Label(Frame_historico_5_Total, text = "CARTONES",bg="dodger blue", font=("Times New Roman",8,"bold")).pack()

total_cartones_historico_5 = Label(Frame_historico_5_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",15,"bold"), width=8)
total_cartones_historico_5.pack(pady=2)

# Medio 5
medio5 = Frame(root)
medio5.config(bg="white")
medio5.pack()
Label(medio5, text="",bg="#000099", font=("Times New Roman",2,"bold")).pack()

# Historico 6
marco_historico_6 = Frame(root)
marco_historico_6.pack(expand=True, fill= BOTH)
marco_historico_6.config(bg="lightblue")

# Historico_6 rango_1
frame_histortico_6_rango_1 = Frame(marco_historico_6)
frame_histortico_6_rango_1.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_1.config(bg="#31BFE4")

pico_salida_historico_6_rango_1 = Label(frame_histortico_6_rango_1, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"))
pico_salida_historico_6_rango_1.pack(side=RIGHT,anchor=NW, pady = 30)


Label(frame_histortico_6_rango_1, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_1 = Label(frame_histortico_6_rango_1, text = "0", bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_1.pack()

carton_salida_historico_6_rango_1 = Label(frame_histortico_6_rango_1, text = "0", background="white",foreground="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_1.pack(pady=1)

# Historico_6 rango_2
frame_histortico_6_rango_2 = Frame(marco_historico_6)
frame_histortico_6_rango_2.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_2.config(bg="#C0C0C0")

Label(frame_histortico_6_rango_2, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_2 = Label(frame_histortico_6_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_2.pack()

carton_salida_historico_6_rango_2 = Label(frame_histortico_6_rango_2, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_2.pack(pady=1)

Label(frame_histortico_6_rango_2, text= "", bg="#C0C0C0", font=("Times New Roman",1),width=5).pack()

# Historico 6 rango_3
frame_histortico_6_rango_3 = Frame(marco_historico_6)
frame_histortico_6_rango_3.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_3.config(bg="gray59")

Label(frame_histortico_6_rango_3, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_3 = Label(frame_histortico_6_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_3.pack()

carton_salida_historico_6_rango_3 = Label(frame_histortico_6_rango_3, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_3.pack(pady=1)

# Historico 6 rango_4
frame_histortico_6_rango_4 = Frame(marco_historico_6)
frame_histortico_6_rango_4.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_4.config(bg="#C0C0C0")

Label(frame_histortico_6_rango_4, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_4 = Label(frame_histortico_6_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_4.pack()

carton_salida_historico_6_rango_4 = Label(frame_histortico_6_rango_4, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_4.pack(pady=1)

# Historico 6 rango_5
frame_histortico_6_rango_5 = Frame(marco_historico_6)
frame_histortico_6_rango_5.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_5.config(bg="gray59")

Label(frame_histortico_6_rango_5, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_5 = Label(frame_histortico_6_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_5.pack()

carton_salida_historico_6_rango_5 = Label(frame_histortico_6_rango_5, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_5.pack(pady=1)

# Historico 6 rango_6
frame_histortico_6_rango_6 = Frame(marco_historico_6)
frame_histortico_6_rango_6.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_6.config(bg="#C0C0C0")

Label(frame_histortico_6_rango_6, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_6 = Label(frame_histortico_6_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_6.pack()

carton_salida_historico_6_rango_6 = Label(frame_histortico_6_rango_6, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_6.pack(pady=1)

# Historico 6 rango_7
frame_histortico_6_rango_7 = Frame(marco_historico_6)
frame_histortico_6_rango_7.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_7.config(bg="gray59")

Label(frame_histortico_6_rango_7, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_7 = Label(frame_histortico_6_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_7.pack()

carton_salida_historico_6_rango_7 = Label(frame_histortico_6_rango_7, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_7.pack(pady=1)

# Historico 6 rango_8
frame_histortico_6_rango_8 = Frame(marco_historico_6)
frame_histortico_6_rango_8.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_8.config(bg="#C0C0C0")

Label(frame_histortico_6_rango_8, text = "SERIES",bg="#C0C0C0", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_8 = Label(frame_histortico_6_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_8.pack()

carton_salida_historico_6_rango_8 = Label(frame_histortico_6_rango_8, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_8.pack(pady=1)

# Historico 6 rango_9
frame_histortico_6_rango_9 = Frame(marco_historico_6)
frame_histortico_6_rango_9.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_rango_9.config(bg="gray59")

Label(frame_histortico_6_rango_9, text = "SERIES",bg="gray59", font=("Times New Roman",13,"bold")).pack()

series_histirico_6_rango_9 = Label(frame_histortico_6_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",22,"bold"), width=2)
series_histirico_6_rango_9.pack()

carton_salida_historico_6_rango_9 = Label(frame_histortico_6_rango_9, text = "0",bg="white",fg="blue",font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_rango_9.pack(pady=1)

# Historico 6 Cierre
frame_histortico_6_cierre = Frame(marco_historico_6)
frame_histortico_6_cierre.pack(expand=True, fill= BOTH, side=LEFT)
frame_histortico_6_cierre.config(bg="#31BFE4")

pico_historico_6_cierre = Label(frame_histortico_6_cierre, text = "0" ,fg="blue" ,bg="white", font=("Times New Roman",12,"bold"), width=1)
pico_historico_6_cierre.pack(side=RIGHT,anchor=NW, pady = 30)

Label(frame_histortico_6_cierre, text = "SERIES",bg="#31BFE4", font=("Times New Roman",13,"bold")).pack()

series_historico_6_cierre = Label(frame_histortico_6_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",22,"bold"), width=2)
series_historico_6_cierre.pack()

carton_salida_historico_6_cierre = Label(frame_histortico_6_cierre, text = "0",bg="white",fg="blue", font=("Times New Roman",18,"bold"), width=8)
carton_salida_historico_6_cierre.pack(pady=1)

# historico 6 liquidacion

Frame_historico_6_Total = Frame(marco_historico_6)
Frame_historico_6_Total.pack(expand=True, fill= BOTH, side=LEFT)
Frame_historico_6_Total.config(bg="dodger blue")

Label(Frame_historico_6_Total, text = "SERIES",bg="dodger blue", font=("Times New Roman",8,"bold")).pack()
total_series_historico_6 = Label(Frame_historico_6_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",22,"bold"), width=4)
total_series_historico_6.pack()
Label(Frame_historico_6_Total, text = "CARTONES",bg="dodger blue", font=("Times New Roman",8,"bold")).pack()

total_cartones_historico_6 = Label(Frame_historico_6_Total, text = "0",bg="white",fg ="blue", font=("Times New Roman",15,"bold"), width=8)
total_cartones_historico_6.pack(pady=2)

# Medio 6
medio6 = Frame(root)
medio6.config(bg="white")
medio6.pack()
Label(medio6, text="",bg="#000099", font=("Times New Roman",2,"bold")).pack()

# boton cierra ventana historico
boton_cerrar = Button(root, text="Cerrar", command=poner_al_frente_raiz, bg="Red", fg ="#F0F8FF", padx = 30, pady = 4, font=("Times New Roman", 14,"bold"),cursor="hand2", width=6, height=1)
boton_cerrar.pack(pady=5)#lambda: poner_al_frente(raiz)

cliente = establecer_conexion_con_servidor()

detener_hilo = threading.Event()
hilo_actualizacion = threading.Thread(target=comprueba_conexion, args=(cliente,))
hilo_actualizacion.daemon = True
hilo_actualizacion.start()

raiz.protocol("WM_DELETE_WINDOW", salir)

raiz.mainloop()
