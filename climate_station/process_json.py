#!/usr/bin/python3

import json


with open('view.log') as file:
	jsonData = json.load(file)

#print(jsonData)

class process(object):
    def __init__(self, jsonData):
        self.jsonData
        self.hi_temp = 0
        self.lo_temp = 200
        self.hi_temp_item = {}
        self.lo_temp_item = {}

    def _processItem(item):
        if

hi = 0
hiItem = {}
lo = 100
loItem = {}
for item in jsonData:
    t = item['temperature']
    if t > hi:
        hi = t
        hiItem = item
    if t < lo:
        lo = t
        loItem = item

print("Hi: {}".format(hiItem))
print("Lo: {}".format(loItem))

