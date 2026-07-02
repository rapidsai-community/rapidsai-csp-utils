#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

echo "Updating your Colab environment.  This will restart your kernel.  Don't Panic!"
pip install -q condacolab
pip uninstall -y cupy-cuda12x
echo "restarting Colab..."
