#!/usr/bin/python

"""
    @author: Eduardo Maia Machado
"""

HOST = ''
N_THREADS = 64
RANGE = 0.01
MAX_REQUESTS = 1000
TEST_TYPE = 'sequential'
SPAWN_TIME = 1

CURRENT_REQUEST = 0
CURRENT_RESPONSE = 0
CURRENT_SPAWN = 0
SPAWNED_THREADS = 0
RESULT = {}
