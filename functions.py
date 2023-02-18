# functions.py

import os
import h5py
import numpy as np
from constants import *

# Finding filepaths with corresponding orbit number
def find_filepath(orbit_no, keyword1, keyword2):
    files = os.listdir(DATAPATH)
    fp1 = ''
    fp2 = ''
    # Convert orbit number to 5 digit format
    orbit_no = str(orbit_no)
    while(len(orbit_no) != 5):
        orbit_no = '0' + orbit_no
    # Find filepaths with corresponding orbit number
    for f in files:
        if f[27:32] == orbit_no:
            if f[0:4] == keyword1:
                fp1 = DATAPATH + f
            elif f[0:4] == keyword2:
                fp2 = DATAPATH + f
    # Check if file wasn't found
    if fp1 == '' and fp2 == '':
        print('Files not found')
    elif fp1 == '':
        print(keyword1 + 'file not found')
    else:
        print(keyword2 + 'file not found')
    return [fp1, fp2]


# Printing group structure of HDF file that has 2 layers of groups
def tree(group1, group2):
    print('File structure')
    for g1 in group1:
        print(' -- ' + g1)
        for g2 in group2:
            print('   -- ' + g2)


# Reading hdf file data
def read_hdf(orbit_no, show_tree):
    filepaths = find_filepath(orbit_no, 'HEPD', 'MEPD')
    dataset = np.array([])
    for fp in filepaths:
        with h5py.File(fp) as f:
            print('Opening ' + fp)
            # Storing groups
            group1 = np.array(list(f.keys()))
            group2 = np.array([])
            for group in group1:
                group2 = np.append(group2, list(f.get(group)))
            # Show file structure
            if show_tree == True:
                tree(group1, group2)
            # Read data
            for g1 in group1:
                for g2 in group2:
                    data =  f.get(g1 + '/' + g2)
                    dataset = np.append(dataset, data)
        print('Closed ' + fp)
    return dataset

