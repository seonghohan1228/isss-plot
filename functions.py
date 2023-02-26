import os
import sys
import h5py
import math
import aacgmv2
import spacepy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spacepy.coordinates as coord
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


# Finds the index of an array that is closest to the given value.
def closest(arr, value):
    return min(range(len(arr)), key=lambda i: abs(arr[i]-value))


# Takes the altitude and time to calculate the geomagnetic latitude line coordinates
def geomag_lat(alt, time):
    arr = np.zeros((181, 360))
    geomag_coord = np.zeros((5, 360))
    print('Creating matrix for geomagnetic coordinates')
    for j in range(360):
        for i in range(181):
            # Show progress
            sys.stdout.write("\rProgress: [ {:.1f}%]".format(float(j*181+i+1)/(360*181)*100))
            sys.stdout.flush()
            coordinates = coord.Coords([alt, i - 90, j - 180], 'GEO', 'sph')
            coordinates.ticks = spacepy.time.Ticktock(time, 'ISO')
            arr[i][j] = coordinates.convert('MAG', 'sph').lati
    print('\tDone')
    for j in range(360):
        sys.stdout.write("\rProgress: [ {:.1f}%]".format((float(j+1)/360)*100))
        sys.stdout.flush()
        for i in range(5):
            geomag_coord[i, j] = closest(arr[:, j], 30 * i - 60) - 90
    print('\tDone')
    return geomag_coord


# Plotting combined plots
def graph_plot(isss_data, orbit_no, plot_folder='./plot', plot_name='plot.png'):
    # Create figure
    fig = plt.figure(constrained_layout=True, figsize=(12, 15))
    fig.suptitle(f'Orbit: {orbit_no} Date: ')
    subfigs = fig.subfigures(1, 2, wspace=0.05)
    subfigsnest0 = subfigs[0].subfigures(3, 1, height_ratios=[2, 3.5, 5.5])
    # Plot subplots
    # PC1
    axes0 = subfigsnest0[0].subplots(1, 2)
    axes0[0].plot(isss_data.pc1[0], isss_data.time[0], color='black', marker='.')
    axes0[1].plot(isss_data.pc1[1], isss_data.time[1], color='black', marker='x', markersize=0.1, linestyle='-')
    axes0[1].plot(isss_data.pc1[2], isss_data.time[2], color='red', marker='D', markersize=0.1, linestyle='--')
    
    # Position
    axes1 = subfigsnest0[1].subplots()
    axes1.plot(isss_data.position[0], isss_data.position[1])
    map = Basemap(projection='merc', llcrnrlat=-85,urcrnrlat=85, llcrnrlon=-180, urcrnrlon=180)
    map.drawcoastlines()
    map.drawparallels(np.arange(-90,90,30), labels=[True, False, False, False])
    map.drawmeridians(np.arange(0,360,45), labels=[False, False, False, True])
    x, y = map(isss_data.position[0], isss_data.position[1])
    map.scatter(x, y,color='r', marker='.')
    # Geomagnetic latitude
    '''avg_alt = sum(isss_data.position[2]) / len(isss_data.position[2])
    geomag_coord = geomag_lat(avg_alt, isss_data.time[0][0])
    
    for i in range(5):
        x, y = map(np.arange(-180, 180, 1), geomag_coord[i,:])
        map.plot(x, y, 'b')'''

    # Magnetic field
    axes2 = subfigsnest0[2].subplots(2, 1, gridspec_kw={'height_ratios': [2.5, 3]})
    axes2[0].plot(isss_data.time[0], isss_data.magnetic[0], 'k', label='Bx')
    axes2[0].plot(isss_data.time[0], isss_data.magnetic[1], 'b', label='By')
    axes2[0].plot(isss_data.time[0], isss_data.magnetic[2], 'r', label='Bz')
    axes2[0].plot(isss_data.time[0], isss_data.magnetic[4], '--k', label='IGRF Bx')
    axes2[0].plot(isss_data.time[0], isss_data.magnetic[5], '--b', label='IGRF By')
    axes2[0].plot(isss_data.time[0], isss_data.magnetic[6], '--r', label='IGRF Bz')
    mag_avg = [math.sqrt(isss_data.magnetic[4][i]**2 + isss_data.magnetic[5][i]**2 + isss_data.magnetic[6][i]**2) for i in range(len(isss_data.magnetic[4]))]
    axes2[0].plot(isss_data.time[0], mag_avg, '--y', label='IGRF|B|')
    
    # Save figure
    plt.savefig(f'{plot_folder}/{plot_name}', dpi=200)
    print(f'Saved plot to {plot_folder}/{plot_name}')

