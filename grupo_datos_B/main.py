from functools import reduce
from typing import Counter
import xml.etree.ElementTree as ET
import re
import os

base = str(os.path.dirname(__file__)) + '/'
print(base)
tree = ET.parse(base + 'posts.xml')

root = tree.getroot()


def respuestas_sin_respuesta(data):
    try:
        salida = data.attrib['AcceptedAnswerId']
    except:
        return
    tag = data.attrib['Tags']
    tag = re.findall('<(.+?)>', tag)
    counter_tag = Counter(tag)
    return counter_tag


def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


def reducir_contadores(data1, data2):
    for key, value in data2.items():
        if key in data1.keys():
            data1[key].update(data2[key])
        else:
            data1.update({key: value})
    return data1

def separar_tags(data):
    for key in data.items():
        return dict([(key[0], key[1])])
    # return dict([(tag[0], tag[1]) for tag in data.items()])

datos_cortados = chunkify(root, 10)
mapped = list(map(respuestas_sin_respuesta, root))
mapped1 = list(filter(None, mapped))
tag_palabra= list(map(separar_tags, mapped1))
reducido = reduce(reducir_contadores, tag_palabra)
