"""
Shared utilities.

"""

#import cPickle as pickle
import pickle

def read_database():
    """Read the database from a pickle file and return it"""
    database_filename = 'database.pickle'
    with open(database_filename, 'rb') as database_file:
        database = pickle.load(database_file, encoding='latin1')
    return database


import pickle
import json

def convert_to_json( database_pickle, database_json):
    """Convert a pickle version of the database to json format."""
    freeSolv = pickle.load(open(database_pickle, 'rb'), encoding='latin1')

    with open(database_json,"w", encoding='utf-8') as fs:
        json.dump(freeSolv,fs)
