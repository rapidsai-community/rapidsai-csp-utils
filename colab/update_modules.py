import re
import sys
import os

print('***********************************************************************')
print('Let us check on those pyarrow and cffi versions...')
print('***********************************************************************')
print()

try:
  sys.modules["pyarrow"]
  pyarrow_version = sys.modules["pyarrow"].__version__
  f = re.search("0.15.+", pyarrow_version)
  if(f == None):
    for key in list(sys.modules.keys()):
      if key.startswith("pyarrow"):
        del sys.modules[key]
        print(f"unloaded pyarrow {pyarrow_version}")
    import pyarrow
    pyarrow_version = sys.modules['pyarrow'].__version__
    print(f"loaded pyarrow {pyarrow_version}")
    print(f"You're now running pyarrow {pyarrow_version} and are good to go!")
    del(pyarrow_version)
  else:
    print(f"You're running pyarrow {pyarrow_version} and are good to go!")

except: 
  print(f"You're don't have pyarrow.")

try:  
  sys.modules['cffi']
  cffi_version = sys.modules['cffi'].__version__
  f = re.search("1.13.+", cffi_version)
  if f == None:
    for key in list(sys.modules.keys()):
      if key.startswith('cffi'):
        del sys.modules[key]
    print(f"unloaded cffi {cffi_version}")
    import cffi
    cffi_version = sys.modules['cffi'].__version__
    print(f"loaded cffi {cffi_version}")
    del(cffi_version)
  else:
    print(f"cffi {cffi_version} is good to go!")

except: 
  print(f"You don't have cffi")
