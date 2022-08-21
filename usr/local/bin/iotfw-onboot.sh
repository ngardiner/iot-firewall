
# In Ubuntu 20.04 (at least) there's an issue with kea leaving a PID file behind
# This can cause the service to fail
# We run once at boot prior to starting the dhcp service, so we can fix this here

if [ -f /var/lib/kea/kea-leases4.csv.pid ]; then
  rm /var/lib/kea/kea-leases4.csv.pi
fi
