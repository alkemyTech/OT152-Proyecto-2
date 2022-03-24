from collections import Counter


def get_tags_and_ansid(data_chunk):
    """
    Returns two lists with all tags and accepdet answer id.

        Parameters:
                data_chunk (generator): Generator objetc with the data chunk to process
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
                data (map object): Contains two lists with tags and accepted answer id
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

            Parameter tags (map object):
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
