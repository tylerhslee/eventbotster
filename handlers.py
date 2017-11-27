#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles each intent defined in examples.txt
"""
from parser import keywords, parse_keywords
from dates import DAYS_OF_WEEK, MODIFIERS, date_diff, add_days 
from tm import get_info

def any_event_on_day_intent_handler(doc):
    modifier = MODIFIERS['this']
    for tok in doc:
        if tok.text in parse_keywords(keywords, 'modifier'):
            modifier = MODIFIERS[tok.text]
        if tok.text in parse_keywords(keywords, 'dayOfWeek'):
            dow = DAYS_OF_WEEK[tok.text]
    
    diff = date_diff(modifier, dow)
    target_date = add_days(diff)  # Add timezone info

    r = get_info(target_date)
    print(r.json())

