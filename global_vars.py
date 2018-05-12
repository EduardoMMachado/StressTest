#!/usr/bin/python

"""
    @author: Eduardo Maia Machado
"""

HOST = 'http://35.196.226.41/list'
N_THREADS = 64
RANGE = 0.01
MAX_REQUESTS = 1000
TEST_TYPE = 'sequential'

CURRENT_REQUEST = 0
EXIT = False
RESULT = {}
