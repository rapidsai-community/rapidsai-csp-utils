#!/bin/bash
echo "Updating your Colab environment.  This will restart your kernel.  Don't Panic!"
pip install -q condacolab
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
echo "Added repo"
sudo apt-get update
echo "Installing libstdc++"
sudo apt-get -y install libstdc++6=11.1.0*
echo "restarting Colab..."