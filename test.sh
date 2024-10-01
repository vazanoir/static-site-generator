#!/usr/bin/env bash

cd src
python3 -m unittest discover -s ../tests
cd -
