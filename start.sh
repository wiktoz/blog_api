#!/bin/sh

if [ ! -f "ec-pub.key" ] || [ ! -f "ec.key" ]; then

    sh generate_keys.sh
fi

python3 app.py
