#!/bin/bash

# Install Required Packages
apt -y install kea-dhcp4-server python3-pip
pip3 install pynetbox

# Enter the iot-firewall directory if we have not already
if [ -d iot-firewall ]; then
  cd iot-firewall || exit 0
fi

# Add iotfw account
getent passwd iotfw > /dev/null
if [ $? -ne 0 ]; then
  useradd iotfw
fi

# Create pidfile directory
if [ ! -d /var/run/iotfw ]; then
  mkdir -p /var/run/iotfw
  chown -R iotfw: /var/run/iotfw
fi

# Copy files
cp -r etc /
cp -r usr /
cp -r var /

# Set permissions
chown -R iotfw: /etc/iotfw
chown iotfw: /usr/local/bin/iotfw-admin.py
chown -R iotfw: /var/lib/iotfw-admin

if [ "$1" != "test" ]; then

  # Reload systemd config
  systemctl daemon-reload

  # Enable necessary services
  systemctl enable iotfw-admin.service

fi
