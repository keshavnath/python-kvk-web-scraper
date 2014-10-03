#!/usr/bin/python

import time

class Timer:
    'Utility class that provides timer functionality'
    start_time = -1
    stop_time = -1

    def __init__(self):
        self.start()

    def start(self):
       self.start_time = time.time()
       
    def stop(self):
       self.stop_time = time.time()

    def exectime(self):
        return self.stop_time - self.start_time