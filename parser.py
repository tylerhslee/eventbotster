#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script will load all examples from examples.txt into lists of strings.
Using keywords.txt, all combinations of keywords will be saved.
All keyword labels should be annotated separately so that the lists can be used
for supervised learning.
"""
import re
import csv

from pprint import PrettyPrinter
from database import get_titles


def add(original, *args):
    content = '\n'.join(args)
    ret = original + '\n' + content + ',.'
    return ret


with open('assets/examples.txt', 'r') as rf:
    g_examples = rf.read()

with open('assets/keywords.txt', 'r') as rf:
    g_keywords = add(rf.read(), 'title', get_titles())


# General functions
def flatten_list(lst):
    return [j for i in lst for j in i]


def remove_comments(raw):
    """
    Remove the comments that are enclosed within triple quotes
    """
    comment = re.match(r'(.|\n)*("""(.|\n)*?""")(.|\n)*', raw)
    if comment is None:
        return raw
    return remove_comments(raw.replace(comment.group(2), '')).strip()


def clean_list(lst):
    return list(filter(lambda k: k != '', lst))

def split_lines(raw):
    """
    Split by newline to get a list of lines
    """
    return clean_list(remove_comments(raw).split('\n'))


def listify_selective(raw, criteria):
    """
    Return a list of lines that meet the criteria
    """
    return [k for k in split_lines(raw) if criteria(k)]


def add_data(d, key, data, names):
    """
    Add all items to the dictionary until a name is found
    """
    d[key] = []
    for p in data:
        if p in names:
            return d
        d[key].append(p)
    return d


def categorize(lines, names):
    """
    Returns a dictionary of all names and appropriate data
    """
    ret = {}
    item = ''
    for num, line in enumerate(lines):
        if line in names:
            add_data(ret, line, lines[num+1:], names)
    return ret


# Examples.txt functions
def is_intent(k):
    """
    Returns 1 if the input is an intent name
    """
    return len(re.findall(r'^[A-Z][a-zA-Z]+(Intent)$', k))


def get_intent_names():
    """
    Return a list of all intent names in examples.txt
    """
    return listify_selective(g_examples, is_intent)


def categorize_intents():
    return categorize(split_lines(g_examples),
                      get_intent_names()) 


def identify_keywords(ex):
    return re.findall(r'\{([a-zA-Z]+)\}', ex)


def replace_keyword(ex, keyword_name, keyword):
    """
    Replaces a keyword in the example string
    """
    regex = r'\{%s\}' % keyword_name
    return re.sub(regex, keyword, ex)


def replace_all_keywords(ex, keyword_name, keywords, delim=','):
    if not(keyword_name in identify_keywords(ex)):
        return [ex]
    return list(map(lambda kw: replace_keyword(ex, keyword_name, kw),
                    parse_keywords(keywords, keyword_name)))


def find_combos(examples, keyword_names, keywords):
    """
    Return a list of example strings with all combinations
    """
    for name in keyword_names:
        f = lambda ex: replace_all_keywords(ex, name, keywords)
        examples = flatten_list(list(map(f, examples)))
    return examples


def parse_intents():
    ret = {}
    for intent, examples in categorize_intents().items():
        ret[intent] = find_combos(examples,
                                  get_keyword_names(),
                                  categorize_keywords())
    return ret


# Keywords.txt functions
def is_name(k, delim=','):
    """
    Returns True if the input is a keyword name
    """
    return not(delim in k) 


def get_keyword_names():
    """
    Returns a list of all keyword names in keywords.txt
    """
    return listify_selective(g_keywords, is_name)


def categorize_keywords():
    return categorize(split_lines(g_keywords),
                      get_keyword_names())


def parse_keywords(keywords, name):
    ret = [item for item in csv.reader(keywords[name])]
    return ret[0]


# Export
intents = parse_intents()
keywords = categorize_keywords()
print(parse_keywords(keywords, 'title'))


if __name__ == '__main__':
    pp = PrettyPrinter(indent=2)
    pp.pprint(parse_intents())

