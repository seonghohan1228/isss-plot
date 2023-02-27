# isss_plot_functions.py
# Functions related to data plotting.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
from mpl_toolkits.basemap import Basemap

def closest(arr, value):
    '''
    Finds the index of an array that is closest to the given value.
    '''
    return min(range(len(arr)), key=lambda i: abs(arr[i]-value))


def geomag_lat(alt, time):
    '''
    Takes the altitude and time to calculate the geomagnetic latitude line coordinates.
    '''
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


def new_cmap():
    '''
    Creates custom colormap for HEPD telescope and MEPD detector plot.
    '''
    jet = plt.cm.get_cmap('jet', 256)
    newcolors = jet(np.linspace(0, 1, 256))
    white = np.array([256/256, 256/256, 256/256, 1])
    newcolors[0, :] = white
    new_cmap = mplc.ListedColormap(newcolors)
    return new_cmap


def plot_pc1(pc1, time, ax):
    '''
    Plots PC1 data with respect to time. PC1 and time data has 3 entries: HEPD, MEPD-A, and MEPD-B.
    '''
    print('Plotting PC1 data ...')
    # HEPD
    ax[0].plot(pc1[0], time[0], color='black', marker='x', markersize=0.1, linestyle='-')
    # MEPD-A and MEPD-B
    ax[1].plot(pc1[1], time[1], color='black', marker='x', markersize=0.1, linestyle='-')
    ax[1].plot(pc1[2], time[2], color='red', marker='D', markersize=0.1, linestyle='--')
    print('PC1 data plot completed')


def plot_position(pos, ax):
    '''
    Plots the satellite position onto a global map. Uses the position data LATT, LONG.
    '''
    print('Plotting position data ...')
    map = Basemap(projection='merc', llcrnrlat=-85,urcrnrlat=85, llcrnrlon=-180, urcrnrlon=180)
    map.drawcoastlines()
    map.drawparallels(np.arange(-90,90,30), labels=[True, False, False, False])
    map.drawmeridians(np.arange(0,360,45), labels=[False, False, False, True])
    x, y = map(pos[0], pos[1])
    map.scatter(x, y, color='r', marker='.')
    print('Position data plot completed')


def plot_geomag(alt, start_time, map):
    '''
    Plots the geomagnetic latitudes -60, -30, 0, 30, and 60 on map.
    Calculation using the function geomag_lat requires a lot of time.
    '''
    print('Plotting geomagnetic latitude ...')
    avg_alt = sum(alt) / len(alt)
    geomag_coord = geomag_lat(avg_alt, start_time)
    for i in range(5):
        x, y = map(np.arange(-180, 180, 1), geomag_coord[i,:])
        map.plot(x, y, 'b')
    print('Geomagnetic latitude plot completed')


def plot_mag(mag, time, ax):
    '''
    Plots the magnetic fields.
    '''
    print('Plotting magnetic field data ...')
    mag_avg = [np.sqrt(mag[4][i]**2 + mag[5][i]**2 + mag[6][i]**2) for i in range(len(mag[4]))]
    ax.plot(time[0], mag[0], 'k', label='Bx')
    ax.plot(time[0], mag[1], 'b', label='By')
    ax.plot(time[0], mag[2], 'r', label='Bz')
    ax.plot(time[0], mag[4], '--k', label='IGRF Bx')
    ax.plot(time[0], mag[5], '--b', label='IGRF By')
    ax.plot(time[0], mag[6], '--r', label='IGRF Bz')
    ax.plot(time[0], mag_avg, '--y', label='IGRF|B|')
    print('Magnetic field data plot completed')


def plot_tel(tel, ax):
    print('Plotting telescope data ...')
    ax.imshow(X=tel[2], aspect='auto', origin='lower', cmap=new_cmap(), interpolation='none')
    print('Telescope data plot completed')