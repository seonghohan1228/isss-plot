import os
import sys
import h5py
import aacgmv2
import spacepy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import spacepy.coordinates as coord
import isss_plot_functions as ipf
from mpl_toolkits.basemap import Basemap

KEYWORD1 = 'HEPD'
KEYWORD2 = 'MEPD'



# Finding filepaths with corresponding orbit number
def find_filepaths(orbit_no, data_folder='./isss_data/', keyword1=KEYWORD1, keyword2=KEYWORD2):
    files = os.listdir(data_folder)
    fp1, fp2 = None, None
    # Convert orbit number to 5 digit format
    if len(str(orbit_no)) > 5:
        print('Error: Orbit number must be 5 digits or less')
        exit()
    orbit_no = '0' * (5 - len(str(orbit_no))) + str(orbit_no)
    # Find filepaths with corresponding orbit number
    for f in files:
        if f[27:32] == orbit_no:
            if f[0:4] == keyword1:
                fp1 = f'{data_folder}/{f}'
            elif f[0:4] == keyword2:
                fp2 = f'{data_folder}/{f}'
    # Check for missing file (or files)
    if fp1:
        if fp2:
            return [fp1, fp2]
        else:
            print(f'Error: {keyword2} file not found\nCheck for file')
    else:
        if fp2:
            print(f'Error: {keyword1} file not found\nCheck for file')
        else:
            print('Error: Files not found\nCheck orbit number')
    quit()


# Printing group structure of HDF file that has 2 layers of groups
def tree(groups, datasets):
    print('File structure')
    for g in groups:
        print(f' -- {g}')
        for ds in datasets:
            print(f'   -- {ds}')


# Reading hdf file data from filepaths and returning HEPD and MEPD data as list
# Can show filetree if show_tree is given True (False as default)
def read_hdf(filepaths, show_tree=False):
    hepd_data, mepd_data = [], []
    for fp in filepaths:
        with h5py.File(fp) as f:
            print(f'Opening {fp}')
            # Storing groups and datasets
            groups = np.array(list(f.keys()))
            datasets = np.array([])
            for group in groups:
                datasets = np.append(datasets, list(f.get(group)))
            # Show file structure
            if show_tree == True:
                tree(groups, datasets)
            #data_index = np.array(f.get(f'{groups[0]}/{datasets[0]}'))
            # Read and store data as a pandas dataframe
            if KEYWORD1 in fp:
                for i in range(2, 4):
                    df_col = np.array(f.get(f'{groups[0]}/{datasets[2*i]}'))
                    df_data = np.array(f.get(f'{groups[0]}/{datasets[2*i+1]}'))
                    hepd_data.append(pd.DataFrame(df_data, index=range(len(df_data)), columns=df_col))
            elif KEYWORD2 in fp:
                for i in range(2, 4):
                    df_col = np.array(f.get(f'{groups[0]}/{datasets[2*i]}'))
                    df_data = np.array(f.get(f'{groups[0]}/{datasets[2*i+1]}'))
                    mepd_data.append(pd.DataFrame(df_data, index=range(len(df_data)), columns=df_col))
        print(f'Closed {fp}')
    return [hepd_data, mepd_data]


# Find data from hdf data using keywords
def find_data(data, dataset_no, index):
    return data[dataset_no].loc[:, bytes(index, 'utf-8')]


# Plotting combined plots
def graph_plot(isss_data, orbit_no, plot_folder='./plot', plot_name='plot.png', 
            pc1_bool=True,
            pos_bool=True,
            geomag_bool=True,
            mag_bool=True):
    print('Creating plot ...')
    # Create figure
    fig = plt.figure(constrained_layout=True, figsize=(12, 15))
    fig.suptitle(f'Orbit: {orbit_no} Date: ')
    subfigs = fig.subfigures(1, 2, wspace=0.05)
    subfigsnest0 = subfigs[0].subfigures(3, 1, height_ratios=[2, 3.5, 5.5])

    # Plot subplots
    # PC1 plot
    pc1, time = isss_data.pc1, isss_data.time
    axes0 = subfigsnest0[0].subplots(1, 2)
    if pc1_bool:
        ipf.plot_pc1(pc1, time, axes0)
    
    # Position plot
    position = isss_data.position
    axes1 = subfigsnest0[1].subplots()
    if pos_bool:
        ipf.plot_position(position, axes1)
        # Geomagnetic latitude plot
        if geomag_bool:
            ipf.plot_geomag(position[2], time[0][0], map)

    # Magnetic field plot
    magnetic = isss_data.magnetic
    axes2 = subfigsnest0[2].subplots(2, 1, gridspec_kw={'height_ratios': [2.5, 3]})
    if mag_bool:
        ipf.plot_mag(magnetic, time, axes2[0])
    
    # Telescope
    telescope = isss_data.telescope
    ipf.plot_tel(telescope, axes2[1])

    print('Plot completed')

    # Save figure
    plt.savefig(f'{plot_folder}/{plot_name}', dpi=200)
    print(f'Saved plot to {plot_folder}/{plot_name}')

