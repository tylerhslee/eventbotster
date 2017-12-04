#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests

URL = ('https://app.ticketmaster.com/discovery/v2/events.json' +
       '?size=1&apikey=80Yiy3BkF0kupWGVzo75UtuPdt1Vu1V3' +
       '&countryCode=US&stateCode=NY')


def write_query(key, value):
    fstring = '&{key}={value}'.format(key=key, value=value)
    return fstring


def get_info(**kwargs):
    queries = list(map(lambda k: write_query(k, kwargs[k]), kwargs.keys()))
    target = URL + ''.join(queries)
    print(target)
    return requests.get(target)

