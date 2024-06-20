#!/bin/bash
sudo apt install linuxptp -y

# create the systemd service files
sudo cp -v systemdUnits/ptp-master.service /etc/systemd/system/ptp-master.service
sudo cp -v systemdUnits/phc2sys-master.service /etc/systemd/system/phc2sys-master.service

# Enable and start the services
sudo systemctl enable ptp-master.service
sudo systemctl enable phc2sys-master.service

sudo systemctl start ptp-master.service
sudo systemctl start phc2sys-master.service
