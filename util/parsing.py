'''
# Parses a file (data/processing/variables_to_extract.txt) in order to
# determine which data we should select when we read the .csv files in order to
# later store them in our SQL database. Many of the dataframes have thousands
# of variables and would not be storable in their entirety.
#
# Andrew Zhou
'''

def get_variables(file):

    tables = {}

    with open(file, 'r') as f:
        current_table = None

        for line in f:
            if line.startswith("TABLE"):
                current_table = line.strip().split(" ")[1]
                sql_name = line.strip().split(" ")[2]
                tables[current_table] = {"sql_name": sql_name,
                                        "variables": {}}
            elif not line.startswith("#"):
                if line.strip():
                    code, name = line.strip().split(": ")
                    tables[current_table]["variables"][code] = name
    return tables