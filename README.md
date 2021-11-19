# BOCS Control
Control scripts for the BOCS.

# Debian packaging

A Debian package can be built using Docker by installing the build dependencies and using `dpkg-buildpackage` for the actual build process.

```
docker run -it --rm -v `pwd`:/bocs_control -w /bocs_control --name deb-sid debian:sid /bin/bash
apt-get update && apt-get upgrade
apt-get install dh-make build-essential debhelper-compat dh-python python3 python3-serial python3-setuptools
dpkg-buildpackage
```
