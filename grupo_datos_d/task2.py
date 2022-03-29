"""
Relación entre cantidad de respuestas de un post y su puntaje.
"""
from functools import reduce


def get_relations(post):
    """
    Get relations between the post and the answers.
    :param post: Row
    :return: tuple containing relation and weight
    """
    if "AnswerCount" not in post.attrib or "Score" not in post.attrib or int(post.attrib["Score"]) == 0:
        return
    return int(post.attrib["AnswerCount"]) / int(post.attrib["Score"]), 1


def reducer(data1, data2):
    """
    Get ponderated average of the relations.
    data[0] = value
    data[1] = weight
    :param data1: Tuple
    :param data2: Tuple
    :return:
    """
    weights = data1[1] + data2[1]
    return (data1[0] * data1[1] + data2[0] * data2[1]) / weights, weights


def mapper(chunk):
    """
    Map relations between the post and the answers and get their pondered average.
    :param chunk: List of rows
    :return: Tuple
    """
    mapped = map(get_relations, chunk)
    filtered = filter(None, mapped)

    ans = reduce(reducer, filtered)
    return ans
