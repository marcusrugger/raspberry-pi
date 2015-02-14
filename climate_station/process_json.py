#!/usr/bin/python3

import json


with open('data.150213.log') as file:
	jsonData = json.load(file)

print("count: {}".format(len(jsonData)))
#print(jsonData)

class process(object):
    KEY_TEMPERATURE   = 'temperature'
    KEY_HUMIDITY      = 'humidity'

    KEY_TOTAL         = 'total'
    KEY_AVERAGE       = 'average'
    KEY_HIGH          = 'high'
    KEY_LOW           = 'low'

    def __init__(self, data):
        self.data = data
        self.results = {}
        self._initializeField(process.KEY_TEMPERATURE)
        self._initializeField(process.KEY_HUMIDITY)
        self._processData(data)

    def _initializeField(self, key):
        self.results[key] = {}
        self.results[key][process.KEY_TOTAL]    = 0
        self.results[key][process.KEY_HIGH] = {}
        self.results[key][process.KEY_LOW]  = {}
        self.results[key][process.KEY_HIGH][key] = 0
        self.results[key][process.KEY_LOW][key]  = 200

    def _processData(self, data):
        for item in data:
            self._processItem(item)

        self._processAverage(process.KEY_TEMPERATURE)
        self._processAverage(process.KEY_HUMIDITY)
        self.results[process.KEY_TEMPERATURE].pop(process.KEY_TOTAL, None)
        self.results[process.KEY_HUMIDITY].pop(process.KEY_TOTAL, None)

    def _processItem(self, item):
        self._processField(item, process.KEY_TEMPERATURE)
        self._processField(item, process.KEY_HUMIDITY)

    def _processField(self, item, key):
        self._processHigh(item, key)
        self._processLow(item, key)
        self._processTotal(item, key)

    def _processHigh(self, item, key):
        if item[key] > self.results[key][process.KEY_HIGH][key]:
            self.results[key][process.KEY_HIGH] = item

    def _processLow(self, item, key):
        if item[key] < self.results[key][process.KEY_LOW][key]:
            self.results[key][process.KEY_LOW] = item

    def _processTotal(self, item, key):
        t = self.results[key][process.KEY_TOTAL]
        self.results[key][process.KEY_TOTAL] = t + item[key]

    def _processAverage(self, key):
        self.results[key][process.KEY_AVERAGE]  = int(10 * self.results[key][process.KEY_TOTAL] / len(self.data)) / 10.0


d = process(jsonData)
print(json.dumps(d.results))
