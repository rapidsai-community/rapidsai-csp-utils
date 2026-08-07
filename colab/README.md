# Colab README

## Folder Contents
Colab folder contains
- `rapids-colab.sh`: main bash script to properly install RAPIDS onto a colab GPU instance.  This script will download all the other files in the folder.
- `env-check.py`: python script to check whether or not your GPU can run RAPIDS
- `update-pyarrow.py`: python script that updates pyarrow on colab to a RAPIDS v0.11+ compatible version

## Maintaining rapids-colab.sh:
`rapids-colab.sh` is the bash script that controls how a user installs Colab on RAPIDS  there are 3 major portions of this script
### 1. Main Function
THe main funciton declares the variables, sets the notice verbiage for every release
There are 3 variables that should be changes with every release
 - NIGHTLIES: This is the version number, after the decimal, for the latest nightly packages
 - STABLE: This is the version number, after the decimal, for the latest stable version that can be installed
 - This is the lowest version number, after the decimal, that the script will support the installation of.  This allows users to run code that they may find useful, but has been deprecated.
2. 
