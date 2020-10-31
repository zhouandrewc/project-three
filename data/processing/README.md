# Processing Data

Since much of the data from PSID are in a format that pandas can't directly read, I used [hanjae112](https://github.com/hanjae1122)'s [PSID ASCII reader](https://github.com/hanjae1122/PSID) to process it. I made slight changes to the code.

The PSID site may be found at https://psidonline.isr.umich.edu/.

This directory should hold folders with ```.sps``` and ```.txt``` files in them, downloaded from PSID's [packaged data](https://simba.isr.umich.edu/data/PackagedData.aspx) releases. The ```.sps``` indicates the format of the ```.txt```, and ```ascii_reader.py``` uses these format files to properly read the data into a CSV.

```main.py``` calls this CSV conversion functionality on every ```.sps``` and ```.txt``` file located in a folder in the directory, so downloading the zipped files from PSID and unzipping them in this directory will suffice.

The specific files used were: the 2001 PSID Family Survey, the 2017 release of the Individual Survey (containing all information from all individual surveys), the 2002 Childhood Development Supplement (CDS) child interview, the 2002 CDS primary caregiver (PCG) interview, the 2002 CDS test score assessment, the 2002 CDS demographic survey data, the 2017 Transition into Adulthood Supplement, and the Childhood and Adoption History data from 1985-2017.

Several dozen variables from these various surveys are combined together in our data cleaning and storage routine in order to synthesize the final dataset. Note that ```variables_to_extract.txt``` contains a list of the variables necessary, which is used in our SQL processing notebook to grab only the necessary datafields from these tables to put into our SQL database.

The folder [wlth2001](wlth2001) is included to demonstrate the proper structure. The example [SPS File](wlth2001/WLTH2001_example.sps) is the original ```.sps``` file, but ```WLTH2001_example.txt``` is left blank as the original would be excessively large.

# Detailed Workflow

Below is a detailed workflow explaining how to acquire and process the data used for this project.

* Download [packaged datasets](https://simba.isr.umich.edu/data/PackagedData.aspx) as ```.zip``` files from PSID

Specific files used are: the 2001 Family Survey, the 2001 Family Wealth Survey, the Individual Survey (2017 Release), the 2002 Child Development Supplement, the 2017 Transition into Adulthood Supplement, and the Childhood and Adoption History File (2017 Release).

These data were downloaded in the SPS fixed file format and are designed for the [SPSS program](https://www.ibm.com/products/spss-statistics). The data for each survey are stored in a ```.txt.``` file, with a ```.sps``` format file indicating how to read in the raw data. Unfortunately pandas does not support directly reading files of this format as its ```read_spss``` function cannot read this specific SPSS format.

* Store these ```.zip``` files in [```data/processing```](data/processing), unzip each to an individual folder, and run [```main.py```](data/processing/main.py). ```main.py``` will look in all subdirectories for paired ```.sps``` and ```txt``` files, convert them to csv, and store them in the [```data/csv```](data/csv) directory.

* Use the notebook ```1_sql_logic.ipynb``` to read in these ```.csv``` files. This routine will consult ```variables_to_extract.txt``` to find and rename our variables of interest, then store them in a PostgreSQL database. The database location is hardcoded as '''localhost:5432/psid''' and may be changed by the user.

* The notebook ```2_prep_data.ipybn``` queries the SQL database and merges all our data of interest into a single dataframe, stored as [```data.csv```][data/data.csv] in our ```data/``` folder.