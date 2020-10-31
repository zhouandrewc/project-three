# Read all .sps formatting headers in all folders in the directory,
# then use ascii_reader to convert them to .csv

from ascii_reader import ascii_
import os

dir_list = []
sps_file_list = []

for root, dirs, _ in os.walk(os.getcwd(), topdown=False):
    for folder in dirs:
        dir_list.append(folder)
        files = [i[:-4] for i in os.listdir(os.getcwd() + "/" + folder) if i.endswith(".sps")]
        sps_file_list.append(files)

for folder, sps_files in zip(dir_list, sps_file_list):
    for sps_file in sps_files:
        try:
            reader = ascii_(folder, sps_file)
            inds, headers, lab2format, lab2name, name2lab = reader.read_index_file()
            reader.read_data_file(inds, headers, lab2format)
        except Exception as e:
            print("error:", e)
