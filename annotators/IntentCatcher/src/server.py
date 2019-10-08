#!/usr/bin/env python

from os import getenv

import tensorflow as tf
import logging
import sentry_sdk
import uuid
from flask import Flask, request, jsonify

from src.detector import USESimpleDetector

sentry_sdk.init(getenv('SENTRY_DSN'))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)

app = Flask(__name__)

sess = tf.compat.v1.Session()

logger.info('Creating detector...')
detector = USESimpleDetector(logger)
logger.info('Creating detector... finished')

logger.info('Initializing tf variables...')
sess.run(tf.compat.v1.tables_initializer())

logger.info("Tables initialized")
sess.run(tf.compat.v1.global_variables_initializer())

logger.info("DONE")


@app.route("/detect", methods=['POST'])
def detect():
    session_id = uuid.uuid4().hex
    logger.info(f"Session_id: {session_id}")
    utterances = request.json['sentences']
    logger.info(f"Number of utterances: {len(utterances)}")
    results = detector.detect(utterances, sess)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8014)
    sess.close()
