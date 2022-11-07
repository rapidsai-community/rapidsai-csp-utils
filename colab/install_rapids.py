#!/usr/bin/env python
import os, sys, io
import subprocess
from pathlib import Path

# CFFI fix with pip 
output = subprocess.Popen(["pip uninstall --yes cffi"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
  if(line == ""):
    break
  else:
    print(line.rstrip())
output = subprocess.Popen(["pip uninstall --yes cryptography"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
  if(line == ""):
    break
  else:
    print(line.rstrip())
output = subprocess.Popen(["pip install cffi==1.15.1"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
  if(line == ""):
    break
  else:
    print(line.rstrip())

# Install RAPIDS
pkg = "rapids"
if(sys.argv[1] == "nightly"):
  release =  ["rapidsai-nightly", "22.02"]
  print("Installing RAPIDS Nightly "+release[1])
else:
  release = ["rapidsai", "21.12"]
  print("Installing RAPIDS Stable "+release[1])

pkg = "rapids"
print("Starting the RAPIDS install on Colab.  This will take about 15 minutes.")

output = subprocess.Popen(["conda install -y --prefix /usr/local -c "+release[0]+" -c nvidia -c conda-forge python=3.7 cudatoolkit=11.2 "+pkg+"="+release[1]+" llvmlite gcsfs openssl dask-sql"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
  if(line == ""):
    break
  else:
    print(line.rstrip())

print("RAPIDS conda installation complete.  Updating Colab's libraries...")
import sys, os, shutil
sys.path.append('/usr/local/lib/python3.7/site-packages/')
os.environ['NUMBAPRO_NVVM'] = '/usr/local/cuda/nvvm/lib64/libnvvm.so'
os.environ['NUMBAPRO_LIBDEVICE'] = '/usr/local/cuda/nvvm/libdevice/'

os.environ["CONDA_PREFIX"] = "/usr/local"
for so in ['cudf', 'rmm', 'nccl', 'cuml', 'cugraph', 'xgboost', 'cuspatial', 'cupy', 'geos','geos_c']:
  fn = 'lib'+so+'.so'
  source_fn = '/usr/local/lib/'+fn
  dest_fn = '/usr/lib/'+fn
  if os.path.exists(source_fn):
    print(f'Copying {source_fn} to {dest_fn}')
    shutil.copyfile(source_fn, dest_fn)
