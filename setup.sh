#!/usr/bin/env bash

conda create -n mnemonics python=3.12 -y
conda activate mnemonics
if [ "$CONDA_DEFAULT_ENV" != "mnemonics" ]; then
    echo -e "\e[31mError: failed to activate environment 'mnemonics'. Aborting.\e[0m"
    return 1
fi

python -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
else
    echo "File requirements.txt not found."
fi
