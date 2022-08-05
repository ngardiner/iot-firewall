#!/bin/bash

echo Running tests on `python -c "import sys; print(sys.version)"`

echo Running setup script
./setup.sh test

echo Copy test cluster configuration
cp /etc/iotfw/.test.cluster.db /etc/iotfw/cluster.db

echo Start iotfw-admin service
./usr/local/bin/iotfw-admin.py -i /tmp/iotfw-admin.pid -p 8081 &
sleep 5

echo Check PID file exists
if [ ! -f "/tmp/iotfw-admin.pid" ]; then
  echo "ERROR: PID file does not exist (/tmp/iotfw-admin.pid)"
  exit 255
fi

echo Check listener is active on port 8081
if [ `netstat -an | grep LIST | grep -c 8081` -lt 1 ]; then
  echo "ERROR: Process is not listening on port 8081"
  exit 255
fi
