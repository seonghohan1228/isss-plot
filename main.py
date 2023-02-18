# main.py

from constants import *
from functions import *

SHOW_TREE = True
ORB_NO = 8737

def main():
    # Load file
    data = read_hdf(ORB_NO, SHOW_TREE)
    print(data)
    # Plot


if __name__ == "__main__":
    main()


