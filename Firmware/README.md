**FIRMWARE UPDATES ARE ALWAYS AT YOUR OWN RISK!**

**PEBBLE 2 updates could fail, but bricks did not happen so far**

This document is mostly copied from https://github.com/Freeyourgadget/Gadgetbridge/wiki/Pebble-Firmware-updates/

OG folder includes firmware updates for the original Pebble, Pebble Steel and Kickstarter edition pebble.

Time folder includes firmware updates for Pebble Time, Time Steel and Time Round.

Two folder includes firmware updates for the Pebble 2.

Based on Gadgetbridge's tests the following should be possible:

* Up or downgrade from 1.x/2.x to any 1.x/2.x firmware.
* Up or downgrade from 3.x/4.x to any 3.x/4.x firmware
* Upgrade from 1.x/2.x to 3.x via migration firmware

## Upgrading from 1.x/2.x to 3.x (Pebble, Pebble Steel)

### Instructions

1. Flash the migration firmware (example file name of a migration firmware: `3.x-migration_v1_5_v3.8-mig10.pbz`) and **wait till the Pebble reboots, ignoring errors if any** 
2. The pebble will start in a 3.x recovery, flash the real firmware from there

### Warnings
* Upgrading from 1.x/2.x to 3.x will update the recovery to 3.8
* Downgrading from 3.x to 2.x won't downgrade the recovery firmware and your data will be lost, gadgetbridge haven't tested it and do not know the correct procedure to update to 3.x again

**NOTE: Install firmware files from .pbz files by selecting them from a file manager and opening them in Gadgetbridge's App/FW Installer**

**DO NOT FLASH A RECOVERY FIRMWARE, IF YOU WANT TO UPDATE THE RECOVERY FIRMWARE TO A NEWER VERSION, INSTALL THE LATEST MIGRATION, AND THEN THE NORMAL FIRMWARE AGAIN**

## Upgrading from 3.x to 4.x (only available for the pebble time watches)

Just flash the firmware as normal, no special procedure needed.
