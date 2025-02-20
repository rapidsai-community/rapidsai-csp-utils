import os, sys, io
import subprocess
from pathlib import Path

# Install RAPIDS -- we're doing this in one file, for now, due to ease of use
try:
  import pynvml
except:
  output = subprocess.Popen(["uv pip install --system pynvml"], shell=True, stderr=subprocess.STDOUT,
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

LATEST_RAPIDS_VERSION = "25.02"
NIGHTLY_RAPIDS_VERSION = "25.04"

if(len(sys.argv)>=2):
  if(len(sys.argv[1])=="legacy"):
    rapids_version = "24.12.*"
    print("Installing the rest of the RAPIDS " + rapids_version + " libraries")
    output = subprocess.Popen([f"uv pip install --system cudf-cu12=={rapids_version} cuml-cu12=={rapids_version} cugraph-cu12=={rapids_version} cuspatial-cu12=={rapids_version} cuproj-cu12=={rapids_version} cuxfilter-cu12=={rapids_version} cucim-cu12=={rapids_version} pylibraft-cu12=={rapids_version} raft-dask-cu12=={rapids_version} nx-cugraph-cu12=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT,
      stdout=subprocess.PIPE)
  elif(sys.argv[1] == "latest"):
    print(f"Installing RAPIDS Stable {LATEST_RAPIDS_VERSION}.*")
    output = subprocess.Popen([f"pip install cudf-cu12=={LATEST_RAPIDS_VERSION}.* cuml-cu12=={LATEST_RAPIDS_VERSION}.* cugraph-cu12=={LATEST_RAPIDS_VERSION}.* cuspatial-cu12=={LATEST_RAPIDS_VERSION} cuproj-cu12=={LATEST_RAPIDS_VERSION} cuxfilter-cu12=={LATEST_RAPIDS_VERSION} cucim-cu12=={LATEST_RAPIDS_VERSION} pylibraft-cu12=={LATEST_RAPIDS_VERSION} raft-dask-cu12=={LATEST_RAPIDS_VERSION}.* nx-cugraph-cu12=={LATEST_RAPIDS_VERSION}.* aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT,
      stdout=subprocess.PIPE)
  elif(sys.argv[1] == "nightlies"):
    print(f"Installing RAPIDS {NIGHTLY_RAPIDS_VERSION}.*")
    output = subprocess.Popen([f'pip install "cudf-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "cuml-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "cugraph-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "cuspatial-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "cuproj-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "cuxfilter-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "cucim-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "pylibraft-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a" "raft-dask-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" "nx-cugraph-cu12=={NIGHTLY_RAPIDS_VERSION}.*,>=0.0.0a0" aiohttp --extra-index-url=https://pypi.anaconda.org/rapidsai-wheels-nightly/simple'], shell=True, stderr=subprocess.STDOUT,
      stdout=subprocess.PIPE)
  else:
    rapids_version = "25.02.*"
    print("Installing RAPIDS Stable " + rapids_version)
    output = subprocess.Popen([f"pip install cudf-cu12=={rapids_version} cuml-cu12=={rapids_version} cugraph-cu12=={rapids_version} cuspatial-cu12=={rapids_version} cuproj-cu12=={rapids_version} cuxfilter-cu12=={rapids_version} cucim-cu12=={rapids_version} pylibraft-cu12=={rapids_version} raft-dask-cu12=={rapids_version} nx-cugraph-cu12=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT,
      stdout=subprocess.PIPE)
else:
  rapids_version = "24.12.*"
  print("Installing RAPIDS remaining " + rapids_version + " libraries")
  output = subprocess.Popen([f"uv pip install --system cudf-cu12=={rapids_version} cuml-cu12=={rapids_version} cugraph-cu12=={rapids_version} cuspatial-cu12=={rapids_version} cuproj-cu12=={rapids_version} cuxfilter-cu12=={rapids_version} cucim-cu12=={rapids_version} pylibraft-cu12=={rapids_version} raft-dask-cu12=={rapids_version} nx-cugraph-cu12=={rapids_version} aiohttp --extra-index-url=https://pypi.nvidia.com"], shell=True, stderr=subprocess.STDOUT,
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
