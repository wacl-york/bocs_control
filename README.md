# BOCS Data Collection

Contains the source code for the `python3-bocs` Debian package that runs the BOCS air quality instrument, recording data to local storage.
Deb files for installation are available in the [Releases page](https://github.com/wacl-york/bocs_control/releases).

# Setup Pi

The RaspberryPi needs setting up before the BOCS software can be installed.

  1. Install the latest version of [RaspberryPi OS with desktop](https://www.raspberrypi.com/software/) to a microSD card
  2. Boot up the Pi (outside of the BOCS) and follow the onscreen instructions to setup locale, password, WiFi access (if needed), and **make sure to update the software**
  3. Reboot
  4. OPTIONAL: If you want to either use the touchscreen display or connect via SSH then run `sudo raspi-config`, go into Interface Options and enable `Legacy Camera` and/or `SSH`. Then Reboot

The Pi can now be inserted into the BOCS and interfaced with by either SSH or connecting a keyboard to the USB port on the front panel, depending on what was configured in Step 4.

# Installation of BOCS data collection software

With the Pi housed in the BOCS and connected to a sensor array via USB, the data collection software is ready to be run.

  1. Download `python3-bocs_1.0.0-0_all.deb` from [the release page](https://github.com/wacl-york/bocs_control/releases/tag/v1.0.0) onto the Pi
  2. Install it with `sudo apt install ./python3-bocs_1.0.0-0_all.deb`

The data collection should start automatically; if a plaintext log file with the day's date doesn't appear in `~/bocs/data/` then check the log with `journalctl -t bocs_control`.

## Daily archiving

Provided the Raspberry Pi has its time set (either through NTP via a network connection or being manually set at each boot), each day at 01:00 the previous day's data is archived into a zip folder and placed in `~/bocs/data` using the same file naming convention as the data files.
Logs from this process are sent to the system log and can be viewed using `journalctl -t bocs_archive`.

# Building from source

If you want to build the program from source than you can use the provided `Dockerfile` to rebuild the Deb.
First clone this repository, then create a Debian Docker image with the build dependencies from this repo's root folder.

```
docker build -t bocs_debian_builder .
```

Build the Deb by running the image from the repository's top level directory, passing in the directory's contents.

```
docker run --rm -v `pwd`:/bocs_control -w /bocs_control bocs_debian_builder
```
