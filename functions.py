import os
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

MEPD_DT_A = 3
MEPD_DT_B = 4

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
def tree(groups, dataset):
    print('File structure')
    for g in groups:
        print(f' -- {g}')
        for ds in dataset:
            print(f'   -- {ds}')


# Reading hdf file data
def read_hdf(orbit_no, data_folder='./isss_data', show_tree=False):
    filepaths = find_filepath(orbit_no, data_folder, 'HEPD', 'MEPD')
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
            data_index = np.array(f.get(f'{groups[0]}/{datasets[0]}'))
            # Read and store data as a pandas dataframe
            if 'HEPD' in fp:
                for i in range(2, 4):
                    df_col = np.array(f.get(f'{groups[0]}/{datasets[2*i]}'))
                    df_data = np.array(f.get(f'{groups[0]}/{datasets[2*i+1]}'))
                    hepd_data.append(pd.DataFrame(df_data, 
                                    index=range(len(df_data)), columns=df_col))
            elif 'MEPD' in fp:
                for i in range(2, 4):
                    df_col = np.array(f.get(f'{groups[0]}/{datasets[2*i]}'))
                    df_data = np.array(f.get(f'{groups[0]}/{datasets[2*i+1]}'))
                    mepd_data.append(pd.DataFrame(df_data, 
                                    index=range(len(df_data)), columns=df_col))
        print(f'Closed {fp}')
    return hepd_data, mepd_data


def find_data(data, dataset_no, index):
    return data[dataset_no].loc[:, bytes(index, 'utf-8')]


def graph_plot(hepd_data, mepd_data, orbit_no, plot_folder='./plot', 
            plot_name='plot.png'):
    hepd_time = find_data(hepd_data, 0, 'TIME_x')
    mepd_time = find_data(mepd_data, 0, 'TIME')
    hepd_pc1 = find_data(hepd_data, 0, 'PC1')
    mepd_pc1 = find_data(mepd_data, 0, 'PC1')
    mepd_dt = find_data(mepd_data, 0, 'DT')
    mepd_time_a, mepd_time_b, mepd_pc1_a, mepd_pc1_b = [], [], [], []
    # Find where DT in MEPD_SCI data changes to divide MEPD-A and MEPD-B
    for i in range(len(mepd_dt)):
        if mepd_dt[i] == MEPD_DT_A:
            mepd_time_a.append(mepd_time[i])
            mepd_pc1_a.append(mepd_pc1[i])
        elif mepd_dt[i] == MEPD_DT_B:
            mepd_time_b.append(mepd_time[i])
            mepd_pc1_b.append(mepd_pc1[i])

    fig = plt.figure(constrained_layout=True, figsize=(12, 15))
    fig.suptitle(f'Orbit: {orbit_no} Date: ')
    subfigs = fig.subfigures(1, 2, wspace=0.05)
    subfigsnest = subfigs[0].subfigures(3, 1, height_ratios=[2, 3, 5])
    axesnest = subfigsnest[0].subplots(1, 2)
    
    axesnest[0].plot(hepd_pc1, hepd_time)
    axesnest[1].plot(mepd_pc1_a, mepd_time_a, color='black', marker='x', 
                    markersize=0.1, linestyle='-')
    axesnest[1].plot(mepd_pc1_b, mepd_time_b, color='red', marker='D', 
                    markersize=0.1, linestyle='--')
    
    '''
    for ax in axesnest:
        pc = plt.example_plot(ax)
        '''
    '''
    fig.set_figwidth(10)
    fig.set_figheight(30)
    gs0 = plt.GridSpec(1, 2, figure=fig)
    gs00 = gs0[0].subgridspec(11, 1)
    gs01 = gs0[1].subgridspec(11, 1)
    ax1 = fig.add_subplot(gs00[:2, :])
    ax2 = fig.add_subplot(gs00[2:5, :])
    ax3 = fig.add_subplot(gs00[5:8, :])
    ax4 = fig.add_subplot(gs00[8:11, :])
    ax5 = fig.add_subplot(gs01[:4, :])
    ax6 = fig.add_subplot(gs01[4:8, :])
    ax7 = fig.add_subplot(gs01[8:11, :])
    '''
   
    plt.savefig(f'{plot_folder}/{plot_name}', dpi=200)
    print(f'Saved plot to {plot_folder}/{plot_name}')

