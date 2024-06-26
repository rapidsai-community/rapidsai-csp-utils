import os, sys, io
import subprocess
from pathlib import Path

# Install RAPIDS -- we're doing this in one file, for now, due to ease of use
try: 
  import pynvml
except:
  output = subprocess.Popen(["pip install pynvml"], shell=True, stderr=subprocess.STDOUT, 
      stdout=subprocess.PIPE)
  for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
    if(line == ""):
      break
    else:
      print(line.rstrip())
  import pynvml
try:
  pynvml.nvmlInit()
except:
  raise Exception("""
                  Unfortunately you're in a Colab instance that doesn't have a GPU.

                  Please make sure you've configured Colab to request a GPU Instance Type.
               
                  Go to 'Runtime -> Change Runtime Type --> under the Hardware Accelerator, select GPU', then try again."""
  )
gpu_name = pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0))

if(len(sys.argv)==1):
  rapids_version = "24.4.*"
  print("Installing the rest of the RAPIDS " + rapids_version + " libraries")
  output = subprocess.Popen([f"pip install cudf-cu12=={rapids_version} cuml-cu12=={rapids_version} cugraph-cu12=={rapids_version} cuspatial-cu12=={rapids_version} cuproj-cu12=={rapids_version} cuxfilter-cu12=={rapids_version} cucim-cu12=={rapids_version} pylibraft-cu12=={rapids_version} raft-dask-cu12=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
elif(sys.argv[1] == "latest"):
  rapids_version = "24.6.*"
  print("Installing RAPIDS Stable " + rapids_version)
  output = subprocess.Popen([f"pip install cudf-cu12=={rapids_version} cuml-cu12=={rapids_version} cugraph-cu12=={rapids_version} cuspatial-cu12=={rapids_version} cuproj-cu12=={rapids_version} cuxfilter-cu12=={rapids_version} cucim-cu12=={rapids_version} pylibraft-cu12=={rapids_version} raft-dask-cu12=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
elif(sys.argv[1] == "nightlies"):
  rapids_version = "24.8.*"
  print("Installing RAPIDS " + rapids_version)
  rapids_version = "24.08"
  output = subprocess.Popen([f'pip install "cudf-cu12>={rapids_version}.0a0,<=24.8" "cuml-cu12>={rapids_version}.0a0,<=24.8" "cugraph-cu12>={rapids_version}.0a0,<=24.8" "cuspatial-cu12>={rapids_version}.0a0,<=24.8" "cuproj-cu12>={rapids_version}.0a0,<=24.8" "cuxfilter-cu12>={rapids_version}.0a0,<=24.8" "cucim-cu12>={rapids_version}.0a0,<=24.8" "pylibraft-cu12>={rapids_version}.0a0,<=24.8" "raft-dask-cu12>={rapids_version}.0a0,<=24.8" aiohttp --extra-index-url=https://pypi.anaconda.org/rapidsai-wheels-nightly/simple'], shell=True, stderr=subprocess.STDOUT, 
    stdout=subprocess.PIPE)
else:
  rapids_version = "24.4.*"
  print("Installing RAPIDS remaining " + rapids_version + " libraries")
  output = subprocess.Popen([f"pip install cudf-cu12=={rapids_version} cuml-cu12=={rapids_version} cugraph-cu12=={rapids_version} cuspatial-cu12=={rapids_version} cuproj-cu12=={rapids_version} cuxfilter-cu12=={rapids_version} cucim-cu12=={rapids_version} pylibraft-cu12=={rapids_version} raft-dask-cu12=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT, 
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
