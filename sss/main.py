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
