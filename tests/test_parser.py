import unittest

from src.transactions.models import Transaction, TransactionSequence
from src.transactions.parser import parse_sequences, parse_storage


class ParserTests(unittest.TestCase):

    def test_parse_single_sequence(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction4 = Transaction(date='02/01/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3, transaction4]

        sequences = parse_sequences(transactions)

        assert len(sequences) == 1
        assert isinstance(sequences[0], TransactionSequence)
        assert transaction1 in sequences[0]
        assert transaction2 in sequences[0]
        assert transaction3 in sequences[0]
        assert transaction4 in sequences[0]

    def test_parse_short_sequence(self):
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

        sequences = parse_sequences(transactions)

        assert len(sequences) == 0

    def test_parse_short_interval(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/05/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='01/08/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction4 = Transaction(date='01/11/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3, transaction4]

        sequences = parse_sequences(transactions)

        assert len(sequences) == 0

    def test_parse_single_sequence_with_singletons(self):
        transaction1 = Transaction(date='01/02/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactionX1 = Transaction(date='01/10/2020',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transaction2 = Transaction(date='01/12/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactionX2 = Transaction(date='01/18/2020',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transaction3 = Transaction(date='01/22/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction4 = Transaction(date='02/01/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactions = [transaction1, transaction2, transaction3, transaction4]

        sequences = parse_sequences(transactions)

        assert len(sequences) == 1
        assert isinstance(sequences[0], TransactionSequence)
        assert transaction1 in sequences[0]
        assert transaction2 in sequences[0]
        assert transaction3 in sequences[0]
        assert transaction4 in sequences[0]
        assert transactionX1 not in sequences[0]
        assert transactionX2 not in sequences[0]

    def test_parse_multiple_sequences(self):
        transaction1 = Transaction(date='01/01/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction2 = Transaction(date='01/15/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction3 = Transaction(date='02/01/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transaction4 = Transaction(date='02/15/2020',
                                   description='TEST INVOICE 1234',
                                   amount='435.23')
        transactionX1 = Transaction(date='01/01/2021',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactionX2 = Transaction(date='02/10/2021',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactionX3 = Transaction(date='03/20/2021',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactionX4 = Transaction(date='04/30/2021',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactionY1 = Transaction(date='03/10/2022',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactionY2 = Transaction(date='03/20/2022',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactionY3 = Transaction(date='03/30/2022',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactionY4 = Transaction(date='04/09/2022',
                                    description='TEST INVOICE 1234',
                                    amount='435.23')
        transactions = [transaction1, transaction2, transaction3, transaction4,
                        transactionX1, transactionX2, transactionX3, transactionX4,
                        transactionY1, transactionY2, transactionY3, transactionY4]

        sequences = parse_sequences(transactions)
        print(sequences)
        assert len(sequences) == 3
        assert isinstance(sequences[0], TransactionSequence)
        assert isinstance(sequences[1], TransactionSequence)
        assert isinstance(sequences[2], TransactionSequence)
        assert transaction1 in sequences[0]
        assert transaction2 in sequences[0]
        assert transaction3 in sequences[0]
        assert transaction4 in sequences[0]
        assert transactionX1 in sequences[1]
        assert transactionX2 in sequences[1]
        assert transactionX3 in sequences[1]
        assert transactionX4 in sequences[1]
        assert transactionY1 in sequences[2]
        assert transactionY2 in sequences[2]
        assert transactionY3 in sequences[2]
        assert transactionY4 in sequences[2]

    def test_parse_storage_single_sequence(self):
        transactions = [
            dict(date='01/02/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23'),
            dict(date='01/12/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23'),
            dict(date='01/22/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23'),
            dict(date='02/01/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23')
        ]
        storage = parse_storage(transactions)
        sequence1 = storage.get_sequence(Transaction(date='01/02/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))
        sequence2 = storage.get_sequence(Transaction(date='01/12/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))
        sequence3 = storage.get_sequence(Transaction(date='01/22/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))
        sequence4 = storage.get_sequence(Transaction(date='02/01/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))

        assert sequence1 == sequence2 == sequence3 == sequence4

    def test_parse_storage_multiple_sequences(self):
        transactions = [
            dict(date='01/02/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23'),
            dict(date='01/12/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23'),
            dict(date='01/22/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23'),
            dict(date='02/01/2020',
                 description='TEST INVOICE 1234',
                 amount='435.23'),
            dict(date='01/02/2020',
                 description='ANOTHER TEST 1432',
                 amount='435.23'),
            dict(date='01/12/2020',
                 description='ANOTHER TEST 1234',
                 amount='435.23'),
            dict(date='01/22/2020',
                 description='ANOTHER TEST 2234',
                 amount='435.23'),
            dict(date='02/01/2020',
                 description='ANOTHER TEST 3334',
                 amount='435.23'),
            dict(date='01/02/2020',
                 description='THIRD*ONE*6565',
                 amount='435.23'),
            dict(date='01/12/2020',
                 description='THIRD*ONE*2907',
                 amount='435.23'),
            dict(date='01/22/2020',
                 description='THIRD*ONE*5555',
                 amount='435.23'),
            dict(date='02/01/2020',
                 description='THIRD*ONE*2356',
                 amount='435.23')
        ]
        storage = parse_storage(transactions)
        sequence1 = storage.get_sequence(Transaction(date='01/02/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))
        sequence2 = storage.get_sequence(Transaction(date='01/12/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))
        sequence3 = storage.get_sequence(Transaction(date='01/22/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))
        sequence4 = storage.get_sequence(Transaction(date='02/01/2020',
                                                     description='TEST INVOICE 1234',
                                                     amount='435.23'))
        sequence5 = storage.get_sequence(Transaction(date='01/02/2020',
                                                     description='ANOTHER TEST 1432',
                                                     amount='435.23'))
        sequence6 = storage.get_sequence(Transaction(date='01/12/2020',
                                                     description='ANOTHER TEST 1234',
                                                     amount='435.23'))
        sequence7 = storage.get_sequence(Transaction(date='01/22/2020',
                                                     description='ANOTHER TEST 2234',
                                                     amount='435.23'))
        sequence8 = storage.get_sequence(Transaction(date='02/01/2020',
                                                     description='ANOTHER TEST 3334',
                                                     amount='435.23'))
        sequence9 = storage.get_sequence(Transaction(date='01/02/2020',
                                                     description='THIRD*ONE*6565',
                                                     amount='435.23'))
        sequence10 = storage.get_sequence(Transaction(date='01/12/2020',
                                                      description='THIRD*ONE*2907',
                                                      amount='435.23'))
        sequence11 = storage.get_sequence(Transaction(date='01/22/2020',
                                                      description='THIRD*ONE*5555',
                                                      amount='435.23'))
        sequence12 = storage.get_sequence(Transaction(date='02/01/2020',
                                                      description='THIRD*ONE*2356',
                                                      amount='435.23'))

        assert sequence1 == sequence2 == sequence3 == sequence4
        assert sequence5 == sequence6 == sequence7 == sequence8
        assert sequence9 == sequence10 == sequence11 == sequence12
        assert sequence1 != sequence5 != sequence12
