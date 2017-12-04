#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from handlers import any_event_on_day_intent_handler,  \
                     specific_event_on_day_intent_handler, \
                     event_info_intent_handler
from nlp import preprocess_text, select_most_likely_intent
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)


def debug_mode():
    return True


def normal_mode():
    return False


def take_usr_input():
    text = str(input('Message: '))
    return preprocess_text(text)


def main(debug=False):
    usr = take_usr_input()
    intent = select_most_likely_intent(usr)

    if intent == 'AnyEventOnDayIntent':
        data = any_event_on_day_intent_handler(usr)
        if debug:
            pp.pprint(data)
    
    elif intent == 'SpecificEventOnDayIntent':
        data = specific_event_on_day_intent_handler(usr)
        if debug:
            pp.pprint(data)
    
    elif intent == 'EventInfoIntent':
        data = event_info_intent_handler(usr)
        if debug:
            pp.pprint(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the script in debug mode.')
    parser.add_argument('--debug', dest='debug', nargs='?',
                        const=debug_mode, default=normal_mode)
    args = parser.parse_args()
    main(args.debug())

