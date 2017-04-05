# Automated conversion of files and vaidation of the conversion

# Manifest
- `README.md`: this file
- `grompp_freesolv.mdp`: simulation input file for computing vacuum GROMACS energies
- `min_freesolv.in`: simulation input file for computing LAMMPS energies
- `onepoint_freesolv.cfg`: simulation input file for computing DESMOND energies
- `energy_comparison_info.txt`: output of automated energy conversion.

# Conversion Details:

Program versions used were
   - GROMACS: GROMACS 5.1.2
   - sander: Version 16.0
   - lammps: release date 16 Feb 2016
   - desmond: schrodinger2016-1
   - charmm: Developmental Version 40b2   February 15, 2016 

In the following description, the files are
   - GROMACS_PATH = path to the bin/ directory gromacs is installed in
   - AMBER_PATH = the location of the sander executable
   - LAMMPS_PATH = the location of the lammps executable
   - CHARMM_PATH = the location of the charmm executable
   - mobley_XXXXXX = input file, with number indicated by XXXXXX

Files were converted with the python module `intermol`. The intermol
version was https://github.com/shirtsgroup/InterMol, freesolv branch,
commit 4fd307e updated 3/28/2017.  The addition module `ParmEd`
https://github.com/ParmEd/ParmEd is a dependency of InterMol for
conversion from and to AMBER and CHARMM format files. 

For all but two systems, tagged version 2.73 of ParmEd was used.  For
these two systems (6733657 and 3727287), a bug-fixed version (git
commit `e05e32a`, 3/29/2017, after pull request #857) was used. For
system 6733657, the charmm `.rtf` file was manually edited to give a
valid CHARMM file. The `energy_comparison_info.txt` was manually
edited to add these energies.

The command for conversion was was:

```
    python convert.py --odir mobley_XXXXX
               --gromacs --charmm --lammps --desmond --amber --energy --amb_in mobley_XXXXX.prmtop mobley_XXXX.inpcrd
               --inefile ./min_freesolv.in
               --gropath GROMACS_PATH
               --amberpath AMBER_PATH
               --lmppath LAMMPS_PATH
               --charmmpath CHARMM_PATH
               -gs ./grompp_freesolv.mdp
               -ds ./onepoint_freesolv.cfg
               -as ./min_freesolv.in
               -ls pair_style lj/cut/coul/cut 30.0 30.0\npair_modify tail no\n\n
               -cs nbonds ips elec vdw cutnb 50 ctofnb 49.99 noewald
```

where `convert.py` refers to the relevant InterMol utility. 

# Energy file conversion description

This file contains (somewhat filtered) version of the output from
`convert.py`.  Some notes about both the output and the energy
comparison:

- For each system, the file consists of run conversion logging
  information from `intermol.py`, and a summary of differences in
  energy groups. Because of the way that energies are reported
  differently in each program, the InterMol output is divided into a
  'Not comparable energies' section, where terms that do not have
  matches between different programs are listed, and 'Comparable
  energy terms', which ARE found in all programs being compared. The
  'headline' number is located at the end, in the 'total potential
  energy comparison' section, where differences in potential energies
  between the input and all output programs are given. Differences are
  generally of the magnitude seen in a previous study, Shirts, M.R.,
  Klein, C., Swails, J.M. et al. J Comput Aided Mol Des (2016),
  doi:[10.1007/s10822-016-9977-1](http://dx.doi.org/10.1007/s10822-016-9977-1),
  with exceptions noted below.

- Conversions in InterMol are done from AMBER to GROMACS, and then to
  a variety of file formats. For a number of files, once the AMBER
  fields are converted into GROMACS, the functional form of the
  dihedrals in the GROMACS files cannot be read back into AMBER,
  resulting in the error 'AmberParm does not support all of the
  parameters defined in the input Structure'. This means that there is
  no direct comparison of amber<=>amber conversion, but since only the
  original AMBER files are distributed, these files are not needed.

- There are some moderate differences in angle energies for a number
  of files that have angles that are nearly 180 degrees, of magnitude 0.1 to
  0.2 kJ/mol, which is about 100x larger than the typical discrepancy
  between energies.  This is not an artifact of the conversion
  process, but appears to because of differences in the way that AMBER
  computes angle energies near 180 degrees.  In this dataset, the systems are:
    - mobley_8522124 oct-1-yne
    - mobley_1674094 hex-1-yne
    - mobley_2123854 4-hydroxybenzonitrile
    - mobley_2451097 benzonitrile
    - mobley_430089 pent-1-yne
    - mobley_49274 hept-1-yne
    - mobley_5026370 pyridine-4-carbonitrile
    - mobley_8260524 prop-1-yne
    - mobley_8522124 oct-1-yne
    - mobley_8764620 pyridine-3-carbonitrile
    - mobley_9121449 but-1-yne
    - mobley_9740891 2,6-dichlorobenzonitrile

- charmm files frequently have moderate differences, due essentially
  entirely to the way that nonbonded energies are evaluated in an
  isolated system in vacuum.  Inspection of the results will show that
  the sometimes moderate sized differences (in the 0.1 of kJ/mol) are
  in the nonbonded terms only, and these differences will be
  irrelevant in a solvated system that uses different long range
  summation files.
