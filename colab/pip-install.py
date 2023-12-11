import os, sys, io
import subprocess
from pathlib import Path

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

if ('K80' not in gpu_name):
  print('***********************************************************************')
  print('Woo! Your instance has the right kind of GPU, a '+ str(gpu_name)+'!')
  print('We will now install RAPIDS cuDF, cuML, and cuGraph via pip! ')
  print('Please stand by, should be quick...')
  print('***********************************************************************')
  print()


  # Install RAPIDS -- we're doing this in one file, for now, due to ease of use
  rapids_version = "23.10.*"
  output = subprocess.Popen([f"pip install cudf-cu11=={rapids_version} cuml-cu11=={rapids_version} cugraph-cu11=={rapids_version} cuspatial-cu11=={rapids_version} cuproj-cu11=={rapids_version} cuxfilter-cu11=={rapids_version} cucim=={rapids_version} pylibraft-cu11=={rapids_version} raft-dask-cu11=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT, 
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
  output = subprocess.Popen(["pip install cupy-cuda11x"], shell=True, stderr=subprocess.STDOUT, 
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
else:
  raise Exception("""
                  Unfortunately Colab didn't give you a RAPIDS compatible GPU (P4, P100, T4, or V100), but gave you a """+ gpu_name +""".

                  Please use 'Runtime -> Factory Reset Runtimes...', which will allocate you a different GPU instance, to try again."""
  )  
