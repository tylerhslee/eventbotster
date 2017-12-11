#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask, request, render_template
from handlers import any_event_on_day_intent_handler,  \
                     specific_event_on_day_intent_handler,  \
                     event_info_intent_handler
from nlp import select_most_likely_intent
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)
app = Flask(__name__)


def render_data(data):
    data_to_send = json.dumps(data).replace("'", "\\'").replace('"', '\\"')
    return render_template('index.html', data=data_to_send, show_data='true')


def handle_intent(intent_name, usr):
    if intent_name == 'AnyEventOnDayIntent':
        data = any_event_on_day_intent_handler(usr)
        return render_data(data)

    elif intent_name == 'SpecificEventOnDayIntent':
        data = specific_event_on_day_intent_handler(usr)
        return render_data(data)

    elif intent_name == 'EventInfoIntent':
        data = event_info_intent_handler(usr)
        pp.pprint(data)
        return render_data(data)

    else:
        return render_template('index.html', data=[], show_data='false')


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html', data=[], show_data='false')
    elif request.method == 'POST':
        user_in = request.form['userIn']
        intent = select_most_likely_intent(user_in)
        return handle_intent(intent, user_in)
            

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

