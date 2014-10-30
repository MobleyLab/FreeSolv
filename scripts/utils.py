"""
Shared utilities.

"""

import cPickle as pickle

def read_database():
    database_filename = 'database.pickle'
    with open(database_filename, 'r') as database_file:
        database = pickle.load(database_file)
    return database
