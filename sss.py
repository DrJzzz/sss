import hashlib
import os
import struct
from getpass4 import getpass
import random
from Cryptodome.Cipher import AES

primo = 208351617316091241234326746312124448251235562226470491514186331217050270460481

def encript(contraseña_usuario, nombre_arch, particiones, llaves, ruta_arch_encrip):
	
	contraseña_hash = hashlib.sha256(contraseña_usuario.encode())
	contra_hexa = contraseña_hash.hexdigest()
	contra_decimal = (int(contra_hexa, 16))
	
	# lista corresponde a los coeficientes del polinomio
	lista = []
	
	for i in range(llaves):
		coeficiente = random.randint(1, llaves)
		
		if(i == llaves-1):
			lista.append(contra_decimal)
			break
		lista.append(coeficiente)	
	
	# lista_evaluaciones son los valores en los que se evaluara el polinomio
	lista_evaluaciones = []
	
	while len(lista_evaluaciones) < particiones:
		evaluacion = random.randint(1, particiones + 50)
		if not evaluacion in lista_evaluaciones:
			lista_evaluaciones.append(evaluacion)	

	# lista_resultados son las parejas ordenadas en las que se dividio la contraseña encriptada
	lista_resultados = []
	resultado = 0

	for i in lista_evaluaciones:
		for j in range(len(lista)):
			resultado = resultado * i  + lista[j]
		
		resultado = resultado % primo
		
		lista_resultados.append((i, resultado))
		resultado = 0
	
	txt = open(nombre_arch + '.txt', "w")
	for i in range(len(lista_resultados)):
		txt.write(str(lista_resultados[i]) + os.linesep)
		
	key = contra_decimal.to_bytes(32, 'big')
	mode = AES.MODE_CBC
	IV = b'this is an IV456'
	
	def message(file):
		while len(file) % 16 != 0:
			file = file + b"0"
		return file

	cipher = AES.new(key, mode, IV)
	
	with open(ruta_arch_encrip, 'rb') as file:
		orig_file = file.read()
			
	padded_file = message(orig_file)
	
	encrypted_message = cipher.encrypt(padded_file)
	
	with open(nombre_arch + '.aes', 'wb') as e:
		e.write(encrypted_message)


def interpolacion(arch_encrip, nombre_des):

	print("Para dejar de ingresar valores ingrese el valor 0 en la coordenada 1")
	lista = []
	x = int(input("coordenada 1: "))
	y = int(input("coordenada 2: "))
	while(True):
		lista.append((x,y))
		x = int(input("coordenada 1: "))
		y = int(input("coordenada 2: "))
		if(x == 0):
			break
	
	lista_terminos = []
	lista_imagenes = []
	
	for c, d in lista:
		
		numerador = 1
		denominador = 1
		
		for a, b in lista:
			
			if(a != c):
				numerador *= -a % primo
				denominador *= (c-a) 
			
		inverso = pow(denominador, primo-2, primo)
	
		z = (numerador * inverso)	
		lista_terminos.append(z)
		
	for a, b in lista:
		lista_imagenes.append(b)
	
	clave = 0
	
	for i in range(len(lista_terminos)):
		clave += (lista_terminos[i] * lista_imagenes[i])
	
	clave = clave % primo
	
	key = clave.to_bytes(32, 'big')
	mode = AES.MODE_CBC
	IV = b'this is an IV456'

	cipher = AES.new(key, mode, IV)
	
	with open(arch_encrip, 'rb') as e:
		encrypted_file = e.read()
	
	
	decrypted_file = cipher.decrypt(encrypted_file)

	with open(nombre_des, 'wb') as df:
		df.write(decrypted_file.rstrip(b'0'))
		
def main():
	print("seleccione un modo: 'c' para codificar, 'd' para decodificar")
	Modo = input()
	if(Modo == 'c'):
		print("Ingrese la ruta del archivo a enciptar: ")
		ruta_arch_encrip = str(input())
		contraseña_usuario = getpass("ingrese una contraseña: ")
		print("ingrese el nombre del archivo encriptado y el archivo .txt: ")
		nombre_arch = str(input()) 
		print("ingrese la cantidad en la que la contraseña sera dividida: ")
		particiones = int(input())
		print("¿Cuantas partes de la contraseña dividida seran necesarias para decifrar el archivo? ")
		llaves = int(input())
		
		encript(contraseña_usuario, nombre_arch, particiones, llaves, ruta_arch_encrip)
		
	if(Modo == 'd'):
		print("ingrese la ruta del archivo encriptado: ")
		arch_encrip = str(input())
		print("Nombre del archivo descencriptado: ")
		nombre_des = str(input())
		
		interpolacion(arch_encrip, nombre_des)
		
main()
	



































		

