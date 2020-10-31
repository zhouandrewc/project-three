# Processing Data

Since much of the data from PSID are in a format that pandas can't directly read, I used [hanjae112](https://github.com/hanjae1122)'s [PSID ASCII reader](https://github.com/hanjae1122/PSID) to process it. I made slight changes to the code.

The PSID site may be found at https://psidonline.isr.umich.edu/.

This directory should hold folders with ```.sps``` and ```.txt``` files in them, downloaded from PSID's [packaged data](https://simba.isr.umich.edu/data/PackagedData.aspx) releases. The ```.sps``` indicates the format of the ```.txt```, and ```ascii_reader.py``` uses these format files to properly read the data into a CSV.

```main.py``` calls this CSV conversion functionality on every ```.sps``` and ```.txt``` file located in a folder in the directory, so downloading the zipped files from PSID and unzipping them in this directory will suffice.

The specific files used were: the 2001 PSID Family Survey, the 2017 release of the Individual Survey (containing all information from all individual surveys), the 2002 Childhood Development Supplement (CDS) child interview, the 2002 CDS primary caregiver (PCG) interview, the 2002 CDS test score assessment, the 2002 CDS demographic survey data, the 2017 Transition into Adulthood Supplement, and the Childhood and Adoption History data from 1985-2017.

Several dozen variables from these various surveys are combined together in our data cleaning and storage routine in order to synthesize the final dataset. Note that ```mod_vars_clean.txt``` contains a list of the variables necessary, which is used in our SQL processing notebook to grab only the necessary datafields from these tables to put into our SQL database.