#!/usr/bin/env bash

# Initial system setup. Meant to be run as privileged user.

# set everything to utf-8 because thai
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Installing various system packages
apt-get update
apt-get upgrade
apt-get install -y postgresql libpq-dev 
apt-get install -y python-pip python-virtualenv python-dev git vim

# Setting up PostgreSQL database
echo "CREATE USER vagrant WITH PASSWORD 'vagrant';" | sudo -u postgres psql
