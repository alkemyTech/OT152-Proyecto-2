from functools import reduce
from typing import Counter
import xml.etree.ElementTree as ET
import re
import os

base = str(os.path.dirname(__file__)) + '/'
print(base)
tree = ET.parse(base + 'posts.xml')

root = tree.getroot()


def respuestas_aceptadas(data):
    try:
        salida = data.attrib['AcceptedAnswerId']
    except:
        return
    tag = data.attrib['Tags']
    tag = re.findall('<(.+?)>', tag)
    return tag, salida


def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


datos_cortados = chunkify(root, 10)
mapped = list(map(respuestas_aceptadas, root))
print(len(mapped))
mapped1 = list(filter(None, mapped))
print(len(mapped1))
