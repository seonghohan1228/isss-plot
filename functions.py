import os
import h5py
import numpy as np
import pandas as pd
from constants import *


# Finding filepaths with corresponding orbit number
def find_filepath(orbit_no, data_folder, keyword1, keyword2):
    files = os.listdir(data_folder)
    fp1, fp2 = None, None
    # Convert orbit number to 5 digit format
    orbit_no = str(orbit_no)
    while(len(orbit_no) != 5):
        orbit_no = '0' + orbit_no
    # Find filepaths with corresponding orbit number
    for f in files:
        if f[27:32] == orbit_no:
            if f[0:4] == keyword1:
                fp1 = f'{data_folder}/{f}'
            elif f[0:4] == keyword2:
                fp2 = f'{data_folder}/{f}'
    # Check if file wasn't found
    if fp1 is None and fp2 is None:
        print('Files not found')
        quit()
    elif fp1 is None:
        print(f'{keyword1} file not found')
        quit()
    elif fp2 is None:
        print(f'{keyword2} file not found')
        quit()
    return [fp1, fp2]


# Printing group structure of HDF file that has 2 layers of groups
def tree(group1, group2):
    print('File structure')
    for g1 in group1:
        print(f' -- {g1}')
        for g2 in group2:
            print(f'   -- {g2}')


# Reading hdf file data
def read_hdf(orbit_no, data_folder, show_tree):
    filepaths = find_filepath(orbit_no, data_folder, 'HEPD', 'MEPD')
    hepd_data, mepd_data = [], []
    for fp in filepaths:
        with h5py.File(fp) as f:
            print(f'Opening {fp}')
            # Storing groups
            group1 = np.array(list(f.keys()))
            group2 = np.array([])
            for group in group1:
                group2 = np.append(group2, list(f.get(group)))
            # Show file structure
            if show_tree == True:
                tree(group1, group2)
            data_index = np.array(f.get(f'{group1[0]}/{group2[0]}'))
            # Read and store data as a pandas dataframe
            if 'HEPD' in fp:
                for i in range(2, 4):
                    df_col = np.array(f.get(f'{group1[0]}/{group2[2*i]}'))
                    df_data = np.array(f.get(f'{group1[0]}/{group2[2*i+1]}'))
                    hepd_data.append(pd.DataFrame(df_data, 
                                    index=range(len(df_data)), columns=df_col))
            elif 'MEPD' in fp:
                for i in range(2, 4):
                    df_col = np.array(f.get(f'{group1[0]}/{group2[2*i]}'))
                    df_data = np.array(f.get(f'{group1[0]}/{group2[2*i+1]}'))
                    mepd_data.append(pd.DataFrame(df_data, 
                                    index=range(len(df_data)), columns=df_col))
        print(f'Closed {fp}')
    return hepd_data, mepd_data
    

