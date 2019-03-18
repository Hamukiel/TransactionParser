from collections import OrderedDict

import itertools

from src.transactions.models import TransactionSequence, Transaction, SequenceStorage


MINIMUM_TRANSACTIONS = 4
MINIMUM_INTERVAL = 4
DEFAULT_MARGIN = 3
SIMILARITY_RATIO = 0.5


def parse_sequences(transaction_list, margin=DEFAULT_MARGIN):
    """
    Given a list of transactions with similar descriptions, find sequences that respect
    the interval rule.

    :param transaction_list: List of transactions with similar descriptions.
    :param margin: Acceptable margin for the interval rule.
    :return: List of valid sequences.
    """
    def get_margin(days):
        return [str(i) for i in range(days - margin, days+margin+1)]

    # First, we should evaluate sequence candidates from transaction combinations.
    # By using itertools.combinations, we avoid the issue of singleton transactions breaking
    # a possible sequence.
    delta_hash = OrderedDict()
    for a, b in itertools.combinations(transaction_list, 2):
        xdiff = b.date - a.date
        if xdiff.days >= MINIMUM_INTERVAL:                                            # '4 day rule' evaluation
            keys = list(set(delta_hash.keys()).intersection(get_margin(xdiff.days)))  # margin evaluation
            if len(keys) > 0:
                delta_hash[keys[0]].add_transactions([a, b], margin=margin)
            else:
                sequence = TransactionSequence(interval=xdiff.days)
                sequence.add_transactions([a, b], margin=margin)
                delta_hash[str(xdiff.days)] = sequence

    sequences = []
    # Now that we have the candidates, we should make sure that we are adhering to the minimum transactions and
    # the single-sequence rules, iterating through our candidates to get rid of extra sequences.
    for key, sequence in delta_hash.items():
        transactions = [transaction for transaction in sequence
                        if not transaction.sequence]                                # Single-sequence evaluation

        if len(transactions) >= MINIMUM_TRANSACTIONS:                               # Minimum transactions evaluation
            clean_sequence = TransactionSequence(interval=int(key))
            clean_sequence.add_transactions(transactions, margin=margin, set_ownership=True)
            sequences.append(clean_sequence)

    return sequences


def parse_storage(json_transactions):
    """
    Parses a list of dict transactions into a Sequence Storage.

    :param json_transactions: List of transactions in a dict format.
    :return: SequenceStorage
    """
    transactions = [Transaction(**transaction) for transaction in json_transactions]

    storage = SequenceStorage()

    # We iterate through the list of transactions, parsing sequences from those that have similar descriptions
    # and adding those to a Sequence Storage.
    while len(transactions) > 0:
        transaction = transactions[0]

        descs = list(filter(lambda x: x.compare_description(transaction.description) > SIMILARITY_RATIO, transactions))
        sequences = parse_sequences(descs)
        storage.add_sequences(sequences)
        for tran in descs:
            transactions.remove(tran)

    return storage
