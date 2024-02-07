#!/usr/bin/env bash

# commented commands
# -g -t \

runcompss \
    --lang=python \
    --python_interpreter=python3 \
    --pythonpath=$(pwd) \
    ./launch-multiple-simulations-pycompss.py
