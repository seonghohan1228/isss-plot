import warnings
from functions import *
from classes import *

ORB_NO = 8795

def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    filepaths = find_filepaths(ORB_NO)
    raw_data = read_hdf(filepaths)
    isss_data = ISSSData()
    isss_data.set_data(raw_data)
    graph_plot(isss_data, ORB_NO)

if __name__ == "__main__":
    main()
