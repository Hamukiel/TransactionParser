"""
Example script for running the algorithm for a file.
"""

import json

from src.transactions.parser import parse_storage


def get_transactions():
    with open('./transactions.json', 'r') as file:
        return json.loads(file.read())


transactions = get_transactions()
storage = parse_storage(transactions)
print(storage)