#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles each intent defined in examples.txt
"""
from parser import keywords, parse_keywords
from dates import DAYS_OF_WEEK, MODIFIERS, date_diff, add_days
from tm import get_info
from database import find_table, store_data


def any_event_on_day_intent_handler(doc):
    """
    Handles AnyEventOnDayIntent
    """
    modifier = MODIFIERS['this']
    for tok in doc:
        if tok.text in parse_keywords(keywords, 'modifier'):
            modifier = MODIFIERS[tok.text]
        if tok.text in parse_keywords(keywords, 'dayOfWeek'):
            dow = DAYS_OF_WEEK[tok.text]

    diff = date_diff(modifier, dow)
    target_date = add_days(diff)  # Add timezone info

    data = find_table(start_date=target_date)
    if len(data.keys()) == 0:
        r = get_info(date=target_date)
        store_data(r.json())
        return r.json()
    return data


def specific_event_on_day_intent_handler(doc):
    """
    Handles SpecificEventOnDayIntent
    Always fetches the API because we can't store
    "keyword" column in the database.
    """
    modifier = MODIFIERS['this']
    for tok in doc:
        if tok.text in parse_keywords(keywords, 'modifier'):
            modifier = MODIFIERS[tok.text]
        if tok.text in parse_keywords(keywords, 'dayOfWeek'):
            dow = DAYS_OF_WEEK[tok.text]
        if tok.text in parse_keywords(keywords, 'eventType'):
            et = tok.text

    diff = date_diff(modifier, dow)
    target_date = add_days(diff)  # Add timezone info

    r = get_info(date=target_date, keyword=et)
    return r.json()
