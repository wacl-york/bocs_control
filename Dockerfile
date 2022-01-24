FROM debian:stable

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y dh-make build-essential debhelper-compat dh-python python3 python3-serial python3-setuptools

ENTRYPOINT ["sh", "-c", "dpkg-buildpackage && mv ../*.deb ."]
