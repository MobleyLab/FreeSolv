# `OrionDB.ipynb`

iPython notebook that illustrates how to concatenate multiple mol2 files into a single `OEMol` object.
Associated with each mol2 file is a dictionary containing some data, parsed from a JSON file.
Each field from the database (key from dictionary) is used as a tag identifier for attaching the associated database information (values from dictionary). Alternatively, one can attach the entire database associated with each molecule as a single object. The concatenated `OEMol` is then written to a compressed `freesolv.oeb.gz` file.

###### Data here is attached as [Generic Data](https://docs.eyesopen.com/toolkits/python/oechemtk/genericdata.html) and not as [SD Tagged Data](https://docs.eyesopen.com/toolkits/python/oechemtk/moltaggeddata.html#section-moltaggeddata-sd).
