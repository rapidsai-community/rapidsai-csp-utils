import io
import subprocess

try:
    import pynvml
except ImportError:
    output = subprocess.Popen(
        ["pip install pynvml"],
        shell=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
        if line == "":
            break
        else:
            print(line.rstrip())
    import pynvml
try:
    pynvml.nvmlInit()
except Exception:
    raise Exception(
        "Unfortunately you're in a Colab instance that doesn't have a GPU.\n\n"
        "Please make sure you've configured Colab to request a GPU Instance Type.\n\n"
        "Go to 'Runtime -> Change Runtime Type -> under the Hardware Accelerator, "
        "select GPU', then try again."
    )
gpu_name = pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0))

if "K80" not in gpu_name:
    print("***********************************************************************")
    print("Woo! Your instance has the right kind of GPU, a " + str(gpu_name) + "!")
    print("We will now install RAPIDS cuDF, cuML, and cuGraph via pip! ")
    print("Please stand by, should be quick...")
    print("***********************************************************************")
    print()

    # Install RAPIDS -- we're doing this in one file, for now, due to ease of use
    output = subprocess.Popen(
        [
            "pip install cudf-cu11 cuml-cu11 cugraph-cu11 cuspatial-cu11 cuproj-cu11 "
            "cuxfilter-cu11 cucim pylibraft-cu11 raft-dask-cu11 aiohttp "
            "--extra-index-url=https://pypi.nvidia.com"
        ],
        shell=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
        if line == "":
            break
        else:
            print(line.rstrip())
    output = subprocess.Popen(
        ["rm -rf /usr/local/lib/python3.8/dist-packages/cupy*"],
        shell=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
        if line == "":
            break
        else:
            print(line.rstrip())
    output = subprocess.Popen(
        ["pip install cupy-cuda11x"],
        shell=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
        if line == "":
            break
        else:
            print(line.rstrip())
    print(
        """
***********************************************************************
The pip install of RAPIDS is complete.

Please do not run any further installation from the conda based
installation methods, as they may cause issues!

Please ensure that you're pulling from the git repo to remain updated
with the latest working install scripts.

Troubleshooting:
 - If there is an installation failure, please check back on RAPIDS
   templates/notebooks to see how to update your personal files.
 - If an installation failure persists when using the latest script, please
   file an issue on https://github.com/rapidsai-community/rapidsai-csp-utils
***********************************************************************"""
    )
else:
    raise Exception(
        "Unfortunately Colab didn't give you a RAPIDS compatible GPU "
        f"(P4, P100, T4, or V100), but gave you a {gpu_name}.\n\n"
        "Please use 'Runtime -> Factory Reset Runtimes...', which will allocate "
        "a different GPU instance, to try again."
    )
