# Devtools directory

This directory contains data and tools to support the development and deployment of your library.

## How to create a conda environment to work with this repository

To create a working conda environment named in this case "OpenKTN-Tests", do the following:

```bash
conda env create -n OpenKTN-Tests -f conda_env.yaml
```

Now you can activate the environment:

```bash
conda activate OpenKTN-Tests
```

## How to update your conda environment with new dependencies

With the environment activated,

```bash
conda activate OpenKTN-Tests
```

execute the command:

```bash
conda env update -f conda_env.yaml --prune
```

`--prune` uninstalls dependencies in your environment no longer needed by the list of packages in the file
`conda_env.yaml`.

