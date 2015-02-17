"""
Generate Tripos mol2 files with AM1-BCC charges from canonical isomeric SMILES strings.

Molecules will be named after database key.

"""

import os

from openeye import oechem
from openeye import oeiupac
from openeye import oeomega
from openeye import oequacpac

import utils

def generate_molecule_from_smiles(smiles, name=None):
    """
    Parameters
    ----------
    smiles : str
       The canonical isomeric SMILES string.
    name : str, optional, default=None
       If specified, the molecule title will be set to this; if not, the IUPAC name will be assigned.

    """

    # Generate a molecule from canonical isomeric SMILES.
    molecule = oechem.OEMol()
    if not oechem.OEParseSmiles(molecule, smiles):
        raise ValueError("The supplied SMILES '%s' could not be parsed." % smiles)

    # Assign aromaticity.
    oechem.OEAssignAromaticFlags(molecule, oechem.OEAroModelOpenEye)

    # Add hydrogens.
    oechem.OEAddExplicitHydrogens(molecule)

    # Set title.
    if name is None:
        # Set title to IUPAC name.
        name = oeiupac.OECreateIUPACName(molecule)
    molecule.SetTitle(name)

    # Check for any missing atom names, if found reassign all of them.
    if any([atom.GetName() == '' for atom in molecule.GetAtoms()]):
        oechem.OETriposAtomNames(molecule)

    return molecule

def assign_conformations(molecule, max_confs=None):
    """
    Generate set of expanded conformations.

    Parameters
    ----------
    molecule : openeye.oechem.OEMol
       The molecule to be assigned conformations (will be modified).
    max_confs : int, optional, default=None
       If specified, will limit number of conformations generated.

    """

    omega = oeomega.OEOmega()
    strictStereo = True # maintain strict stereochemistry
    omega.SetStrictStereo(strictStereo)
    omega.SetIncludeInput(False)  # don't include input
    if max_confs is not None:
        omega.SetMaxConfs(max_confs)
    omega(molecule)  # generate conformation
    return

def assign_charges(molecule):
    """
    Assign AM1-BCC charges using recommended scheme from Christopher Bayly.

    Parameters
    ----------
    molecule : openeye.oechem.OEMol
       The molecule to be assigned conformations (will be modified).

    """
    oequacpac.OEAssignPartialCharges(molecule, oequacpac.OECharges_AM1BCCSym)  # AM1BCCSym recommended by Chris Bayly to KAB+JDC, Oct. 20 2014.
    return

def write_tripos_mol2(molecule, filename, substructure_name='MOL', nconfs=None):
    """
    Write the molecule as a Tripos mol2 file.

    Parameters
    ----------
    molecule : openeye.oechem.OEMol
       The molecule to be written.
    filename : str
       The file to write to.
    substructure_name : str, optional, default='MOL'
       The name of the substructure to write.
    nconfs : int, optional, default=None
       The number of conformers to write.

    """

    # Avoid changing molecule by making a deep copy.
    molecule = oechem.OEMol(molecule)

    # Select number of conformers to write.
    if nconfs is None: nconfs = molecule.GetConfs()

    # Write the molecule in Tripos mol2 format.
    ofs = oechem.oemolostream(filename)
    ofs.SetFormat(oechem.OEFormat_MOL2H)
    for k, mol in enumerate(molecule.GetConfs()):
        if (k < nconfs):
            oechem.OEWriteMolecule(ofs, mol)
    ofs.close()

    # Replace <0> substructure names with valid text.
    if substructure_name:
        infile = open(filename, 'r')
        lines = infile.readlines()
        infile.close()
        newlines = [line.replace('<0>', substructure_name) for line in lines]
        outfile = open(filename, 'w')
        outfile.writelines(newlines)
        outfile.close()

    return

if __name__ == '__main__':
    # Read database.
    database = utils.read_database()

    # Process molecules.
    for (key, entry) in database.iteritems():
        print "Processing molecule %s [%s]..." % (key, entry['iupac'])
        molecule = generate_molecule_from_smiles(entry['smiles'])
        assign_conformations(molecule) # assign expanded set of conformations
        assign_charges(molecule) # assign charges
        filename = os.path.join('tripos_mol2', key + '.mol2')
        write_tripos_mol2(molecule, filename, nconfs=1)

