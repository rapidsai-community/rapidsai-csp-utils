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
    print("We will now install RAPIDS via pip!  Please stand by, should be quick...")
    print("***********************************************************************")
    print()
else:
    raise Exception(
        "Unfortunately Colab didn't give you a RAPIDS compatible GPU "
        f"(P4, P100, T4, or V100), but gave you a {gpu_name}.\n\n"
        "Please use 'Runtime -> Factory Reset Runtimes...', which will allocate "
        "a different GPU instance, to try again."
    )
