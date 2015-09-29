#!/bin/env python

"""Make edits to database for v0.32 release - specifically, fixing some issues relating to two nitro compounds which had incorrect SMILES."""

#Load database
import pickle
file = open('../database.pickle', 'r')
database = pickle.load(file)
file.close()

#Fix SMILES for mobley_3802803
database['mobley_3802803']['smiles'] = 'CCCCCCO[N+](=O)[O-]'

#Fix SMILES for mobley_9741965
database['mobley_9741965']['smiles'] = 'CC(CCO[N+](=O)[O-])O[N+](=O)[O-]'


#Get checkmol descriptors and store
import openmoltools.utils
descriptors = openmoltools.utils.get_checkmol_descriptors('../tripos_mol2/mobley_3802803.mol2')[0]
database['mobley_3802803']['groups'] = descriptors

descriptors = openmoltools.utils.get_checkmol_descriptors('../tripos_mol2/mobley_9741965.mol2')[0]
database['mobley_9741965']['groups'] = descriptors


#Store updated database
file = open('../database.pickle', 'w')
pickle.dump(database, file)
file.close()

