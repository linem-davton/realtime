#!/bin/bash

# make sure ptp4l is installed, service file is in place and ntp and ptp4l services are diabled and stopped
# Start NTP service
echo "Starting NTP service..."
sudo systemctl start systemd-timesyncd.service

# Wait for NTP to synchronize
echo "Waiting for NTP synchronization..."
while ! timedatectl status | grep -q 'synchronized: yes'; do
	sleep 1
done

echo "NTP synchronized, stopping NTP service..."
# Stop NTP service
sudo systemctl stop systemd-timesyncd.service

# Start PTP service
echo "Starting PTP service..."
sudo systemctl start ptp-slave.service
