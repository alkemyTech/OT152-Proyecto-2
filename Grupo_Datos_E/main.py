from datetime import datetime
from functools import reduce
from collections import Counter
import xml.etree.ElementTree as Et


def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


# Top 10 fechas con mayor cantidad de post creados


def obtener_fechas(data):
    creation_date = data.attrib['CreationDate']
    creation_date = datetime.strptime(creation_date,
                                      '%Y-%m-%dT%H:%M:%S.%f').date()
    return creation_date


def mapper(data):
    post_mapeados = list(map(obtener_fechas, data))
    return post_mapeados


def reducir_counter(data1, data2):
    data1.update(data2)
    return data1


tree = Et.parse(r'/Users/joelsolaligue/Desktop/Joel/ALKEMY/big_data/OT152-Proyecto-2/Grupo_Datos_E/posts.xml')
root = tree.getroot()

data_chunks = chunkify(root, 50)
mapped = list(map(mapper, data_chunks))
mapped = list(map(Counter, mapped))
reduced = reduce(reducir_counter, mapped)
top_ten_post = reduced.most_common(10)

#print("\nTop 10 fechas con mayor cantidad de post creados\n", top_ten_post)

# Relacion entre cantidad de respuestas y visitas


def respuestas_visitas(data):
    try:
        answer_count = data.attrib['AnswerCount']
    except Exception:
        return
    view_count = data.attrib['ViewCount']
    view_count = int(view_count)
    answer_count = int(answer_count)

    return {answer_count: view_count}


def reducir_counter(data1, data2):
    data1.update(data2)
    return data1


# def reducir_contadores(data1, data2):
#     for key, value in data2.items():
#         if key in data1.keys():
#             data1[key].update(data2[key])
#         else:
#             data1.update({key: value})
#     return data1


def mapper_answer_view(data):
    post_mapeados = list(map(respuestas_visitas, data))
    post_mapeados = list(filter(None, post_mapeados))
    try:
        reducido = reduce(reducir_counter, post_mapeados)
    except Exception:
        return
    return reducido


data_chunks = chunkify(root, 50)
mapped_answer_view = list(map(mapper_answer_view, data_chunks))
mapped_answer_view = list(filter(None, mapped_answer_view))
#print(mapped_answer_view)
reduced = reduce(reducir_counter, mapped_answer_view)

key_1, value_2 = reduced.keys(), reduced.values()
sum_keys, sum_value = sum(key_1), sum(value_2)

total = {sum_keys/sum_value}

print(total)
