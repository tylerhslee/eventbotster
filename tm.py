#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests

URL = ('https://app.ticketmaster.com/discovery/v2/events.json' +
       '?size=1&apikey=80Yiy3BkF0kupWGVzo75UtuPdt1Vu1V3' +
       '&countryCode=US&stateCode=NY')


def format_time(dt):
    return dt.strftime('%Y-%m-%dT%H:%m:%SZ')


def write_query(key, value):
    fstring = '&{key}={value}'
    if key == 'date':
        return fstring.format(key='startDateTime', value=format_time(value))
    if key == 'event':
        return fstring.format(key='keyword', value=value)


def get_info(**kwargs):
    queries = list(map(lambda k: write_query(k, kwargs[k]), kwargs.keys()))
    target = URL + ''.join(queries)
    print(target)
    return requests.get(target)

