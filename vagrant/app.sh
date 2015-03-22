#!/usr/bin/env bash

virtualenv --python=python2.7 ~/venv
pip install ipython honcho
source ~/venv/bin/activate
cd /type-flashcards/
pip install -r requirements.txt
cp vagrant/dev.env .env
echo "CREATE DATABASE type_flashcards;" | sudo -u postgres psql

honcho start web -e vagrant/init-db.env
honcho start init_dev_db
honcho run alembic stamp head
