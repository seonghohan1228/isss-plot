# main.py

import constants
import h5py

filepath = constants.FILEPATH

def main():
    # Load file
    with h5py.File(filepath) as f:
        print("Opening file: " + filepath)
            
        # Read and process data
        f.close()
    
    # Plot

if __name__ == "__main__":
    main()


