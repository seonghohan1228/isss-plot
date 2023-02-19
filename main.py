from functions import *

ORB_NO = 8737

def main():
    hepd_data, mepd_data = read_hdf(ORB_NO)
    graph_plot(hepd_data, mepd_data, ORB_NO, plot_folder='plot', 
            plot_name='plot.png')

if __name__ == "__main__":
    main()
