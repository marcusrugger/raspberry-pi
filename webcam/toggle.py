#!/usr/bin/python3


class Toggle:
    def __init__(self, obj):
        self.obj = obj
        self.toggle = False


    def tick(self):
        self.toggle = not self.toggle
        self.obj.set(self.toggle)
