import logging.config
from decouple import config as cfg
import xml.etree.ElementTree as ET
from datetime import datetime, date
from collections import Counter
from functools import reduce

# Loading logging configuration file
logging.config.fileConfig(cfg('LOG_PATH'))

# Create Logger
logger = logging.getLogger('Grupo_Datos_F')

def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def get_dates(data):
    date_str = data.attrib['CreationDate']
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").date()
    return dt

def mapper(data):
    mapped_dates = list(map(get_dates, data))
    return mapped_dates

def reducir_counter(data1, data2):
    data1.update(data2)
    return data1

tree = ET.parse('posts.xml')
root = tree.getroot()
data_chunks = chunkify(root, 20)
mapped = list(map(mapper, data_chunks))    # ej: datetime.date(2010, 10, 31)
mapped = list(map(Counter, mapped))    # ej: lista de Counter({datetime.date(2010, 10, 31) : 20})...
reducido = reduce(reducir_counter, mapped)
top_10_dates_less_post = reducido.most_common()[-10:]
logging.INFO('Descargados el Top 10 de fechas con menor cantidad de post creados')