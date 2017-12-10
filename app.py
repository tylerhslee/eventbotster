from flask import Flask, render_template
import MySQLdb as mdb
from handlers import any_event_on_day_intent_handler
from similarity import spacy, nlp

app = Flask(__name__)
@app.route('/')


def someting():
    
    intent = select_most_likely_intent(usr)
    if intent == 'AnyEventOnDayIntent':
        data = any_event_on_day_intent_handler(usr)
        return render_template('index.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)