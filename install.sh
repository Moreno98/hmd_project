#!/bin/sh
eval "$(conda shell.bash hook)"
conda env create -f environment.yml
conda activate hmd_project