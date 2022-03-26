from functools import reduce
from typing import Counter
import xml.etree.ElementTree as ET
import re
import os


def post_sin_respuesta(data):
    try:
        data.attrib['AcceptedAnswerId']
    except Exception:
        return
    tag = data.attrib['Tags']
    tag = re.findall('<(.+?)>', tag)
    counter_tag = Counter(tag)
    return counter_tag


def reducir_contadores(data1, data2):
    for key, value in data2.items():
        if key in data1.keys():
            data1.update({key: data2[key]})
        else:
            data1.update({key: value})
    return data1


def separar_tags(data):
    return dict([[key, data[1].copy] for key in data[0]])


def obtener_id_y_palabras(data):
    try:
        tags = data.attrib['Id']
    except Exception:
        return
    # tags = re.findall('<(.+?)>', tags)
    body = data.attrib['Body']
    body = re.findall('(?<!\S)[A-Za-z]+(?!\S)|(?<!\S)[A-Za-z]+(?=:(?!\S))', body)
    visitas = int(data.attrib['ViewCount'])
    counter_palabras = len(body)
    if visitas == 0:
        relacion = 0
    else:
        relacion = round(counter_palabras / visitas, 2)
    # counter_palabras = Counter(body)
    return tags, relacion


def get_repuestas_favoritas(data):
    tipo_tags = data.attrib['PostTypeId']
    if tipo_tags == '2':
        try:
            cant_favoritos = data.attrib['FavoriteCount']
        except Exception:
            cant_favoritos = 0
    else:
        return
    tags = data.attrib['Id']
    return tags, cant_favoritos


def get_10_sin_repuestas():
    base = str(os.path.dirname(__file__)) + '/'
    tree = ET.parse(base + 'posts.xml')
    root = tree.getroot()
    mapped = list(map(post_sin_respuesta, root))
    mapped = list(filter(None, mapped))
    reducido = reduce(reducir_contadores, mapped)
    return reducido.most_common(10)


def palabra_vs_visita():
    base = str(os.path.dirname(__file__)) + '/'
    tree = ET.parse(base + 'posts.xml')
    root = tree.getroot()
    mapped = list(map(obtener_id_y_palabras, root))
    palabras_tags = list(filter(None, mapped))
    return palabras_tags


def promedio_score():
    base = str(os.path.dirname(__file__)) + '/'
    tree = ET.parse(base + 'posts.xml')
    root = tree.getroot()
    mapped = list(map(get_repuestas_favoritas, root))
    mapped = list(filter(None, mapped))
    return mapped


top_10 = get_10_sin_repuestas()
relacion_palabra_visita = palabra_vs_visita()
print(top_10)
print(relacion_palabra_visita)
test = promedio_score()
print(test)
