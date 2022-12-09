# Devtools directory

This directory contains data and tools to support the development and deployment of your library.

## How to create a conda environment to work with this repository

To create a working conda environment named in this case "OpenCTN-Tools", do the following:

```bash
conda env create -n OpenCTN-Tools -f conda_env.yaml
```

Now you can activate the environment:

```bash
conda activate OpenCTN-Tools
```

## How to update your conda environment with new dependencies

With the environment activated execute the command:

```bash
conda env update -f conda_env.yaml --prune
```

or

```bash
mamba env update --file conda_env.yaml --prune
```
