#!/bin/bash

set -eu

echo "PLEASE READ"
echo "********************************************************************************************************"
echo "Colab Notebooks Migration Notice:"
echo " "
echo "We have changed the location of the Colab script to our new CSP utilties repo."
echo "We are also dropping support for versions below 0.11, as we are on 0.13 nightlies"
echo " "
echo "Not all Colab notebooks are updated (like personal Colabs) and/or are using outdated versions of RAPIDS,"
echo "so we HIGHLY encourage users to update their scripts and Colab notebooks both with the new link AND with "
echo "to the new API.  Otherwise, your code MAY BREAK"
echo " "
echo "This notice will disappear/be updated on our next release."
echo " "
echo "Please enter in the box your desired RAPIDS version (ex: '0.11' or '0.12', between 0.11 to 0.13, without the quotes)"
echo "and hit Enter. If you need stability, use 0.12. If you want bleeding edge, use our nightlies (0.13), but things can break."

read RAPIDS_VERSION
MULT="100"

#conditions accidental inputs
RAPIDS_RESULT=$(awk '{print $1*$2}' <<<"${RAPIDS_VERSION} ${MULT}")
#echo $RAPIDS_RESULT
if (( $RAPIDS_RESULT >=13 )) ;then
  RAPIDS_VERSION="0.13"
  RAPIDS_RESULT=13
  echo "RAPIDS Version modified to 0.13 nightlies"
elif (( $RAPIDS_RESULT <= 11 )) ;then
  RAPIDS_VERSION="0.11"
  RAPIDS_RESULT=11
  echo "RAPIDS Version modified to 0.11 stable"
fi
#echo $RAPIDS_VERSION
if (( $RAPIDS_RESULT >= 11 )) ;then
  echo "Please COMPARE the \"SCRIPT TO COPY\" with the code in the above cell.  If they are the same, just type any key.  If not, do steps 2-4. "
  echo " "
  echo "SCRIPT TO COPY: "
  echo "!git clone https://github.com/rapidsai/rapidsai-csp-utils.git"
  echo "!bash rapidsai-csp-utils/colab/rapids-colab.sh"
  echo "import sys, os"
  echo "dist_package_index = sys.path.index('/usr/local/lib/python3.6/dist-packages')"
  echo "sys.path = sys.path[:dist_package_index] + ['/usr/local/lib/python3.6/site-packages'] + sys.path[dist_package_index:]"
  echo "sys.path"
  echo "exec(open('rapidsai-csp-utils/colab/update_modules.py').read(), globals())"
  echo "********************************************************************************************************"
  echo "Do you have the above version of the script running in your cell? (Y/N).  "
  echo "Please note: If you do not positively affirm with 'Y' or 'y', the script show you have to rectify that issue and then stop the RAPIDS install,"
  echo "without installing RAPIDS, but will still continue update some packages"
  read response
  if [ $response == "Y" ] || [ $response == "y" ] ;then
    echo "Continuing with RAPIDS install"
  else
    echo "Please do the following:"
    echo "1. STOP cell execution" 
    echo "2. CUT and PASTE the script below into the cell you just ran "
    echo "3. RERUN the cell"
    echo " "
    echo "SCRIPT TO COPY:"
    echo "!git clone https://github.com/rapidsai/rapidsai-csp-utils.git"
    echo "!bash rapidsai-csp-utils/colab/rapids-colab.sh"
    echo "import sys, os"
    echo "dist_package_index = sys.path.index('/usr/local/lib/python3.6/dist-packages')"
    echo "sys.path = sys.path[:dist_package_index] + ['/usr/local/lib/python3.6/site-packages'] + sys.path[dist_package_index:]"
    echo "sys.path"
    echo "exec(open('rapidsai-csp-utils/colab/update_modules.py').read(), globals())"
    echo "********************************************************************************************************"
    echo "Please COPY the above code and RERUN the cell"
    exit 0
  fi
else
  echo "You may not have to change anything.  All versions of our script should work with this version of Colab"
fi

echo "Checking for GPU type:"
python rapidsai-csp-utils/colab/env-check.py

if [ ! -f Miniconda3-4.5.4-Linux-x86_64.sh ]; then
    echo "Removing conflicting packages, will replace with RAPIDS compatible versions"
    # remove existing xgboost and dask installs
    pip uninstall -y xgboost dask distributed

    # intall miniconda
    echo "Installing conda"
    wget https://repo.continuum.io/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh
    chmod +x Miniconda3-4.5.4-Linux-x86_64.sh
    bash ./Miniconda3-4.5.4-Linux-x86_64.sh -b -f -p /usr/local
    
    #Installing another conda package first something first seems to fix https://github.com/rapidsai/rapidsai-csp-utils/issues/4
    conda install -y --prefix /usr/local -c conda-forge openssl python=3.6
    
    if (( $RAPIDS_RESULT == 13 )) ;then #Newest nightly packages.  UPDATE EACH RELEASE!
    echo "Installing RAPIDS $RAPIDS_VERSION packages from the nightly release channel"
    echo "Please standby, this will take a few minutes..."
    # install RAPIDS packages
        conda install -y --prefix /usr/local \
                -c rapidsai-nightly/label/xgboost -c rapidsai-nightly -c nvidia -c conda-forge \
                python=3.6 cudatoolkit=10.0 \
                cudf=$RAPIDS_VERSION cuml cugraph gcsfs pynvml cuspatial xgboost\
                dask-cudf
    else #Stable packages requiring PyArrow 0.15
        echo "Installing RAPIDS $RAPIDS_VERSION packages from the stable release channel"
        echo "Please standby, this will take a few minutes..."
        # install RAPIDS packages
        conda install -y --prefix /usr/local \
            -c rapidsai/label/xgboost -c rapidsai -c nvidia -c conda-forge \
            python=3.6 cudatoolkit=10.0 \
            cudf=$RAPIDS_VERSION cuml cugraph cuspatial gcsfs pynvml xgboost\
            dask-cudf
    fi
      
    echo "Copying shared object files to /usr/lib"
    # copy .so files to /usr/lib, where Colab's Python looks for libs
    cp /usr/local/lib/libcudf.so /usr/lib/libcudf.so
    cp /usr/local/lib/librmm.so /usr/lib/librmm.so
    cp /usr/local/lib/libnccl.so /usr/lib/libnccl.so
fi

echo ""
echo "************************************************"
echo "Your Google Colab instance has RAPIDS installed!"
echo "************************************************"
