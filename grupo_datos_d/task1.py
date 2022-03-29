"""
Top 10 tags de post sin respuestas aceptadas
"""
from collections import Counter
from functools import reduce
import re


def get_tags(data):
    """
    Obtain tag names and empty invalid entries
    :param data: Row object
    :return:
    """
    if "Tags" not in data.attrib or "AnswerCount" in data.attrib:
        return
    tags = data.attrib['Tags']
    tags = re.findall('<(.+?)>', tags)
    return Counter(tags)


def reducer(counter_tracker, new_tags):
    """
    Merge tags into the occurrence counter
    :param counter_tracker: Counter
    :param new_tags: Counter
    :return: Counter
    """
    counter_tracker += new_tags
    return counter_tracker


def mapper(chunk):
    """
    Map tags and get their occurrence count
    :param chunk: List of rows
    :return: Counter
    """
    # Map tags into a list of tuples
    mapped = map(get_tags, chunk)
    filtered = filter(None, mapped)

    # Reduce the elements
    ans = reduce(reducer, filtered)
    return ans
