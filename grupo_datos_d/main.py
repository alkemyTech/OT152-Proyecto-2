import logging.config
import os
import xml.etree.ElementTree as Et
from functools import reduce
from math import ceil

import task1
import task2
import task3

# Configure logger
LOGGING_CONF = os.path.join(os.path.dirname(__file__), 'logging.cfg')
logging.config.fileConfig(LOGGING_CONF)
logger = logging.getLogger("Grupo_de_datos_D")


def chunkify(data, number_of_chunks=4):
    """
    Divide current data into smaller chucks to process in parallel
    Base number of chunks is 4 (core * threads)
    :param data: list of entries
    :param number_of_chunks: parallel portions
    """
    chunk_size = ceil(len(data) / number_of_chunks)
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def mapreduce(task):
    """
    Apply map and reduce defined functions to data
    :param task: task to be executed
    :return: mapreduce result
    """
    mapped = map(task.mapper, data_chunks)
    return reduce(task.reducer, mapped)


def get_treeroot():
    """
    Get root of xml tree
    :return: xml tree root
    """
    # Get root folder
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Load specific xml requested
    try:
        file_xml = Et.parse(root_folder + '\\posts.xml')
    except Exception as E:
        logger.error(f"Error obtaining xml file in root path: {E}")
        exit()
    return file_xml.getroot()


if __name__ == '__main__':
    # Get xml root
    treeroot = get_treeroot()

    # Specify parallel execution instance number
    pool_size = 4

    # Chunkify data
    data_chunks = list(chunkify(treeroot, pool_size))

    # Task 1
    task1_ans = mapreduce(task1)
    logging.info(
        f"Top 10 tags de post sin respuestas aceptadas: {', '.join([x[0] for x in task1_ans.most_common(10)])}")

    # Task 2
    task2_ans = mapreduce(task2)
    logging.info(f"Relación entre cantidad de respuestas de un post y su puntaje: {'{:.3f}'.format(task2_ans[0])}")

    # Task 3
    task3_ans = mapreduce(task3)
    logging.info(
        f"Top 10 preguntas que tuvieron mayor tiempo de actividad: {', '.join([x[0] for x in task3_ans.most_common(10)])}")
