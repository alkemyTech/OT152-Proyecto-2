"""
Top 10 preguntas que tuvieron mayor tiempo de actividad
"""
from collections import Counter
from functools import reduce
from datetime import datetime


def parse_datetime(string):
    """
    Convert string to datetime
    :param string: String
    :return: Datetime
    """
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%f')


def get_activity_time(row):
    """
    Get the activity time of a question
    :param row: Row of data
    :return: Counter
    """
    creation_date = parse_datetime(row.attrib['CreationDate'])
    last_activity_date = parse_datetime(row.attrib['LastActivityDate'])
    delta = last_activity_date - creation_date
    question_id = row.attrib['Id']
    return Counter({question_id: int(delta.total_seconds())})


def reducer(data1, data2):
    """
    Reduce the counters into a single counter
    :param data1: Counter
    :param data2: Counter
    :return: Counter
    """
    data1 += data2
    return data1


def mapper(chunk):
    """
    Map tags and get their occurrence count
    :param chunk: List of rows
    :return: Counter
    """
    # Map tags into a list of tuples
    mapped = map(get_activity_time, chunk)
    filtered = filter(None, mapped)

    # Reduce the elements
    reduced = reduce(reducer, filtered)

    # Convert most_common into a counter again
    ans = Counter()
    dict.update(ans, reduced.most_common(10))

    return ans
