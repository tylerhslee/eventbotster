#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date functions
"""
from datetime import datetime, timezone, timedelta


def today(tz=timezone.utc):
    return datetime.now(tz)


def date_diff(modifier, dow):
    t = today().weekday()
    return (dow + modifier * 7) - t


def add_days(days, tz=timezone.utc):
    return (today(tz) + timedelta(days=days)).replace(hour=0, minute=0, second=0)


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
