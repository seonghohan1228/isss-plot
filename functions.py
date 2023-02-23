import os
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

KEYWORD1 = 'HEPD'
KEYWORD2 = 'MEPD'

# Finding filepaths with corresponding orbit number
def find_filepaths(orbit_no, data_folder='./isss_data/', keyword1=KEYWORD1, keyword2=KEYWORD2):
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
def tree(groups, dataset):
    print('File structure')
    for g in groups:
        print(f' -- {g}')
        for ds in dataset:
            print(f'   -- {ds}')


# Reading hdf file data
def read_hdf(filepaths, show_tree=False):
    hepd_data, mepd_data = [], []
    for fp in filepaths:
        with h5py.File(fp) as f:
            print(f'Opening {fp}')
            # Storing groups
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


def graph_plot(isss_data, orbit_no, plot_folder='./plot', plot_name='plot.png'):
    # Create figure
    fig = plt.figure(constrained_layout=True, figsize=(12, 15))
    fig.suptitle(f'Orbit: {orbit_no} Date: ')
    subfigs = fig.subfigures(1, 2, wspace=0.05)
    subfigsnest = subfigs[0].subfigures(3, 1, height_ratios=[2, 3, 5])
    axesnest = subfigsnest[0].subplots(1, 2)
    # Plot subplots
    axesnest[0].plot(isss_data.pc1[0], isss_data.time[0])
    axesnest[1].plot(isss_data.pc1[1], isss_data.time[1], color='black', marker='x', markersize=0.1, linestyle='-')
    axesnest[1].plot(isss_data.pc1[2], isss_data.time[2], color='red', marker='D', markersize=0.1, linestyle='--')
    # Save figure
    plt.savefig(f'{plot_folder}/{plot_name}', dpi=200)
    print(f'Saved plot to {plot_folder}/{plot_name}')

