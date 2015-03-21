#!/usr/bin/env bash

# Initial system setup. Meant to be run as privileged user.

# Installing various system packages
apt-get update
apt-get upgrade
apt-get install -y postgresql libpq-dev 
apt-get install -y python-pip python-virtualenv python-dev git vim

# Setting up PostgreSQL database
echo "CREATE USER vagrant WITH PASSWORD 'vagrant';" | sudo -u postgres psql
bash /type-flashcards/vagrant/app.sh
