# isss-plot
New version of the old "isss" package.
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
conda install -y numpy
conda install -y matplotlib
conda install -y h5py
conda install -y pandas
conda install -y -c conda-forge basemap
```