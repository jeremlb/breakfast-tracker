from google.appengine.api import urlfetch
import urllib
import logging

SLACK_ENDPOINT_URL = 'http://slack.com/api/'

class Slack:
    def __init__(self, token):
        self.token = token

    def postMessage(self, channel, text, attachments='', linknames=0):
        return self._makeRequest('chat.postMessage', urlfetch.GET, {
            'token': self.token,
            'channel': channel,
            'text': text,
            'attachments': attachments,
            'parse': 'full',
            'link_names': linknames,
            'pretty':1
        })

    def getUserInfos(self, userid):
        return self._makeRequest('users.info', urlfetch.GET, {'token': self.token, 'user': userid})

    def getChannelInfos(self, channelid):
        return self._makeRequest('channels.info', urlfetch.GET, {'token': self.token, 'channel': channelid})

    def getGroupInfos(self, channelid):
        return self._makeRequest('groups.info', urlfetch.GET, {'token': self.token, 'channel': channelid})

    def _makeRequest(self, endpoint, method, data):
        form_data = urllib.urlencode(data)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        return urlfetch.fetch(
            url=SLACK_ENDPOINT_URL + endpoint + '?' + form_data,
            method=method,
            headers=headers)
