import logging.config
import re
from collections import Counter
from datetime import datetime
from functools import reduce

import defusedxml.ElementTree as Etree

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("main")
logger.info("start")


def chunkify(iterable, len_chunk):
    for i in range(0, len(iterable), len_chunk):
        yield iterable[i:i + len_chunk]


# Get the tags for the task1
def get_tags(data):
    try:
        data.attrib['AcceptedAnswerId']
    except KeyError:
        return
    tags = data.attrib['Tags']
    tags = re.findall('<(.+?)>', tags)
    tag_counter = Counter(tags)
    return tags, tag_counter


# Get the scores for the task 2
def get_scores(data):
    try:
        word = data.attrib['Body']
    except KeyError:
        return
    word = re.findall("<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>",
                      word)
    score = data.attrib['Score']
    # I transform de variable score into int to find its relationship
    score = int(score)
    word_counter = Counter(word)
    word_counter = sum(word_counter.values())
    return score, word_counter


def get_dates(data):
    try:
        creation = data.attrib['CreationDate']
    except KeyError:
        return
    last = data.attrib['LastActivityDate']
    creation = creation.replace("T", " ")
    last = last.replace("T", " ")
    creation = datetime.strptime(creation, "%Y-%m-%d %H:%M:%S.%f")
    last = datetime.strptime(last, "%Y-%m-%d %H:%M:%S.%f")
    res = abs((creation-last).days)
    return res


def suma_total(data):
    data = [[a/2 for a in dates if a] for dates in data]
    data = [sum(i) for i in zip(*data)]
    return sum(data)


def separate(data):
    return dict([tag, data[1].copy()] for tag in data[0])


def count_reduce(data1, data2):
    for key, value in data2.items():
        if key in data1.keys():
            data1[key].update(data2[key])
        else:
            data1.update({key: value})
    return data1


def reducer(mapped_list):
    return [[a / b for a, b in data if b] for data in mapped_list]


def top_ten(data):
    return data[0], data[1].most_common


# I named this function as mapper 1 because it belongs to the first task
def mapper_1(data):
    mapped_tags = list(map(get_tags, data))
    mapped_tags = list(filter(None, mapped_tags))
    separated_tags = list(map(separate, mapped_tags))
    try:
        reduced_tags = reduce(count_reduce, separated_tags)
    except BaseException:
        return
    return reduced_tags


# I named this function as mapper 2 because it belongs to the second task
def mapper_2(data):
    mapped_scores = list(map(get_scores, data))
    mapped_scores = list(filter(None, mapped_scores))
    return mapped_scores


def mapper_dates(data):
    mapped_dates = list(map(get_dates, data))
    return mapped_dates


xml_posts = Etree.parse('posts.xml')
root = xml_posts.getroot()

# ______________Calling the function for the first task______________________
data_chunk = chunkify(root, 50)
mapped_1 = list(map(mapper_1, data_chunk))
mapped_1 = list(filter(None, mapped_1))
reduced1 = reduce(count_reduce, mapped_1)
top_10 = dict(map(top_ten, reduced1.items()))
top = list(reduced1.items())[:10]
try:
    logging.info('Top ten tags with most accepted answers:\n{}\n'.format(top))
except AttributeError:
    logging.warning('NoneType not admitted')

# ________________________Calling the functions for the second task__________

data_chunk_2 = chunkify(root, 50)
mapped2 = list(map(mapper_2, data_chunk_2))
mapped = list(filter(None, mapped2))
relationship = reducer(mapped)
reduced_2 = reduce(reducer, relationship[0:1])
try:
    logging.info(f'\n\nA random post and its relationship between\
                the score and number of words is: {reduced_2[0:1]}')
except TypeError:
    logging.warning("The value must be integer or float")
# ____________________Calling functions for the third task _______________

data_chunk3 = chunkify(root, 50)
mapped_3 = list(map(mapper_dates, data_chunk3))
tiempo = suma_total(mapped_3)
reduced = reduce(lambda count, l: count + len(l), mapped_3, 0)
average_t = tiempo/reduced
try:
    logging.info(f'\n\nThe average time for a post to get an answer\
                 is: \n {average_t}')
except TypeError:
    logging.warning("This is not a number to show ")
