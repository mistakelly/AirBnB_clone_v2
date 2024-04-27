#!/usr/bin/python3

"""Script that starts a Flask web application
listening on address 0.0.0.0 port 5000
adds another route to serve /HBNB
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb() -> str:
    """ Function that generates the main route """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def do_hbnb() -> str:
    """ Function that generates that serves hbhb"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def custom_url(text) -> str:
    """ Function that generates that serves hbhb"""
    if '_' in  text:
        text = text.replace('_', ' ')
    return f'C {text}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
