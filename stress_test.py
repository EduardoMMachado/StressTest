#!/usr/bin/python

"""
    @author: Eduardo Maia Machado
"""

import time
import json
import global_vars
from argparse import ArgumentParser
from stress_thread import RequestLoopThread

# Arguments Parser
parser = ArgumentParser()

parser.add_argument("-u", "--url", type=str, help="URL to be tested")
parser.add_argument("-n", "--threads_number", type=int, help="Number of threads")
parser.add_argument("-r", "--range", type=float, help="Request search range")
parser.add_argument("-m", "--max_requests", type=int, help="Number of requests")
parser.add_argument("-t", "--test_type", type=str, help="Test Type (sequential, random or skew)")

args = parser.parse_args()

if args.url:
    global_vars.HOST = args.url
if args.threads_number:
    global_vars.N_THREADS = args.threads_number
if args.range:
    global_vars.RANGE = args.range
if args.max_requests:
    global_vars.MAX_REQUESTS = args.max_requests
if args.test_type:
    global_vars.TEST_TYPE = args.test_type

# Start threads
threads = []
for n in range(global_vars.N_THREADS):
    t = RequestLoopThread(n, 'Thread-'+str(n), 0.1)
    t.start()
    threads.append(t)
    time.sleep(0.1)

# Join threads
for t in threads:
    t.join()

# Write json file
with open('data.json', 'w') as file:
    print('\nWrite json file...')
    file.write(json.dumps(global_vars.RESULT, indent=4, sort_keys=True))
    file.close()
