#!/usr/bin/env bash

# Initial system setup. Meant to be run as privileged user.

# Installing various system packages
apt-get update
apt-get upgrade
apt-get install -y postgresql libpq-dev 
apt-get install -y python-pip python-virtualenv python-dev git

# Setting up PostgreSQL database
sudo -u postgres createdb type_flashcards -T template0 -E UTF8 --locale=en_US.UTF8
echo "CREATE USER mjr;" | sudo -u postgres psql
