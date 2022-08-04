#!/bin/bash

# Enter the iot-firewall directory if we have not already
if [ -d iot-firewall ]; then
  cd iot-firewall || exit 0
fi

cp -r var /
