from random import randint
from lagrange import interpolate
import doctest
from getpass4 import getpass

username= "estudiante";
password= "1234";

def share(value, parties, prime, coefficients = None):
    """
    Convierte un número entero en un número de compartidos dado un módulo y un
    numero de parties (mo sé cómo pordía traducir al español)
    """
    shares = {}
    threshold = parties - 1
    if coefficients is None:
        # coeficientes aleatorios polinomiales
        polynomial = [value] + [randint(0,prime-1) for _ in range(1,threshold)]
    else:
        polynomial = [value] + coefficients

    # computa cada compartido[i] = f(i).
    for i in range(1, parties+1):
        shares[i] = polynomial[0]
        for j in range(1, len(polynomial)):
            shares[i] = (shares[i] + polynomial[j] * pow(i,j)) % prime

    return shares


def build(shares, prime):
    
    return interpolate(shares, prime)

def main():
    user= input("hi, please enter your username: ");
    if user != username:
        print("Try again")
    else:
        pswd= getpass("Enter your password: ")
        if pswd == password:
            print("Hello, please enter the option that you want: ")
            print("c: Encode")
            print("d: Decode")
        else:
            print("Incorrect Password")
        

    func = input()

    if func == 'c':
        print("Enter Source Image Path")
        src = input()
        print("Enter Message to Hide")
        message = input()
        print("Enter Destination Image Path")
        dest = input()
        print("Encoding...")
        Encode(src, message, dest)

    elif func == 'd':
    
        print("Enter Source Image Path")
        src = input()
        print("Decoding...")
        Decode(src)

    else:
        print("ERROR: Invalid option chosen")
        
