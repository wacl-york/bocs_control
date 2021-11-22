# BOCS Control
Control scripts for the BOCS.

# Debian packaging

A Debian package can be built using Docker by installing the build dependencies and using `dpkg-buildpackage` for the actual build process.

```
docker build -t bocs_debian_builder .
docker run --rm -v `pwd`:/bocs_control -w /bocs_control bocs_debian_builder
```
