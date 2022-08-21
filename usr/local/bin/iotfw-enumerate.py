#!/usr/bin/env python3

import pickle
import pynetbox
import pprint
import re

# Read configuration database
config = {}
try:
    with open('/etc/iotfw/config.db', 'rb') as handle:
        config = pickle.loads(handle.read())
except FileNotFoundError:
    config = {}

# Connect to netbox
nb = pynetbox.api(
    'http://' + config['netbox_ip'],
    token=config['netbox_token']
)

devices = nb.dcim.devices.all()
for device in devices:
  print(device)

fh = open("08-define-profiles.sh", "w")
fh.write("#!/bin/bash\n\n")
for x in classes:
  fh.write("ipset -q create profile:" + x + " hash:ip\n")
  for y in classes[x]:
    fh.write("ipset -q add profile:" + x + " " + y + "\n")
fh.close

