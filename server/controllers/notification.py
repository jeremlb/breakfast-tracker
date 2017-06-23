"""
"""
from __future__ import absolute_import
import logging
import json

from datetime import datetime

from flask import render_template
from flask import request
from flask import make_response

from . import app
from ..utils.slack import Slack
from ..models.breakfast import Breakfast

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

@app.route('/breakfast-notification', methods=['GET'])
def notification():
    slack = Slack(token=app.config['SLACK_APP_TOKEN'])

    for breakfast in Breakfast.getTomorowBreakfast():
        text = 'Breakfast Tracker remind you that you should come with a breakfast tomorrow for #' + breakfast['channelname']
        slack.postMessage(breakfast['userid'], text)

    return make_response('ok')