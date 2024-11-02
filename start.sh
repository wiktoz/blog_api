#!/bin/bash

if [[ ! -f "ec-pub.key" || ! -f "ec.key" ]]
then
    bash generate_keys.sh
fi

python3 app.py