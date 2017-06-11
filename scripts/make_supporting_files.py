#!/bin/env python

import pickle
import utils
file = open('../database.pickle', 'rb')
database = pickle.load(file, encoding='latin1')
file.close()

utils.convert_to_json('../database.pickle', '../database.json')

#Put it in a nice table for easy parsing. Use semicolons to separate fields, making sure each individual field doesn't contain any semicolons since this would break parsing.

outtext = ["#Hydration free energy datbase v0.52, 6/11/17.\n"]
outtext += ["#Semicolon-delimited text file with fields in the following format:\n"]
outtext += ["# compound id (and file prefix); SMILES; iupac name (or alternative if IUPAC is unavailable or not parseable by OEChem); experimental value (kcal/mol); experimental uncertainty (kcal/mol); Mobley group calculated value (GAFF) (kcal/mol); calculated uncertainty (kcal/mol); experimental reference (original or paper this value was taken from); calculated reference; text notes.\n"]

cids = list(database.keys())
cids.sort()
for cid in cids:
    notes = ''
    for line in database[cid]['notes']:
        if not '\n' in line: line += '  '
        notes+= line.replace('\n','  ') #Remove line breaks as they will break format here

    if ';' in notes: #Make sure no semicolon in notes
        #Fix issue where I used a semicolon
        notes = notes.replace('not presently available;', 'not presently available, so')
        if ';' in notes:
            print("ERROR: For %s, note contains ;. The note is:" % cid, notes)
    if ';' in database[cid]['expt_reference']:
        print("ERROR: For %s, experimental reference contains ;. The reference is:" % cid, database[cid]['expt_reference'])

    if ';' in database[cid]['calc_reference']:
        print("ERROR: For %s, calculation reference contains ;. The reference is:" % cid, database[cid]['calc_reference'])

    #Compose line
    entry = database[cid]
    line = '%s; %s; %s; %.2f; %.2f; %.2f; %.2f; %s; %s; %s\n' % (cid, entry['smiles'], entry['iupac'], entry['expt'], entry['d_expt'], entry['calc'], entry['d_calc'], entry['expt_reference'], entry['calc_reference'], notes )
    outtext.append(line)

file = open('../database.txt', 'w')
file.writelines(outtext)
file.close()


# Store functional group descriptions by compound code and name to text files
file = open('../groups.txt', 'w')
file.write('cid; \t iupac; \t groups (semicolon delimited);\n')
for cid in cids:
    line = '%s; \t %s \t' % (cid, database[cid]['iupac'] )
    for gname in database[cid]['groups']:
        line += '; %s' % gname
    line+='\n'
    file.write(line)
file.close()


# Generate and store smiles_to_cid and iupac_to_cid in pickle and json
smiles_to_cid = {}
iupac_to_cid = {}
for cid in cids:
    smiles_to_cid[ database[cid]['smiles']] = cid
    iupac_to_cid[ database[cid]['iupac']] = cid

file = open('../smiles_to_cid.pickle', 'wb')
pickle.dump(smiles_to_cid, file)
file.close()

file = open('../iupac_to_cid.pickle', 'wb')
pickle.dump(iupac_to_cid, file)
file.close()

utils.convert_to_json('../smiles_to_cid.pickle', '../smiles_to_cid.json')
utils.convert_to_json('../iupac_to_cid.pickle', '../iupac_to_cid.json')

