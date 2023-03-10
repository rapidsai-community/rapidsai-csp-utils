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
  print('We will now install RAPIDS 22.12 via pip!  Please stand by, should be quick...')
  print('***********************************************************************')
  print()


  # Install RAPIDS -- we're doing this in one file, for now, due to ease of use
  output = subprocess.Popen(["pip install cudf-cu11==22.12 cuml-cu11==22.12 cugraph-cu11==22.12 --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT, 
      stdout=subprocess.PIPE)
  for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
    if(line == ""):
      break
    else:
      print(line.rstrip())
  output = subprocess.Popen(["rm -rf /usr/local/lib/python3.8/dist-packages/cupy*"], shell=True, stderr=subprocess.STDOUT, 
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
          With the new pip install complete, please do not run any further installation 
          commands from the conda based installation methods!!!  
          
          In your personal files, you can delete these cells.  
          
          RAPIDSAI owned templates/notebooks should already be updated with no action needed.
          ***********************************************************************
          """
       )
else:
  raise Exception("""
                  Unfortunately Colab didn't give you a RAPIDS compatible GPU (P4, P100, T4, or V100), but gave you a """+ gpu_name +""".

                  Please use 'Runtime -> Factory Reset Runtimes...', which will allocate you a different GPU instance, to try again."""
  )  
