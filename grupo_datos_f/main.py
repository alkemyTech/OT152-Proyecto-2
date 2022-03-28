import logging.config
from decouple import config as cfg
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import Counter
from functools import reduce

# Loading logging configuration file
logging.config.fileConfig(cfg('LOG_PATH'))

# Create Logger
logger = logging.getLogger('Grupo_Datos_F')

def chunkify(iterable, len_of_chunk):
    '''
    Split an iterable into evenly sized Chunks
    '''
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def get_dates(data):
    '''
    Get the posts creation date and create a date object from a string
    '''
    date_str = data.attrib['CreationDate']
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").date()
    return dt

def mapper(data):
    '''
    Apply "mapper" functions
    '''
    mapped_dates = list(map(get_dates, data))
    return mapped_dates

def reduce_counter(data1, data2):
    '''
    Join data
    '''
    data1.update(data2)
    return data1

def calculate_top_10_less(data):
    top_10 = dict(data.most_common()[-10:])
    top_10 = list(top_10.keys())
    return top_10

# Parse the file with posts data
tree = ET.parse('posts.xml')
root = tree.getroot()
# Create chunks
data_chunks = chunkify(root, 20)

def top_10_dates_less_post():
    # Apply mapper and reducer functions
    mapped = list(map(mapper, data_chunks))
    mapped = list(map(Counter, mapped))
    reduced = reduce(reduce_counter, mapped)
    # Get and show top 10 dates with less posts
    top_10_dates = calculate_top_10_less(reduced)
    print('Top 10 date with less posts:')
    for i in range(len(top_10_dates)):
        print(' - ', top_10_dates[i])
    logging.info(' Top 10 dates with less posts - Downloaded')
    return

# Run main code
if __name__ == '__main__':
    top_10_dates_less_post()
