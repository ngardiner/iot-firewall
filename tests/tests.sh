#!/bin/bash

echo Running tests on `python -c "import sys; print(sys.version)"`

echo Running setup script
./setup.sh test

echo Copy test cluster configuration

echo Start iotfw-admin service
./usr/local/bin/iotfw-admin.py -p /tmp/iotfw-admin.pid &

echo Check PID file exists
if [ ! -f "/tmp/iotfw-admin.pid" ]; then
  echo "ERROR: PID file does not exist (/tmp/iotfw-admin.pid)"
  exit 255
fi
