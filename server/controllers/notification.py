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

@app.route('/breakfast-notification', methods=['GET'])
def notification():

    
    return json.dumps(Breakfast.getTomorowBreakfast())