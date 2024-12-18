#!/bin/bash

conda deactivate
source virtualenv/bin/activate
python manage.py runserver
