from constants import *
from functions import *

ORB_NO = 8737

def main():
    hepd_data, mepd_data = read_hdf(ORB_NO, data_folder='isss_data', 
                                    show_tree=False)

if __name__ == "__main__":
    main()
