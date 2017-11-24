#! /usr/bin/env python
# -*- coding: utf-8 -*-

from handlers import any_event_on_day_intent_handler
from similarity import select_most_likely_intent, nlp


def take_usr_input():
    text = str(input('Message: ')).lower()
    return nlp(text)


usr = take_usr_input()
intent = select_most_likely_intent(usr)

if intent == 'AnyEventOnDayIntent':
    any_event_on_day_intent_handler(usr)

