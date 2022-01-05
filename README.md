# BOCS Data Collection

Contains the source code for the `python3-bocs` Debian package that runs the BOCS air quality instrument, recording data to local storage.
Released Deb files are available at <TODO>.

# Setup Pi

The RaspberryPi needs setting up before the BOCS software can be installed.

  1. Install the latest version of [RaspberryPi OS with desktop](https://www.raspberrypi.com/software/) to a microSD card
  2. Boot up the Pi (outside of the BOCS) and follow the onscreen instructions to setup locale, password, WiFi access (if needed), and **make sure to update the software**
  3. Reboot
  4. Run `sudo raspi-config`, go into Interface Options and enable both `SSH` and `Legacy Camera`
  5. Reboot

The Pi can now be inserted into the BOCS and interfaced with by either SSH or connecting a keyboard to the USB port on the front panel.

# Installation of BOCS data collection software

With the Pi housed in the BOCS and all wires connected as shown in <TODO document>, the data collection software is ready to be run.

  1. Download `python3-bocs_1.0.0-0_all.deb` from <TODO location> 
  2. Install it with `sudo apt install ./python3-bocs_1.0.0-0_all.deb`

The data collection should start automatically, confirm that data is appearing in `~/bocs/logs/data/`.
If isn't, check the log (`journalctl -t bocs_control`).

# Building from source

If the Deb isn't available, or you want to build the program from source than you can use the provided `Dockerfile` to rebuild the Deb.
First clone this repository, then create a Debian Docker image with the build dependencies from this repo's root folder.

```
docker build -t bocs_debian_builder .
```

Build the Deb by running the image from the repository's top level directory, passing in the directory's contents.

```
docker run --rm -v `pwd`:/bocs_control -w /bocs_control bocs_debian_builder
```

Install the Deb using the instructions as in the previous section.
