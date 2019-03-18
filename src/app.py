from flask import Flask

from src.transactions.blueprint import mod_transactions


def create_app():
    app = Flask(__name__)
    app.register_blueprint(mod_transactions)
    return app
