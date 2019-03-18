"""
Class representations of our key entities
"""
import json
from collections import OrderedDict

from src.transactions.comparison import compare_sentences
import datetime


class Transaction:
    """
    Represents a Transaction, the most granular of our entities.
    Transactions contain a date, description and amount.
    They also contain an optional reference to the Transaction Sequence they belong to.
    """

    def __init__(self, date, description, amount):
        self.date = datetime.datetime.strptime(date, '%m/%d/%Y')
        self.description = description
        self.amount = amount
        self.sequence = None

    def compare_description(self, description):
        """
        Compares the transaction's description to another sentence, to assert similarities between
        two transactions.

        :param description: Sentence to compare to.
        :return: A similarity ratio, from 0 to 1.
        """
        return compare_sentences(self.description, description)

    def to_dict(self):
        return dict(date=self.date.strftime('%m/%d/%Y'),
                    description=self.description,
                    amount=self.amount)

    def __str__(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return str(self)

    @property
    def id(self):
        """
        Generates an id based on the transaction's contents. Different objects with the same contents
        should generate the same id.
        """
        return hash(str(self))


class TransactionSequence:
    """
    Represents a sequence of transactions.
    Transactions in a sequence have:
    - Similar descriptions;
    - Regular intervals, with an acceptable margin
    - Intervals longer than 4 days between each other.
    Sequences also should have at least 4 transactions, and transactions should be owned by no more
    than one sequence.
    """

    def __init__(self, interval):
        self.transactions = OrderedDict()
        self.interval = interval

    def add_transaction(self, transaction, margin, set_ownership=False):
        """
        Adds a transaction to the sequence. If it is not the first transaction being added,
        it also validates the interval rule.

        :param transaction: Transaction to be added to the sequence.
        :param margin: Acceptable distance margin from the expected interval to be considered.
        :param set_ownership: Indicates whether the transaction should consider this sequence
        to be its owner.
        """
        if self.transactions:
            diff = (transaction.date - self.get_last_transaction().date).days
        else:
            diff = self.interval

        if diff in range(self.interval-margin, self.interval+margin+1):
            self.transactions[transaction.id] = transaction
            if set_ownership:
                transaction.sequence = self

    def add_transactions(self, transactions, margin, set_ownership=False):
        """
        Adds a list of transactions to the sequence.
        :param transactions: Transactions to be added to the sequence.
        :param margin: Acceptable distance margin from the expected interval to be considered.
        :param set_ownership: Indicates whether the transactions should consider this sequence
        to be their owner.
        """
        for transaction in transactions:
            self.add_transaction(transaction, margin, set_ownership)

    def get_first_transaction(self):
        """
        Returns the first transaction in the sequence.

        :return: The first transaction in the sequence.
        """
        return self.transactions[next(iter(self.transactions))]

    def get_last_transaction(self):
        """
        Returns the last transaction in the sequence.

        :return: The last transaction in the sequence.
        """
        return self.transactions[next(reversed(self.transactions))]

    def to_dict(self):
        return dict(interval=self.interval,
                    transactions=[transaction.to_dict()
                                  for key, transaction in self.transactions.items()])

    def __str__(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.transactions)

    def __contains__(self, item):
        return item.id in self.transactions

    def __iter__(self):
        yield from [transaction for id, transaction in self.transactions.items()]


class SequenceStorage:
    """
    A Storage for sequences and their transactions. It contains a dictionary acting as a lookup,
    enabling O(n) access to a transaction's sequence.
    """

    def __init__(self):
        self.sequences = OrderedDict()

    def add_sequence(self, sequence):
        """
        Adds a sequence to the storage.

        :param sequence: Sequence of transactions to be added.
        """
        for transaction in sequence:
            self.sequences[transaction.id] = sequence

    def add_sequences(self, sequences):
        """
        Adds a list of sequences to the storage.

        :param sequences: List of sequences of transactions to be added.
        """
        for sequence in sequences:
            self.add_sequence(sequence)

    def get_sequence(self, transaction):
        """
        Given a transaction, returns its sequence.

        :param transaction: Transaction whose sequence should be returned.
        :return: The transaction's sequence.
        """
        if transaction.id in self.sequences:
            return self.sequences[transaction.id]
        else:
            return None

    def to_dict(self):
        return {'transactions': {key: sequence.to_dict()
                                 for key, sequence in self.sequences.items()}}

    def __str__(self):
        return json.dumps(self.to_dict())
