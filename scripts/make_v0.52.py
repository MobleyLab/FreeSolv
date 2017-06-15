#!/bin/env python

"""This will update the current v0.51 database to v0.52 to reflect the following changes:
- Update DOI for all calculated values to 2017 J Chem Eng Data paper associated with v0.51 (10.1021/acs.jced.7b00104)
- Remove duplicate compound mobley_4689084, which was a SAMPL1 compound that was already present in the earlier "504 molecule" set with the same experimental value and therefore duplicates mobley_352111. In SAMPL1 it was referred to as "ethylene glycol diacetate" and originally it was 1,2-diacetoxyethane in the Mobley and earlier Rizzo sets. Apparently when Guthrie and OpenEye were curating SAMPL1, they did not notice that this compound was already present in public datasets, and somehow I missed it when checking SMILES strings in the database for duplicates.
- Now takes advantage of new functionality added to utils.py to check database for duplicates prior to export by creating new SMILES strings for each from the database SMILES and cross-check.
"""

# Load database
import pickle
import utils
file = open('../database.pickle', 'rb')
database = pickle.load(file, encoding='latin1')
file.close()

# Remove mobley_4689084
database.pop('mobley_4689084')

# Update DOI for calculated values
for cid in database:
    database[cid]['calc_reference'] = '10.1021/acs.jced.7b00104'

# Check for duplicates
num_dupes, keypairs = utils.check_for_duplicates( database )
if num_dupes > 0:
    raise Exception("Error: %s duplicates found." % num_dupes)

# Write out database
file = open('../database.pickle', 'wb')
pickle.dump(database, file)
file.close()

# Update supporting files
import os
os.system('python make_supporting_files.py')
