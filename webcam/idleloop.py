#!/usr/bin/python3

import time


class IdleLoop:
    registrants = []

    def __init__(self):
        self.sleep = 0.2
        self.isDone = False


    def setDone(self, flag):
        self.isDone = flag


    def register(self, registrant):
        self.registrants.append(registrant)


    def unregister(self, registrant):
        self.registrants.remove(registrant)


    def tick(self):
        for registrant in self.registrants:
            registrant.tick()


    def run(self):
        while not self.isDone:
            time.sleep(self.sleep)
            self.tick()