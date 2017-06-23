from datetime import datetime, timedelta
from google.appengine.ext import ndb

from ..utils.workday import WorkDay

import logging

def get_datetime_today_midnight():
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


class Breakfast(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.StringProperty()
    channelid = ndb.StringProperty()
    channelname = ndb.StringProperty()
    fullname = ndb.StringProperty()
    avatar = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    done = ndb.BooleanProperty(default=False)

    @staticmethod
    def _isWeekEnd(date):
        return date.weekday() < 5

    @staticmethod
    def _getNextWorkDay(date, holidays=None):
        holidays = holidays if holidays is not None else WorkDay.getFrenchHolidays(date.year)
        nextWorkDay = date + timedelta(days=1)

        if Breakfast._isWeekEnd(nextWorkDay) and nextWorkDay not in holidays:
            return nextWorkDay
        else:
            return Breakfast._getNextWorkDay(nextWorkDay, holidays=holidays)

    @staticmethod
    def getNextAvailableDate(channelid):
        q = Breakfast.query().filter(Breakfast.channelid == channelid).order(-Breakfast.date)
        r = q.fetch(1)
        date = r[0].date if len(r) > 0 else get_datetime_today_midnight()

        return Breakfast._getNextWorkDay(date)

    @staticmethod
    def getNextBreakfasts(channelid=None):
        if channelid is not None:
            q = Breakfast.query().filter(Breakfast.date > get_datetime_today_midnight()).filter(Breakfast.channelid == channelid)
        else:
            q = Breakfast.query().filter(Breakfast.date > get_datetime_today_midnight())

        q.order(Breakfast.date)

        results = []
        for breakfast in q.fetch():
            b = breakfast.to_dict()
            b['id'] = breakfast.key.id()
            results.append(b)

        return results

    @staticmethod
    def getTomorowBreakfast():
        tomorow = get_datetime_today_midnight() + timedelta(days=1)
        dayafter = tomorow + timedelta(days=1)
        logging.info(tomorow)
        logging.info(dayafter)
        q = Breakfast.query().filter(Breakfast.date > tomorow).filter(Breakfast.date < dayafter)

        results = []
        for breakfast in q.fetch():
            b = breakfast.to_dict()
            b['id'] = breakfast.key.id()
            results.append(b)

        return results


