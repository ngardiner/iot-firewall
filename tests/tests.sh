#!/bin/bash

echo Running tests on `python -c "import sys; print(sys.version)"`

echo Running setup script
./setup.sh test
