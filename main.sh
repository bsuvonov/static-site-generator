#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 src/main.py
cd public && python3 -m http.server 8888 --bind 127.0.0.1
