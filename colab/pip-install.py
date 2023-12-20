import os, sys, io
import subprocess
from pathlib import Path

# Install RAPIDS -- we're doing this in one file, for now, due to ease of use
rapids_version = "23.12.*"
output = subprocess.Popen([f"pip install cudf-cu12=={rapids_version} cuml-cu12=={rapids_version} cugraph-cu12=={rapids_version} cuspatial-cu12=={rapids_version} cuproj-cu12=={rapids_version} cuxfilter-cu12=={rapids_version} cucim-cu12=={rapids_version} pylibraft-cu12=={rapids_version} raft-dask-cu12=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
  if(line == ""):
    break
  else:
    print(line.rstrip())
output = subprocess.Popen(["rm -rf /usr/local/lib/python3.10/dist-packages/cupy*"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
  if(line == ""):
    break
  else:
    print(line.rstrip())
output = subprocess.Popen(["pip install cupy-cuda12x"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
  if(line == ""):
    break
  else:
    print(line.rstrip())
print("""
        ***********************************************************************
        The pip install of RAPIDS is complete.
        
        Please do not run any further installation from the conda based installation methods, as they may cause issues!
        
        Please ensure that you're pulling from the git repo to remain updated with the latest working install scripts.

        Troubleshooting:
            - If there is an installation failure, please check back on RAPIDSAI owned templates/notebooks to see how to update your personal files. 
            - If an installation failure persists when using the latest script, please make an issue on https://github.com/rapidsai-community/rapidsai-csp-utils
        ***********************************************************************
        """
      )
