#!/usr/bin/env python
# coding: utf-8

import csv
from collections import defaultdict
from random import randint


def loaddata(filename):
    with open(filename, 'r') as fh:
        return list(csv.DictReader(fh, delimiter=';'))


def learn(trainset):
    """
	Selle funktsiooni peab realiseerima!
	"""
    model = defaultdict(lambda: defaultdict(float))
    for sample in trainset:

        condition = sample["famsup"] + "_" + sample["studytime"] + "_" + sample["health"] + "_" + sample["Dalc"] + "_" + sample["famsize"] + "_" + sample["failures"] + "_" + sample["schoolsup"]
        grade = sample["grade"]
        model[condition][grade] += 1
        model[condition]["__total"] += 1

    return model


def predictGrade(model, sample):
    """
	Selle funktsiooni peab realiseerima!
	"""
    prediction = max(["fail", "pass"],
                         key=lambda hypothesisGrade: model[sample["famsup"] + "_" + sample["studytime"] + "_" + sample["health"] + "_" + sample["Dalc"] + "_" + sample["famsize"] + "_" + sample["failures"] + "_" + sample["schoolsup"]][hypothesisGrade])
    return prediction

def evaluate(model, testset):

    correct = 0

    for testSample in testset:
        rightAnswer = testSample['grade']
        del testSample['grade']

        prediction = predictGrade(model, testSample)

        if rightAnswer == prediction:
            correct += 1

    print("Correct: {0:}%".format(100.0 * correct / len(testset)))


trainset = loaddata('tudeng_train.csv')
model = learn(trainset)

testset = loaddata('tudeng_dev.csv')
evaluate(model, testset)
