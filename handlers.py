#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles each intent defined in examples.txt
"""
from parser import keywords, parse_keywords
from dates import DAYS_OF_WEEK, MODIFIERS, date_diff, add_days
from tm import get_info
from database import extract_columns, store_data, find_data
from nlp import preprocess_text


def format_time(dt):
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt.strftime('%Y-%m-%dT%H:%m:%SZ')


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
    target_date = format_time(add_days(diff))  # Add timezone info

    r = get_info(startDateTime=target_date)
    data = extract_columns(r.json())
    data['std_time'] = target_date
    store_data(data)
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

    r = get_info(startDateTime=format_time(target_date, False), keyword=et)
    data = extract_columns(r.json())
    data['std_time'] = target_date
    store_data(data)
    return data


def event_info_intent_handler(doc):
    """
    Handles EventInfoIntent
    Gives the information on an event from the database
    If the event is not found in the database, it will fetch the API.
    """
    for title in parse_keywords(keywords, 'title'):
        if str(preprocess_text(title)) in str(doc):
            data = find_data(title=title)
            return data

