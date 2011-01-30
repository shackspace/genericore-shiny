#!/bin/bash
dirname="`dirname "$0"`"
mongod &
BINDIR=$dirname/../src
python2 $BINDIR/main.py "$@"
