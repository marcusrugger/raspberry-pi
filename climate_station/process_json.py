#!/usr/bin/python3

import json


with open('view.log') as file:
	jsonData = json.load(file)

print("count: {}".format(len(jsonData)))
#print(jsonData)

class process(object):
    FIELD_TEMPERATURE   = 'temperature'
    FIELD_HUMIDITY      = 'humidity'

    FIELD_TOTAL         = 'total'
    FIELD_AVERAGE       = 'average'
    FIELD_HIGH          = 'high'
    FIELD_LOW           = 'low'

    def __init__(self, data):
        self.data = data
        self.results = {}
        self._initializeField(process.FIELD_TEMPERATURE)
        self._initializeField(process.FIELD_HUMIDITY)
        self._processData(data)

    def _initializeField(self, field):
        self.results[field] = {}
        self.results[field][process.FIELD_TOTAL]    = 0
        self.results[field][process.FIELD_HIGH] = {}
        self.results[field][process.FIELD_LOW]  = {}
        self.results[field][process.FIELD_HIGH][field] = 0
        self.results[field][process.FIELD_LOW][field]  = 200

    def _processData(self, data):
        for item in data:
            self._processItem(item)

        self._processAverage(process.FIELD_TEMPERATURE)
        self._processAverage(process.FIELD_HUMIDITY)
        self.results[process.FIELD_TEMPERATURE].pop(process.FIELD_TOTAL, None)
        self.results[process.FIELD_HUMIDITY].pop(process.FIELD_TOTAL, None)

    def _processItem(self, item):
        self._processField(item, process.FIELD_TEMPERATURE)
        self._processField(item, process.FIELD_HUMIDITY)

    def _processField(self, item, field):
        self._processHigh(item, field)
        self._processLow(item, field)
        self._processTotal(item, field)

    def _processHigh(self, item, field):
        if item[field] > self.results[field][process.FIELD_HIGH][field]:
            self.results[field][process.FIELD_HIGH] = item

    def _processLow(self, item, field):
        if item[field] < self.results[field][process.FIELD_LOW][field]:
            self.results[field][process.FIELD_LOW] = item

    def _processTotal(self, item, field):
        t = self.results[field][process.FIELD_TOTAL]
        self.results[field][process.FIELD_TOTAL] = t + item[field]

    def _processAverage(self, field):
        self.results[field][process.FIELD_AVERAGE]  = int(10 * self.results[field][process.FIELD_TOTAL] / len(self.data)) / 10.0


d = process(jsonData)
print(json.dumps(d.results))
