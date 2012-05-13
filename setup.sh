#!/bin/bash

virtualenv --distribute -p python2.7 env
. env/bin/activate
pip install --upgrade sqlalchemy
