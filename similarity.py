#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Predicts the most likely intent given user input
"""

import spacy

import numpy as np

from parser import intents 

nlp = spacy.load('en')


def calculate_similarity(usr, intent_name):
    return np.array([usr.similarity(nlp(ex)) for ex in intents[intent_name]]) \
            .max()


def analyze_similarities(usr):
    ret = {}
    for name in intents.keys():
        ret[name] = calculate_similarity(usr, name)
    return ret


def select_most_likely_intent(usr):
    sims = analyze_similarities(usr)
    max_sim = max(list(sims.values()))
    
    # Not similar enough
    if max_sim < 0.5:
        return None

    for name, sim in sims.items():
        if sim == max_sim:
            return name


if __name__ == '__main__':
    usr = take_usr_input()
    print(select_most_likely_intent(usr))

