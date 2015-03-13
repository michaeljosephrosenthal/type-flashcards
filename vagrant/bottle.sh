#!/usr/bin/env bash

virtualenv --python=python2.7 ~/venv
source ~/venv/bin/activate
cd /type-flashcards/
pip install -r requirements.txt
