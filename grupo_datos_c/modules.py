from collections import Counter
import re


# Functions for top 10 tags ------------------------------------
def get_tags_and_ansid(data_chunk):
    """
    Returns two lists with all tags and accepdet answer id.

        Parameters:
                data_chunk (list): c with the data chunk to process
        Returns:
                tags, acc_ans_id (lists): lists containing data requested
    """
    tags = []
    acc_ans_id = []
    for data in data_chunk:
        tags.append(data.attrib.get('Tags'))
        acc_ans_id.append(data.attrib.get('AcceptedAnswerId'))

    return tags, acc_ans_id


def get_tags_with_acc_answ(data):
    """
    Returns a list with tags that only have accepted answer id

        Parameter:
                data (list): Contains two lists with tags and accepted answer id
        Returns:
                tags_with_acc_ans (list): with only tags that have accepted answer id
    """
    tags_with_acc_ans = []
    data = zip(data[0], data[1])

    for tags, ans_id in data:
        if ans_id is not None:
            tags_with_acc_ans.append(tags)

    return tags_with_acc_ans


def split_and_count_tags(tags):
    """
    Returns a list with Counter object with dictionares counting all tags per chunk of data

            Parameter tags (list):
                    Contains tags with accepted answer id
            Returns:
                    counter (list): with all Counter objects

    """
    # Create Counter object
    counter = Counter()

    # Dictionary to replace unnecesary special characters
    char_replacement = {'<': ' ', '>': ' '}

    for tag_string in tags:
        for key, value in char_replacement.items():
            tag_string = tag_string.replace(key, value)
        counter.update(Counter(tag_string.split()))

    return counter


# Functions for word/answercount ratio--------------------
def get_bodies_and_answer_counts(data_chunk):
    """
    Returns three lists with id, bodie of post and awnser count

            Parameters:
                    data_chunk (list): Generator objetc with the data chunk to process
            Returns:
                    post_id, bodies, answer_counts(lists): lists containing data requested
    """
    post_id = []
    bodies = []
    answer_counts = []

    for data in data_chunk:
        post_id.append(data.attrib.get('Id'))
        bodies.append(data.attrib.get('Body'))
        answer_counts.append(data.attrib.get('AnswerCount'))

    return post_id, bodies, answer_counts


def bodies_with_answer_count(data):
    """
    Returns id, body and answer count, if answer count is not None or 0

            Parameter:
                    data (list): Contains id, body and answer count
            Returns:
                    bodies_with_answers (list): contains id, body and answer count
    """
    bodies_with_answers = []
    data = zip(data[0], data[1], data[2])

    for post_id, body, answer_count in data:
        # Check if answer count exist or if it's not 0
        if answer_count is not None:
            if int(answer_count):
                bodies_with_answers.append([int(post_id), body, int(answer_count)])

    return bodies_with_answers


def count_words_in_body(data):
    """
    Returns a list with id, word count and answer count

            Parameter:
                    data (list): Contains id, body and answer count
            Returns:
                    bodies_with_answers (list): contains id, word count and answer count
    """
    for i in range(len(data)):
        body = data[i][1]
        html_patterns = "<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>"
        # Subtract html patterns from the string
        body = re.sub(html_patterns, '', body)
        # Calculate the total words from each body and reasing the data
        data[i][1] = len(re.findall(r'\d+\.\d+|\w+-?\w+|\w', body))

    return data


def generate_data_dict(data):
    """
    Returns a dictionary with post id as key,
              and value is a dictionary with Word count, Answer count and Words per answer ratio

            Parameter:
                    data (list): Contains id, body and answer count
            Returns:
                    bodies_with_answers (list): contains id, word count and answer count
    """
    data_dict = {}
    for post_id, word_count, answer_count in data:
        data_dict.update({post_id: {'Word count': word_count,
                                    'Answer count': answer_count,
                                    'Words per answers ratio': word_count / answer_count}})
    return data_dict


# Top 10 User owner id percentaje of favourite questions--------------------
def get_user_favcount(data):
    """
    Returns a Counter object with Owner id and question favorite count
            Parameter:
                    data (list): Contains data to process
            Returns:
                    Counter object (Counter): contains all owner ids and favorite count
    """
    counter = Counter()
    for row in data:
        # Check if post Id corresponds to Question
        if row.attrib.get('PostTypeId') == '1':
            # Check if Question has favorite count
            if (row.attrib.get('FavoriteCount') is not None) and (row.attrib.get('FavoriteCount') != '0'):
                counter.update({row.attrib.get('OwnerUserId'): int(row.attrib.get('FavoriteCount'))})
    return counter
