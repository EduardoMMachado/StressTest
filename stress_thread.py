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
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)

        self.threadID = threadID
        self.name = name

    def run(self):
        while True:
            global_vars.CURRENT_REQUEST += 1
            if global_vars.CURRENT_REQUEST > global_vars.MAX_REQUESTS:
                print('\rEXIT', end='')
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

                print('\rREQUESTS: ' + str(global_vars.CURRENT_REQUEST) + ' RESPONSES: ' + str(global_vars.CURRENT_RESPONSE), end='')
                r = requests.get(global_vars.HOST, params=params)
                global_vars.CURRENT_RESPONSE += 1

                if r.status_code == 200:
                    if global_vars.RESULT.get(int(time.time())):
                        global_vars.RESULT[int(time.time())]['responses'] += 1
                    else:
                        global_vars.RESULT[int(time.time())] = {
                            'requests': 0,
                            'responses': 1
                        }
                    if r._content == {}:
                        print('\rERROR1', end='')  # Empty data
                        exit()
                else:
                    print('\rERROR2', end='')  # Status != 200
                    exit()

                time.sleep(0.5)

            except Exception as exc:
                print('\r' + str(exc) , end='')  # Other fail
                exit()
