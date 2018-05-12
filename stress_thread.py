#!/usr/bin/python

"""
    @author: Eduardo Maia Machado
"""

import requests
import time
import threading
import random
import global_vars

class RequestLoopThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)

        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        while True:
            global_vars.CURRENT_REQUEST += 1
            if global_vars.EXIT:
                exit()
            if global_vars.CURRENT_REQUEST > global_vars.MAX_REQUESTS:
                exit()

            params = {
                'range_start': round(global_vars.RANGE, 2),
                'range_end': round(global_vars.RANGE + 0.5, 2)
            }

            if global_vars.TEST_TYPE == 'sequential':
                global_vars.RANGE += random.random()
            elif global_vars.TEST_TYPE == 'random':
                global_vars.RANGE = random.random() * 100000
            elif global_vars.TEST_TYPE == 'skew':
                global_vars.RANGE = random.random() + 1000

            try:
                if global_vars.RESULT.get(int(time.time())):
                    global_vars.RESULT[int(time.time())]['requests'] += 1
                else:
                    global_vars.RESULT[int(time.time())] = {
                        'requests': 1,
                        'responses': 0
                    }
                
                print('\rRequest: ' + str(global_vars.CURRENT_REQUEST), end='')
                r = requests.get(global_vars.HOST, params=params)

                if r.status_code == 200:
                    if global_vars.RESULT.get(int(time.time())):
                        global_vars.RESULT[int(time.time())]['responses'] += 1
                    else:
                        global_vars.RESULT[int(time.time())] = {
                            'requests': 0,
                            'responses': 1
                        }
                    if r._content == {}:
                        print('Empty data...')
                        global_vars.EXIT = True
                else:
                    print('Error: status ' + str(r.status_code))
                    global_vars.EXIT = True

            except:
                print('Other fail')
                global_vars.EXIT = True

            time.sleep(self.delay)
