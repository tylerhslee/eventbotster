#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date functions
"""
from datetime import datetime, timedelta
from pytz import timezone

TIMEZONE = timezone('UTC')


def set_timezone(tz):
    global TIMEZONE
    TIMEZONE = timezone(tz)


def today():
    return datetime.now(TIMEZONE)


def date_diff(modifier, dow):
    t = today().weekday()
    return (dow + modifier * 7) - t


def add_days(days):
    return (today() + timedelta(days=days)).replace(hour=0, minute=0, second=0)


# Export
DAYS_OF_WEEK = {'monday': 0,
               'tuesday': 1,
               'wednesday': 2,
               'thursday': 3,
               'friday': 4,
               'saturday': 5,
               'sunday': 6}

MODIFIERS = {'this': 0,
            'next': 1}
