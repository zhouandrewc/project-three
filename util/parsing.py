'''
# Parses a file (generally data/processing/mod_vars_clean.txt) in order to
# determine which data we should select when we read the .csv files in order to
# later store them in our SQL database. Many of the dataframes have thousands
# of variables and would not be storable in their entirety.
#
# Andrew Zhou
'''

def get_variables(file):

    tables = {}

    with open(file, 'r') as f:
        current_table_path = None

        for line in f:
            if line.startswith("TABLE"):
                current_table_path = "data/processing/" + line.strip().split(" ")[1]
                tables[current_table_path] = {}
            else:
                if line.strip():
                    code, name = line.strip().split(": ")
                    tables[current_table_path][code] = name
    return tables