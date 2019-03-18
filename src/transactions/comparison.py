"""
Pretty simple comparison algorithm for strings, lists and sentences in general.
We could improve this project's performance by leveraging specialized libraries instead.
"""


DEFAULT_SPLITTERS = ['--', '*']


def compare_iterables(iterable_a, iterable_b):
    """
    Compares 2 iterables, specifically designed for strings and lists.

    :return: A similarity ratio, ranging from 0 to 1.
    """

    similarity = 0
    difference = 0

    min_length = min(len(iterable_a), len(iterable_b))

    for i in range(0, min_length):
        if iterable_a[i] == iterable_b[i]:
            similarity += 1
        else:
            difference += 1

    ratio = similarity / (similarity+difference)
    return ratio


def compare_sentences(sentence_a, sentence_b, extra_splits=DEFAULT_SPLITTERS):
    """
    Compares 2 sentences, splitting both into lists and then comparing each of their values.

    :param sentence_a: Sentence for comparison.
    :param sentence_b: Sentence for comparison.
    :param extra_splits: List of strings other than whitespaces to be considered as splitters.
    :return: A similarity ratio, ranging from 0 to 1.
    """

    def split_sentence(sentence):
        reworked_sentence = sentence.strip()
        for chars in extra_splits:
            reworked_sentence = reworked_sentence.replace(chars, ' ')
        return reworked_sentence.split()

    reworked_a = split_sentence(sentence_a)
    reworked_b = split_sentence(sentence_b)
    return compare_iterables(reworked_a, reworked_b)
