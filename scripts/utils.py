"""
Shared utilities.

"""

#import cPickle as pickle
import pickle
from openeye.oechem import *

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

def check_for_duplicates( database_contents ):
    """Take contents of database and re-generate all SMILES, checking for duplicates.

    Parameters:
    ----------
    database_contents : dict
        dictionary of FreeSolv database, keyed by compound ID

    Returns:
    ----------
    num_dupes : int
        Number of duplicated compound pairs found
    keypairs : list
        List containing tuples of pairs corresponding to the compound IDs of the duplicates
    """

    # Pull compound IDs
    cids = [ item for item in database_contents ]

    # Generate new OEMols from SMILES
    oemols = []
    for cid in cids:
        mol = OEMol()
        OEParseSmiles(mol, database_contents[cid]['smiles'])
        oemols.append(mol)

    # Generate new SMILES from OEMols, thereby standardizing
    smiles = []
    for mol in oemols:
        smiles.append(OEMolToSmiles(mol))

    # Build duplicate info
    clean_smiles = []
    keypairs = []
    for idx,cid in enumerate(cids):
        smi = smiles[idx]
        if smi not in clean_smiles:
            clean_smiles.append(smi)
        else:
            dupe_idx = smiles.index(smi)
            keypairs.append( (cids[dupe_idx], cid) )

    return len(keypairs), keypairs

