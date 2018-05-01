#!/usr/bin/python

"""
    @author: Eduardo Maia Machado
"""

import requests
import time
import threading
import sys
import random
import json

ROUTE = 'http://35.196.226.41:8000/list'
N_THREADS = 16
EXIT = False
RANGE = 0.01
MAX_RANGE = 100
RESULT = {}

class RequestLoopThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)

        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        global EXIT
        global RANGE

        while True:
            global RESULT
            if EXIT:
                exit()
            if RANGE > MAX_RANGE:
                exit()

            params = {
                'range_start': round(RANGE, 2),
                'range_end': round(RANGE + 0.01, 2)
            }

            try:
                if RESULT.get(int(time.time())):
                    RESULT[int(time.time())]['requests'] += 1
                else:
                    RESULT[int(time.time())] = {
                        'requests': 1,
                        'responses': 0
                    }
                
                print('\rRange: ' + str(round(RANGE, 2)), end='')
                r = requests.get(ROUTE, params=params)

                if r.status_code == 200:
                    if RESULT.get(int(time.time())):
                        RESULT[int(time.time())]['responses'] += 1
                    else:
                        RESULT[int(time.time())] = {
                            'requests': 0,
                            'responses': 1
                        }
                    if r._content == {}:
                        EXIT = True
                else:
                    EXIT = True

            except:
                EXIT = True

            RANGE += random.random()
            time.sleep(self.delay)

threads = []
for n in range(N_THREADS):
    t = RequestLoopThread(n, 'Thread-'+str(n), 0.1)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

with open('data.json', 'w') as file:
    print('\nWrite json file...')
    file.write(json.dumps(RESULT, indent=4, sort_keys=True))
    file.close()
