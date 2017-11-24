#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests

URL = 'https://app.ticketmaster.com/discovery/v2/events.json?size=1&apikey=80Yiy3BkF0kupWGVzo75UtuPdt1Vu1V3'


def format_time(dt):
    return dt.strftime('%Y-%m-%dT%H:%m:%SZ')


def get_info(dt):
    target = URL + '&startDateTime=' + format_time(dt)
    print(target)
    return requests.get(target)

