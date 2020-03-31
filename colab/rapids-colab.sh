#!/bin/bash

MULT="100"
NIGHTLIES=13
STABLE=12
LOWEST=11
 
echo "PLEASE READ"
echo "********************************************************************************************************"
echo "Changes:"
echo "1. Now that most people have migrated, we have rem0ved the migration notice."
echo "2. default stable version is now 0.$STABLE.  Nightly is now 0.$NIGHTLIES"
echo "3. You can now declare your RAPIDS version as a CLI option and skip the user prompts (ex: '0.$STABLE' or '0.$NIGHTLIES', between 0.$LOWEST to 0.$NIGHTLIES, without the quotes): "
echo '        "!bash rapidsai-csp-utils/colab/rapids-colab.sh <version/label>"'
echo "        Examples: '!bash rapidsai-csp-utils/colab/rapids-colab.sh 0.$STABLE', or '!bash rapidsai-csp-utils/colab/rapids-colab.sh stable', or '!bash rapidsai-csp-utils/colab/rapids-colab.sh s'"
echo "                  '!bash rapidsai-csp-utils/colab/rapids-colab.sh 0.$NIGHTLIES, or '!bash rapidsai-csp-utils/colab/rapids-colab.sh nightly', or '!bash rapidsai-csp-utils/colab/rapids-colab.sh n'"
echo "Enjoy using RAPIDS!"


install_RAPIDS () {
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
        
        if (( $RAPIDS_RESULT == $NIGHTLIES )) ;then #Newest nightly packages.  UPDATE EACH RELEASE!
        echo "Installing RAPIDS $RAPIDS_VERSION packages from the nightly release channel"
        echo "Please standby, this will take a few minutes..."
        # install RAPIDS packages
            conda install -y --prefix /usr/local \
                    -c rapidsai-nightly/label/xgboost -c rapidsai-nightly -c nvidia -c conda-forge \
                    python=3.6 cudatoolkit=10.0 \
                    cudf=$RAPIDS_VERSION cuml cugraph gcsfs pynvml cuspatial xgboost\
                    dask-cudf
        else #Stable packages
            echo "Installing RAPIDS $RAPIDS_VERSION packages from the stable release channel"
            echo "Please standby, this will take a few minutes..."
            # install RAPIDS packages
            conda install -y --prefix /usr/local \
                -c rapidsai/label/main -c rapidsai -c nvidia -c conda-forge \
                python=3.6 cudatoolkit=10.0 \
                cudf=$RAPIDS_VERSION cuml cugraph cuspatial gcsfs pynvml xgboost=1.0.0dev.rapidsai$RAPIDS_VERSION\\
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
}

rapids_version_check () {
    
  if  [ $RESPONSE == "NIGHTLY" ]|| [ $RESPONSE == "nightly" ]  || [ $RESPONSE == "N" ] || [ $RESPONSE == "n" ] ; then
    RAPIDS_VERSION="0.$NIGHTLIES"
    RAPIDS_RESULT=$NIGHTLIES
    echo "Starting to prep Colab for install RAPIDS Version 0.$NIGHTLIES nightly"
  elif [ $RESPONSE == "STABLE" ]|| [ $RESPONSE == "stable" ]  || [ $RESPONSE == "S" ] || [ $RESPONSE == "s" ] ; then
    RAPIDS_VERSION="0.$STABLE"
    RAPIDS_RESULT=$STABLE
    echo "Starting to prep Colab for install RAPIDS Version 0.$STABLE stable"
  else
    RAPIDS_RESULT=$(awk '{print $1*$2}' <<<"${RESPONSE} ${MULT}")
    if (( $RAPIDS_RESULT > $NIGHTLIES )) ;then
      RAPIDS_VERSION="0.$NIGHTLIES"
      RAPIDS_RESULT=$NIGHTLIES
      echo "RAPIDS Version modified to 0.$NIGHTLIES nightly"
    elif (($RAPIDS_RESULT < $LOWEST)) ;then
      RAPIDS_VERSION="0.$LOWEST"
      RAPIDS_RESULT=$LOWEST
      echo "RAPIDS Version modified to 0.$LOWEST stable"
    else
      RAPIDS_VERSION="0.$STABLE"
      RAPIDS_RESULT=$STABLE
      echo "RAPIDS Version modified to 0.$STABLE stable"
    fi
  fi
}

if [ -n "$1" ] ; then
  RESPONSE=$1
  echo $RESPONSE
  rapids_version_check
  #install_RAPIDS
else
  echo "As you didn't specify a RAPIDS version, please enter in the box your desired RAPIDS version (ex: '0.11' or '0.12', between 0.$LOWEST to 0.$NIGHTLIES, without the quotes)"
  echo "and hit Enter. If you need stability, use 0.$STABLE. If you want bleeding edge, use our nightly version (0.$NIGHTLIES), but things can break."
  read RESPONSE
  rapids_version_check
  #install_RAPIDS
fi
