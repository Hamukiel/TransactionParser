TransactionParser
=================

TransactionParser is a simple API/algorithm for parsing JSON structured data into a Storage Structure.

The input is a list of transactions, sorted by date, containing a date, a string description
and a transaction amount.

Although the sample script provided loads data from a file, the data source may be easily modified to load
from an API call or a database.

Transactions are loaded into Transaction objects, and should be parsed into sequences considering the following rules:

- Transactions in a sequence have similar descriptions;

- Transactions in a sequence have regular time intervals, with an adjustable acceptable margin (default 3 days);

- Transactions in a sequence should not happen within 3 days or less of each other;

- Transaction sequences should have at least 4 transactions;

- Transactions should not belong to multiple sequences.

After sequences are parsed, they are made available through a Storage class, which can retrieve a transaction's
sequence in O(n) time.

Routes
------

The provided API exposes two POST routes:

/transactions/load builds the storage, either from the "transactions" key in a provided json body or
from the default sample data.

.. code-block:: text

   curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
    '{"transactions": {<insert transaction data here>}}' \
    'http://127.0.0.1:5000/transactions/load'

.. code-block:: text

   curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
    '' \
    'http://127.0.0.1:5000/transactions/load'

/transactions/get_sequence returns a provided transaction's sequence. The transaction should be sent inside
a "transaction key:

.. code-block:: text

   curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
    '{"transaction":  {"date": "11/22/2018", "description": "EXXON MOBIL CORPORATION", "amount": -99.69}}' \
    'http://127.0.0.1:5000/transactions/get_sequence'

Improvements
------------

- The sentence comparison algorithm is pretty simple and inefficient. It could be changed for a specialized library

- Persistence. It should be simple to move the Storage Structure to Redis and to a conventional database.

- Coverage. 90% is not 100%