import unittest
from unittest.mock import patch, call, Mock

from src.transactions.models import Transaction, TransactionSequence, SequenceStorage


class TransactionTests(unittest.TestCase):

    def test_creation(self):
        json_transaction = dict(date='12/24/2019',
                                description='TEST INVOICE 1234',
                                amount='435.23')
        transaction = Transaction(**json_transaction)
        assert isinstance(transaction, Transaction)
        assert transaction.date.strftime('%m/%d/%Y') == json_transaction['date']
        assert transaction.description == json_transaction['description']
        assert transaction.amount == json_transaction['amount']
        assert transaction.sequence is None

    @patch('src.transactions.models.compare_sentences')
    def test_compare_description(self, compare):
        json_transaction = dict(date='12/24/2019',
                                description='TEST INVOICE 1234',
                                amount='435.23')
        other_description = 'TEST 1014'
        transaction = Transaction(**json_transaction)
        transaction.compare_description(other_description)
        compare.assert_called_with(transaction.description, other_description)

    def test_id(self):
        json_transaction = dict(date='12/24/2019',
                                description='TEST INVOICE 1234',
                                amount='435.23')
        transaction = Transaction(**json_transaction)
        transaction2 = Transaction(**json_transaction)
        transaction3 = Transaction(**json_transaction)
        transaction4 = Transaction(date='12/24/2019',
                                   description='TEST INVOICE 1234',
                                   amount='432.23')
        assert transaction.id == transaction2.id == transaction3.id != transaction4.id


class SequenceTests(unittest.TestCase):

    def create_transaction(self):
        json_transaction = dict(date='12/24/2019',
                                description='TEST INVOICE 1234',
                                amount='435.23')
        return Transaction(**json_transaction)

    def test_creation(self):
        interval = 10
        sequence = TransactionSequence(interval)
        assert sequence.interval == interval
        assert sequence.transactions == {}

    def test_add_first_transaction(self):
        transaction = self.create_transaction()
        interval = 10
        margin = 3
        sequence = TransactionSequence(interval)
        sequence.add_transaction(transaction, margin)
        assert transaction.sequence is None
        assert transaction.id in sequence.transactions

    def test_add_second_transaction(self):
        transaction = self.create_transaction()
        second_transaction = Transaction(date='01/02/2020',
                                         description='TEST INVOICE 1234',
                                         amount='435.23')
        interval = 10
        margin = 3
        sequence = TransactionSequence(interval)
        sequence.add_transaction(transaction, margin)
        sequence.add_transaction(second_transaction, margin)

        assert transaction.sequence is None
        assert second_transaction.sequence is None
        assert transaction.id in sequence.transactions
        assert second_transaction.id in sequence.transactions

    def test_add_second_transaction_outside_margin(self):
        transaction = self.create_transaction()
        second_transaction = Transaction(date='01/02/2021',
                                         description='TEST INVOICE 1234',
                                         amount='435.23')
        interval = 10
        margin = 3
        sequence = TransactionSequence(interval)
        sequence.add_transaction(transaction, margin)
        sequence.add_transaction(second_transaction, margin)

        assert transaction.sequence is None
        assert second_transaction.sequence is None
        assert transaction.id in sequence.transactions
        assert second_transaction.id not in sequence.transactions

    def test_add_transaction_set_ownership(self):
        transaction = self.create_transaction()
        interval = 10
        margin = 3
        sequence = TransactionSequence(interval)
        sequence.add_transaction(transaction, margin, set_ownership=True)
        assert transaction.sequence == sequence
        assert transaction.id in sequence.transactions

    @patch('src.transactions.models.TransactionSequence.add_transaction')
    def test_add_transactions(self, add_transaction):
        transaction1 = self.create_transaction()
        transaction2 = self.create_transaction()
        transaction3 = self.create_transaction()
        transactions = [transaction1, transaction2, transaction3]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)
        add_transaction.assert_has_calls([call(transaction1, margin, ownership),
                                         call(transaction2, margin, ownership),
                                         call(transaction3, margin, ownership)])

    def test_get_first_transaction(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)
        first = sequence.get_first_transaction()
        assert first == transaction1

    def test_get_last_transaction(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)
        first = sequence.get_last_transaction()
        assert first == transaction3

    def test_len(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3]
        interval = 10
        margin = 3
        ownership = True
        expected_length = 3
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)
        length = len(sequence)
        assert length == expected_length

    def test_contains(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)
        assert transaction1 in sequence
        assert transaction3 not in sequence

    def test_iter(self):
        called = Mock()
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)
        for transaction in sequence:
            called(transaction)

        called.assert_has_calls([call(transaction1),
                                 call(transaction2),
                                 call(transaction3)])


class StorageTests(unittest.TestCase):

    def create_sequence(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)
        return sequence

    def test_creation(self):
        storage = SequenceStorage()
        assert isinstance(storage, SequenceStorage)
        assert storage.sequences == {}

    def test_add_sequence(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)

        storage = SequenceStorage()
        storage.add_sequence(sequence)
        assert transaction1.id in storage.sequences
        assert transaction2.id in storage.sequences
        assert transaction3.id in storage.sequences

    def test_add_sequences(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        interval = 10
        margin = 3
        ownership = True
        sequence1 = TransactionSequence(interval)
        sequence1.add_transactions([transaction1, transaction2], margin, ownership)
        sequence2 = TransactionSequence(interval)
        sequence2.add_transactions([transaction3], margin, ownership)

        storage = SequenceStorage()
        storage.add_sequences([sequence1, sequence2])
        assert transaction1.id in storage.sequences
        assert transaction2.id in storage.sequences
        assert transaction3.id in storage.sequences

    def test_get_sequence(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2]
        interval = 10
        margin = 3
        ownership = True
        sequence = TransactionSequence(interval)
        sequence.add_transactions(transactions, margin, ownership)

        storage = SequenceStorage()
        storage.add_sequence(sequence)
        sequence1 = storage.get_sequence(transaction1)
        sequence2 = storage.get_sequence(transaction2)
        sequence3 = storage.get_sequence(transaction3)
        assert sequence1 == sequence2 == sequence
        assert sequence3 is None
