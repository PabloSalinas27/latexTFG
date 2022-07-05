from ast import arg
import numpy as np


def followPathAndCheck(element, filtrador, prop=['result', 'uplink_message', 'f_port']) -> bool:
    """ 
    Baja por los tags de "prop" y devuelve si el último elemento de la cadena es "port" 
    Por defecto está hecho para que busque por los puertos, pero es configurable si se 
    introduce "prop"
    """
    it = element
    for value in prop:
        try:
            it = it.get(value)
        except:
            return False

    if filtrador == None:
        return True
    else:
        return it == filtrador


def cadenaDeBien(prop, filtrador):
    """Wrapper of followPathAndCheck to be able to use it as a filter. 
    Input: a list of properties that should be in the packet with a final
    value the final property should have.
    Return: a boolean function classifing between packets with the correct final
    value. Should be used with functions like filter() """
    def a(element):
        return followPathAndCheck(element, prop=prop, filtrador=filtrador)
    return a


def media(array, toFilter=None, byFilter=None):
    """ Hace una media de un diccionario de arrays. Tiene opcion de filtrar la lista
    si se le pasa un array a toFilter con el arbol que tiene que tener 
    el paquete y a toFilter lo que tiene que ser ese item"""
    array = list(filter(followPathAndCheck(
        port=byFilter, prop=toFilter), array))
    medias = {}
    for key, value in array.items():
        medias[key] = np.mean(array[key])
    return medias

    # tmp['powRet'] = (elem['uplink_message']['decoded_payload']['pow'])


def keepKeys(array, valores=["SF", "powRet", "snr"]):
    res = []
    for key, value in array.items():
        tmp = {}
        for keep in valores:
            if key == keep:
                tmp[keep] = value
        res.append(tmp)
    return res
