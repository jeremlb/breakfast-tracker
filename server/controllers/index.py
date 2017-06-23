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

def addBreakfast(userid, channelid, channelname):
    slack = Slack(token=app.config['SLACK_APP_TOKEN'])
    userresult = slack.getUserInfos(userid=userid)

    if userresult.status_code != 200:
        return 'Cant\' retrieve user infos'

    if channelname == 'directmessage':
        return 'Breakfast command need to be triggered in a public or private channel !'

    elif channelname == 'privategroup':
        groupinfo = slack.getGroupInfos(channelid=channelid)

        if groupinfo.status_code != 200:
            return 'Cant\' retrieve group infos'

        group = json.loads(groupinfo.content)
        channelname = group['group']['name']

    user = json.loads(userresult.content)

    fullname = user['user']['real_name']
    avatar = user['user']['profile']['image_512']
    username = user['user']['name']
    date = Breakfast.getNextAvailableDate(channelid)

    bt = Breakfast(
        username=username,
        date=date,
        userid=userid,
        fullname=fullname,
        avatar=avatar,
        channelid=channelid,
        channelname=channelname
    )
    bt.put()

    text = '@' + username + ' merci pour le petit dej, le ' + date.strftime('%A %d %B %Y')
    slack.postMessage(channelid, text, linknames=1)

    return 'Merci pour ce moment !'

def listNextBreakfasts(channel=None):
    nextBreakfasts = Breakfast.getNextBreakfasts(channel)

    text = 'Breakfast planning : \n'

    for b in nextBreakfasts:
        text += b['date'].strftime('%d/%m/%Y') + ' : ' + b['fullname'] + ' @' + b['username']
        text += ' pour #' + b['channelname'] if channel is None and b.has_key('channelname') and b['channelname'] is not None else ''
        text += '\n'

    resp = make_response(json.dumps({
        'text': text
    }))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/breakfast-cmd', methods=['POST'])
def breakfast():
    text = request.form.get('text', type=str)
    userid = request.form.get('user_id', type=str)
    command = request.form.get('command', type=str)
    channelid = request.form.get('channel_id', type=str)
    channelname = request.form.get('channel_name', type=str)

    logging.info(request.form)
    logging.info(channelname)

    if command == '/bt':
        return addBreakfast(userid, channelid, channelname)
    elif command == '/breakfast':
        if text == 'list':
            return listNextBreakfasts(channel=channelid)
        elif text == 'all':
            return listNextBreakfasts()

    logging.info(request.form)

    return 'Bad command'

@app.route('/interactive-message', methods=['GET', 'POST'])
def interactiveMessage():
    logging.info(request.form)

    payload = request.form.get('payload', type=str)

    if payload is not None:
        resp = make_response(json.dumps({
            "text": "Would you like to play a game?",
                "attachments": [
                    {
                        "text": "Choose a game to play",
                        "fallback": "You are unable to choose a game",
                        "callback_id": "wopr_game",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "game",
                                "text": "Plop1",
                                "type": "button",
                                "value": "chess"
                            },
                            {
                                "name": "game",
                                "text": "Plop2",
                                "type": "button",
                                "value": "maze"
                            }
                        ]
                    }
                ]
            }))

    else:


        resp = make_response(json.dumps({
            "text": "Would you like to play a game?",
                "attachments": [
                    {
                        "text": "Choose a game to play my game @jeremilebourhis",
                        "fallback": "You are unable to choose a game",
                        "callback_id": "wopr_game",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "game",
                                "text": "Chess",
                                "type": "button",
                                "value": "chess"
                            },
                            {
                                "name": "game",
                                "text": "Falken's Maze",
                                "type": "button",
                                "value": "maze"
                            },
                            {
                                "name": "game",
                                "text": "Thermonuclear War",
                                "style": "danger",
                                "type": "button",
                                "value": "war",
                                "confirm": {
                                    "title": "Are you sure?",
                                    "text": "Wouldn't you prefer a good game of chess?",
                                    "ok_text": "Yes",
                                    "dismiss_text": "No"
                                }
                            }
                        ]
                    }
                ]
            }))

    resp.headers['Content-Type'] = 'application/json'

    return resp