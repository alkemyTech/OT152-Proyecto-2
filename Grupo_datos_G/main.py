import logging
import logging.config
import defusedxml.ElementTree as Et
import re
import time

from decouple import config as cfg
from functools import reduce
from typing import Counter


# Load logging configurations
logging.config.fileConfig(cfg('FILE_PATH'))
# Instansiate logger class
logger = logging.getLogger('Grupo_Datos_G')

# top 10 posts mas vistos

tree = Et.parse('posts.xml')

root = tree.getroot()


def obtener_tags_y_palabras(data):
    try:
        tags = data.attrib['Tags']
    except KeyError:
        return
    view_count = data.attrib['ViewCount']
    tags = re.findall('<(.+?)>', tags)
    # separo los numeros de viewcount de las tags
    numeros = [int(numeros) for numeros in re.findall(r'-?\d+\.?\d*',
                                                      view_count)]
    return numeros


def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


data_chunks = chunkify(root, 50)

mapped = list(map(obtener_tags_y_palabras, root))
mapped2 = list(filter(None, mapped))
mapped3 = sorted(mapped2, reverse=True)

# Muestro el resultado del top 10 posts mas vistos

top_10 = mapped3[0:10]
print(top_10)


# Top 10 palabras mas nombradas por tag

def obtener_tags_y_palabras(data):
    try:
        tags = data.attrib['Tags']
    except KeyError:
        return
    tags = re.findall('<(.+?)>', tags)
    body = data.attrib['Body']
    body = re.findall('(?<!\\S)[A-Za-z]+(?!\\S)|(?<!\\S)[A-Za-z]+(?=:(?!\\S))',
                      body)
    counter_palabras = Counter(body)
    return tags, counter_palabras


def separar_tags_y_palabras(data):
    return dict([[tags, data[1].copy()] for tags in data[0]])


def reducir_contadores(data1, data2):
    for key, value in data2.items():
        if key in data1.keys():
            data1[key].update(data2[key])
        else:
            data1.update({key: value})
    return data1


def mapper(data):
    palabras_mapeadas = list(map(obtener_tags_y_palabras, data))
    palabras_mapeadas = list(filter(None, palabras_mapeadas))
    palabras_por_tag = list(map(separar_tags_y_palabras, palabras_mapeadas))
    try:
        reducido = reduce(reducir_contadores, palabras_por_tag)
    except TypeError:
        return
    return reducido


def calculate_top_10(data):
    return data[0], data[1].most_common(10)


data_chunks = chunkify(root, 50)
mapped = list(map(mapper, data_chunks))
mapped = list(filter(None, mapped))
reduced = reduce(reducir_contadores, mapped)
top_10 = dict(map(calculate_top_10, reduced.items()))
print(reduced)

# Tiempo de respuesta promedio en top 200-300 score

inicio = time.time()


def separar_numeros_de_tags(data):
    try:
        tags = data.attrib['Tags']
    except KeyError:
        return
    score = data.attrib['Score']
    tags = re.findall('<(.+?)>', tags)
    # separo los numeros de score de las tags
    numeros = [int(numeros) for numeros in re.findall(r'-?\d+\.?\d*', score)]
    return numeros


data_chunks = chunkify(root, 50)

mapped = list(map(separar_numeros_de_tags, root))
mapped2 = list(filter(None, mapped))

# Calculo el top 200 score
top_200 = mapped2[0:200]
print(top_200)

# Calculo el top 300 score
top_300 = mapped2[0:300]
print(top_300)

fin = time.time()

# Tiempo transcurrido para calcular el top 200 y 300 de score
print("El tiempo de respuesta promedio es: " + str(fin-inicio))
