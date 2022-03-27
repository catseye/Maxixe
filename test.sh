#!/bin/sh

APPLIANCES=""
MISSING=""

if command -v python2 > /dev/null 2>&1; then
    APPLIANCES="$APPLIANCES doc/appliances/maxixe.py2.md"
else
    MISSING="${MISSING}2"
fi

if command -v python3 > /dev/null 2>&1; then
    APPLIANCES="$APPLIANCES doc/appliances/maxixe.py3.md"
else
    MISSING="${MISSING}3"
fi

if [ "x${MISSING}" = "x23" ]; then
    echo "Neither python2 nor python3 found on executable search path. Aborting."
    exit 1
fi

falderal $APPLIANCES doc/Maxixe.md doc/Examples.md || exit 1
