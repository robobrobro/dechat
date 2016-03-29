#!/bin/bash

nosetests -v --with-coverage --cover-package=dechat --cover-branches --cover-erase --cover-html \
    --cover-html-dir=./htmlcov "$@"
