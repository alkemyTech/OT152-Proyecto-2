import logging
import logging.config

from datetime import datetime
from functools import reduce
from collections import Counter
import xml.etree.ElementTree as Et


logging.config.fileConfig('logging.cfg')

logger = logging.getLogger('log_datos_e')


def get_xml():
    """Read the xml file in te project
    Ags: 
        None           
    Return:
        xml file
    """
    try:
        tree = Et.parse('posts.xml')
    except IOError as e:
        logger.error(
            f'Error al leer el archivo xml, no se lo ha encontrado: {e}')
        raise Exception('No se encontro el archivo xml')
    return tree


def chunkify(data, len_of_chunk):
    """Produces a cut in the data in sections
    Args:
        data: data xml
        len_of_chunk: amount of CPU, core * threads
    Return:
        Yield generator
    """
    for i in range(0, len(data), len_of_chunk):
        yield data[i:i + len_of_chunk]


# Top 10 fechas con mayor cantidad de post creados
def get_date(data):
    """Get CreationDate from xml file
    Args:
        data: stretch of data

    Return:
        Creationdate attribute
    """
    creation_date = data.attrib['CreationDate']
    creation_date = datetime.strptime(creation_date,
                                      '%Y-%m-%dT%H:%M:%S.%f').date()
    return creation_date


def mapper(data):
    """Map the data
    Ars:
        data: stretch of data
    Return:
        Mapped posts
    """
    post_mapeados = list(map(get_date, data))
    return post_mapeados


def reduce_counter(data1, data2):
    """Reduce counter
    Ars:
        data1: First value
        data2: Second value
    Return:
        Select the first two elements, return result
    """
    data1.update(data2)
    return data1


# Relacion entre cantidad de respuestas y visitas
def answers_views(data):
    """Get the attributes
    Ars:
        data: stretch of data
    Return:
        Attributes AnswerCount, ViewCount
    """
    try:
        answer_count = data.attrib['AnswerCount']
    except Exception:
        return
    view_count = data.attrib['ViewCount']
    view_count = int(view_count)
    answer_count = int(answer_count)

    return {answer_count: view_count}


def mapper_answer_view(data):
    """Map the data
    Ars:
        data: stretch of data
    Return:
        Mapped results
    """
    post_mapeados = list(map(answers_views, data))
    post_mapeados = list(filter(None, post_mapeados))
    try:
        reducido = reduce(reduce_counter, post_mapeados)
    except Exception:
        return
    return reducido


# Tiempo de respuesta primedio en top 0-100 post con mayor puntaje
def find_score(data):
    """Get attributes
    Args:
        data: stretch of data
    Return:
        score attribute
    """
    score = data.attrib['Score']
    return score


def response_time_average(data):
    """
    """
    creation_date = data.attrib['CreationDate']
    creation_date = datetime.strptime(creation_date,
                                      '%Y-%m-%dT%H:%M:%S.%f').date()
    last_date = data.attrib['LastActivityDate']
    last_date = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S.%f').date()
    promedio = last_date - creation_date
    return promedio


def mapper_score(data):
    """Average response time on top 0-100 post with the highest score
    Ars:
        data: stretch of data
    Return:
        Mapped data
    """
    score = list(map(find_score, data))
    promedio = list(map(response_time_average, data))
    return promedio, score


if __name__ == '__main__':
    # First task
    # Top 10 fechas con mayor cantidad de post creados
    tree = get_xml()
    root = tree.getroot()
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper, data_chunks))
    mapped = list(map(Counter, mapped))
    reduced = reduce(reduce_counter, mapped)
    top_ten_post = reduced.most_common(10)

    logger.info(
        f'Top 10 fechas con mayor cantidad de post creados\n {top_ten_post}\n'
        )

    # Second task
    # Relacion entre cantidad de respuestas y visitas
    data_chunks = chunkify(root, 50)
    mapped_answer_view = list(map(mapper_answer_view, data_chunks))
    mapped_answer_view = list(filter(None, mapped_answer_view))
    reduced = reduce(reduce_counter, mapped_answer_view)

    key_1, value_2 = reduced.keys(), reduced.values()
    sum_keys, sum_value = sum(key_1), sum(value_2)

    total = sum_keys/sum_value
    logger.info(
        f'\nRelacion entre cantidad de respuestas y sus visitas:{total:.2f}%\n'
        )

    # Third task
    # Tiempo de respuesta primedio en top 0-100 post con mayor puntajes
    data_chunks = chunkify(root, 100)
    mapped_score = list(map(mapper_score, data_chunks))
    top_0_100_respuesta_promedio = mapped_score[0][0:100]
    top_0_100_respuestas_promedio = dict(
        zip(top_0_100_respuesta_promedio[0], top_0_100_respuesta_promedio[1]))
    max_key = max(top_0_100_respuestas_promedio,
                  key=top_0_100_respuestas_promedio.get)
    logger.info(
        f'\nTiempo de respuesta promedio en top 0-100: {max_key}\n')
