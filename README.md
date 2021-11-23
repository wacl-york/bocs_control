# BOCS Control
Control scripts for the BOCS.

# Installation

Copy deb over
sudo apt install ./<version>.deb
Reboot
Confirm have /dev/SENSOR_ARRAY_A
Start data recording with systemctl start python3-bocs (NB: this can be made optional)
Check data appearing in ~/bocs/logs/SENSOR_ARRAY_A/SENSOR_ARRAY_A_data.log
Check control log with journalctl -u python3-bocs

# Debian packaging
A Debian package can be built using Docker by installing the build dependencies and using `dpkg-buildpackage` for the actual build process.

```
docker build -t bocs_debian_builder .
docker run --rm -v `pwd`:/bocs_control -w /bocs_control bocs_debian_builder
```
