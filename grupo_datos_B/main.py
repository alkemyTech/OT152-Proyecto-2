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


def get_10_sin_repuestas():
    base = str(os.path.dirname(__file__)) + '/'
    tree = ET.parse(base + 'posts.xml')
    root = tree.getroot()
    mapped = list(map(post_sin_respuesta, root))
    mapped = list(filter(None, mapped))
    reducido = reduce(reducir_contadores, mapped)
    return reducido.most_common(10)


top_10 = get_10_sin_repuestas()
print(top_10)
