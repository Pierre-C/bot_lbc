from os import environ
from flask import Flask

# app = Flask(__name__)
# app.run(environ.get('PORT'))

import logging
import bot_lbc
import sys

from flask import Flask

app = Flask(__name__)

@app.before_first_request
def launch_script():
    return bot_lbc.launch_script()


@app.route('/')
def say_hello():
    return "LBC bot ran, check Gmail!"


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)