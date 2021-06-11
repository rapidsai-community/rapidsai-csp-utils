#!/usr/bin/env python
import os, sys
import subprocess
from pathlib import Path

pkg = "rapids-blazing"
if(sys.argv[1] == "nightly"):
  verion =  ["rapidsai-nightly", "21.08"]
  print("Installing RAPIDS Nightly "+install[1])
else:
  verion = ["rapidsai", "21.06"]
  print("Installing RAPIDS Stable "+install[1])

if(sys.argv[2] == "core"):
  pkg = "rapids"

print("Starting the RAPIDS install on Colab.  This will take about 15 minutes.")
output = subprocess.Popen(["conda install -y --prefix /usr/local -c "+verion[0]+" -c nvidia -c conda-forge python=3.7 cudatoolkit=11.0 "+pkg+"="+verion[1]+" llvmlite gcsfs openssl"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
stdout, _ = output.communicate()
print(stdout)

print("RAPIDS conda installation complete.  Updating Colab's libraries...")
import sys, os, shutil
sys.path.append('/usr/local/lib/python3.7/site-packages/')
os.environ['NUMBAPRO_NVVM'] = '/usr/local/cuda/nvvm/lib64/libnvvm.so'
os.environ['NUMBAPRO_LIBDEVICE'] = '/usr/local/cuda/nvvm/libdevice/'

os.environ["CONDA_PREFIX"] = "/usr/local"
for so in ['cudf', 'rmm', 'nccl', 'cuml', 'cugraph', 'xgboost', 'cuspatial', 'cupy', 'geos']:
  fn = 'lib'+so+'.so'
  source_fn = '/usr/local/lib/'+fn
  dest_fn = '/usr/lib/'+fn
  if os.path.exists(source_fn):
    print(f'Copying {source_fn} to {dest_fn}')
    shutil.copyfile(source_fn, dest_fn)