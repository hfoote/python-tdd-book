Provisioning a new site 
=======================

## Required packages:

* nginx
* Python3.11
* virtualenv + pip
* Git

eg, on Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python311 python3.11-venv

## Nginx virtual host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.mydomain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., staging.mydomain.com

** Folder structure

Assume we have a user account at /home/username

/home/username
|- sites
    |- DOMAIN1
    |   |- .env
    |   |- db.sqlite3
    |   |- manage.py etc
    |   |- static
    |   |- virtualenv
    |- DOMAIN2
        |- .env
        |- db.sqlite3
        |- etc


