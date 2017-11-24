#! /bin/bash

cd "$(dirname "$0")"

VIRTUALENV=.venv

if [ ! -d $VIRTUALENV ]; then
  virtualenv $VIRTUALENV -p python3
fi

source $VIRTUALENV/bin/activate

# Set up MySQL
pip install mysqlclient

# pip install requirements doesnt work
pip install spacy requests numpy sqlalchemy
python -m spacy download en

echo "Installation complete."
echo "Please execute main.py, and use the following statement as a test."
echo "    What is happening next Friday?"

