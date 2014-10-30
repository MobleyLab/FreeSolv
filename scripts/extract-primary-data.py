"""
Extract the primary data from the original database pickle file.

Primary data is defined as:

- canonical isomeric SMILES all match
- experimental data:
  + experimental value
  + experiemntal uncertainty
  + citation for experimental data
- notes field
- nickname field

Example entry:
{'smiles': 'CCc1cccc2c1cccc2', 'expt_reference': '10.1021/ct050097l', 'd_calc': 0.03, 'notes': ['Experimental uncertainty not presently available, so assigned a default value.'], 'iupac': '1-ethylnaphthalene', 'PubChemID': 14315, 'd_expt': 0.6, 'expt': -2.4, 'groups': ['aromatic'], 'calc': -3.0, 'nickname': ' 1-ethylnaphthalene', 'calc_reference': '10.1021/ct800409d'}


"""

import cPickle as pickle

# Components that constitute primary data.
primary_data_components = ['smiles', 'expt_reference', 'expt', 'd_expt', 'notes', 'nickname']

if __name__ == '__main__':
    # Extract primary data from original database pickle file.
    original_database_filename = 'database.pickle'
    with open(original_database_filename, 'r') as database_file:
        database = pickle.load(database_file)

    # Extract primary data.
    for key in database.keys():
        entry = database[key]
        # Build new primary database entry with only primary data.
        primary_database_entry = dict()
        for k in primary_data_components:
            primary_database_entry[k] = entry[k]
        # Store it.
            database[key] = primary_database_entry

    # Write primary data.
    primary_database_filename = 'primary-data/primary-data.pickle'
    with open(primary_database_filename, 'w') as primary_database_file:
        pickle.dump(database, primary_database_file)
