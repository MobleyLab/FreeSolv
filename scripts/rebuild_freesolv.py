#!/usr/bin/env python
"""
Use the openmoltools wrappers of OpenEye and Antechamber to rebuild input files
for the FreeSolv database.

Looks for freesolve database using environment variable FREESOLV_PATH
Outputs two LOCAL directories of files: ./tripos_mol2/ and ./mol2files_gaff/
"""
import os
import openmoltools
import pickle
import shutil
import sys
import solvationtoolkit.mol2tosdf as mol2tosdf

FREESOLV_PATH = "../database.pickle"
database = pickle.load(open(FREESOLV_PATH))

def make_path(filename):
    try:
        path = os.path.split(filename)[0]
        os.makedirs(path)
    except OSError:
        pass

for (key, entry) in database.items():
    print "Processing molecule %s ..." % (key)
    tripos_filename = os.path.join('../mol2files_sybyl/', key + '.mol2')
    frcmod_filename = os.path.join("../amber/", "%s.frcmod" % key)
    gaff_mol2_filename = os.path.join("../mol2files_gaff/", "%s.mol2" % key)
    prmtop_filename = os.path.join("../amber/", "%s.prmtop" % key)
    inpcrd_filename = os.path.join("../amber/", "%s.inpcrd" % key)
    sdf_filename = os.path.join("../sdffiles/", "%s.sdf" % key)
    gro_filename = os.path.join("../gromacs_original/", "%s.gro" % key)
    top_filename = os.path.join("../gromacs_original/", "%s.top" % key)
    gro_solv_filename = os.path.join("../gromacs_solvated/", "%s.gro" % key)
    top_solv_filename = os.path.join("../gromacs_solvated/", "%s.top" % key)

    #Add output directories if not already present
    make_path( '../mol2files_sybyl/' )
    make_path( '../mol2files_gaff/')
    make_path( '../sdffiles/')
    make_path( '../gromacs_original/')
    make_path( '../gromacs_solvated/')
    make_path( '../amber/')

    molecule = openmoltools.openeye.smiles_to_oemol(entry['smiles'])
    charged = openmoltools.openeye.get_charges(molecule)
    openmoltools.openeye.molecule_to_mol2(charged, tripos_filename)
    mol2tosdf.writeSDF(gaff_mol2_filename, sdf_filename, key)

    _, _ = openmoltools.utils.run_antechamber(key, tripos_filename, charge_method=None, gaff_mol2_filename=gaff_mol2_filename, frcmod_filename=frcmod_filename)
    openmoltools.utils.run_tleap(key, gaff_mol2_filename, frcmod_filename, prmtop_filename=prmtop_filename, inpcrd_filename=inpcrd_filename)
    openmoltools.utils.convert_via_acpype( key, prmtop_filename, inpcrd_filename, out_top = top_filename, out_gro = gro_filename)
    openmoltools.gromacs.do_solvate(top_filename, gro_filename, top_solv_filename, gro_solv_filename, water_top='tip3p.itp', box_dim=1.5, box_type='cubic', water_model='spc216.gro')

