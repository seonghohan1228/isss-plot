# isss-plot
New version of the old "isss" package. Certain parts of the code was reused while others were completely redesigned.
Windows OS is not yet supported.

## Installation
### Python virtual environment (conda)
In order to keep the required packages separate from other local packages, it is recommended to create a virtual envinment.

Using conda, create a virtual environment with the folder name as 'conda' in the current directory:

```sh
conda create --prefix ./conda
```

Activate the virtual enviroment:

```sh
conda activate ./conda
```

If (FILEPATH/conda) appears on the terminal, the activation is complete.
In order to deactivate:

```sh
conda deactivate
```

Install packages using conda:

```sh
conda install numpy matplotlib h5py pandas
conda install -c conda-forge basemap
```

```sh
sudo apt install gfortran
pip install spacepy
pip install aacgmv2
```