from flask import Blueprint, request, make_response, current_app
from werkzeug.exceptions import BadRequest

from src.transactions.models import Transaction
from src.transactions.parser import parse_storage

import json


def create_blueprint():
    bp = Blueprint('transactions', __name__, url_prefix='/transactions')
    return bp


mod_transactions = create_blueprint()


@mod_transactions.route('/load', methods=['POST'])
def load():
    def get_transactions():
        with open('./transactions.json', 'r') as file:
            return json.loads(file.read())

    try:
        jdata = request.get_json()
        transactions = jdata['transactions']
    except (KeyError, BadRequest) as e:
        # we load the default data if the transactions were not provided.
        transactions = get_transactions()

    current_app.storage = parse_storage(transactions)

    return make_response('OK'), 200


@mod_transactions.route('/get_sequence', methods=['POST'])
def get_sequence():
    jdata = request.get_json()
    try:
        jtransaction = jdata['transaction']
    except KeyError:
        raise BadRequest("The Transaction was not provided")

    try:
        storage = current_app.storage
    except AttributeError:
        raise BadRequest("The Storage was not loaded")

    transaction = Transaction(**jtransaction)
    sequence = storage.get_sequence(transaction)

    response = make_response(str(sequence))
    response.mimetype = 'application/json'
    return response, 200
