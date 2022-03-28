import logging.config
from decouple import config as cfg
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import Counter
from functools import reduce
import re

# Loading logging configuration file
logging.config.fileConfig(cfg('LOG_PATH'))

# Create Logger
logger = logging.getLogger('Grupo_Datos_F')

# --- General functions --- 
def chunkify(iterable, len_of_chunk):
    '''
    Split an iterable into evenly sized Chunks
    '''
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def parse_xml():
    '''
    Parse the file 'posts.xml', which contain posts data
    '''
    tree = ET.parse('posts.xml')
    return tree.getroot()

def reduce_counter(data1, data2):
    '''
    Join data between Counter objects
    '''
    data1.update(data2)
    return data1

# --- Top 10 dates with less posts --- 
def get_dates(data):
    '''
    Get the posts creation date and create a date object from a string
    '''
    date_str = data.attrib['CreationDate']
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").date()
    return dt

def mapper(data):
    '''
    Apply "mapper" functions to get the posts dates
    '''
    mapped_dates = list(map(get_dates, data))
    return mapped_dates

def calculate_top_10_less(data):
    '''
    Select only the top 10 most used words
    '''
    top_10 = dict(data.most_common()[-10:])
    top_10 = list(top_10.keys())
    return top_10

# --- Top 10 most used words in posts --- 
def words_counter(data):
    '''
    Count, and collect, the number of words in each post 
    '''
    body = data.attrib['Body']
    body = re.findall('(?<!\S)[A-Za-z]+(?!\S)|(?<!\S)[A-Za-z]+(?=:(?!\S))',body)
    words = Counter(body)
    return words

def mapper_words(data):
    '''
    Apply "mapper" functions to get the most used words in posts
    '''
    mapped_words = list(map(words_counter, data))
    reduced = reduce(reduce_counter, mapped_words)
    return reduced


# --- Tasks to resolve --- 
def top_10_dates_less_post():
    root = parse_xml()
    data_chunks = chunkify(root, 20)
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

def top_10_words():
    root = parse_xml()
    data_chunks = chunkify(root, 20)
    mapped_words = list(map(mapper_words, data_chunks))
    reduced_words = reduce(reduce_counter, mapped_words)
    print('\nTop 10 most used words in posts:')
    print(reduced_words.most_common(10))
    logging.info(' Top 10 most used words in posts - Downloaded')
    return


# Run main code
if __name__ == '__main__':
    top_10_dates_less_post()
    top_10_words()
